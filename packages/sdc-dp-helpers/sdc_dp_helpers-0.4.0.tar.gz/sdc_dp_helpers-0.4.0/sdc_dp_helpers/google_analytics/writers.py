"""
    CUSTOM WRITER CLASSES
        - Class which manages writer tasks like
        auth, write metadata, write file, create dir structure
"""
import gzip
import io
import json
import os
from datetime import timezone, datetime
from pathlib import Path

import boto3
from interface import implements, Interface


# pylint: disable=no-init
class BaseWriter(Interface):
    """
        Base Writer Class with methods to implement when creating your own custom writer.
        Sets out a design pattern for creating the Custom writer class.

        Namely, the following methods should be implemented:
        (1) write metadata (optional)
        (2) append page
        (3) write file
    """

    def write_metadata(self, metadata: dict):
        """
            Method that writes metadata to local filesystem.
            args:
                metadata (dict) : metadata to be written
        """
        pass

    def append_page(self, report: list):
        """
            Called by main to get data and append rows to single array object.

            args:
                report (list): report data to append
        """
        pass

    def write_file(self):
        """Called to write a file or two database in bulk or s3"""
        pass


class CustomLocalJsonWriter:
    """
        Custom JSON Writer class which writes data to local filesystem.

        Writes data into a file.json per query. The files are written to a directory tree
        set out as GA/{viewid}/{metric}.
    """

    def __init__(
            self,
            file_name: str,
            folder_path: str,
            **kwargs
    ):
        # creates full path
        self.folder_path = folder_path
        # create file paths
        self.file_name = file_name
        # currently overwrites metadata.json each time
        self.metadata_file = kwargs.get("metadata_file", "metadata.json")
        # init data
        self.data = []
        # init path
        self.full_path = None

    @staticmethod
    def mkdir_if_not_exists(full_path: str):
        """
            Make a new directory if one doesn't exist
        """
        Path(full_path).mkdir(parents=True, exist_ok=True)

    def check_files_in_dir(self):
        """
            Return the length of files in a directory
        """
        return len(os.listdir(self.full_path))

    @staticmethod
    def timestamp_suffix():
        """builds a filename suffix from the current timestamp"""
        curr_time = datetime.now().replace(tzinfo=timezone.utc).timestamp()
        suff = str(round(curr_time, 2)).replace(".", "_")
        return suff

    @staticmethod
    def flatten_multilist(mylist: list = None):
        """Utility function to flatten google analytics report list of list of dict"""
        flat_list = []
        for sublist in mylist:
            for item in sublist:
                flat_list.append(item)
        return flat_list

    def append_page(self, report: list):
        """
            Called by main to get data and append rows to single array object.
            args:
                report (dict): report data to append
        """
        # when to write (wrapper)
        data = [r.get('data', {}).get('rows', []) for r in report]
        restructured_data = self.flatten_multilist(data)
        self.data = self.data + restructured_data


class CustomS3GZJsonWriter(CustomLocalJsonWriter, implements(BaseWriter)):
    """Class Extends Basic LocalGZJsonWriter"""

    def __init__(
            self,
            file_name: str,
            folder_path: str,
            bucket: str,
            profile_name: str = None,
            **kwargs
    ):
        self.os_path_sep = "/"

        if profile_name is None:
            self.boto3_session = boto3.Session()
        else:
            self.boto3_session = boto3.Session(profile_name=profile_name)

        self.bucket = bucket
        """Writes a general object to s3"""
        self.s3_resource = self.boto3_session.resource('s3')
        super().__init__(file_name=file_name, folder_path=folder_path, **kwargs)
        self.metadata_file = kwargs.get("metadata_file", "metadata.json.gz")

    def set_full_path(self, nested_dirs: list = None):
        """Set full path to write to"""
        # creates full path
        full_path = [self.folder_path]+nested_dirs
        return os.path.join(*full_path).replace('\\', '/')

    # pylint: disable=no-member,too-many-arguments
    def write_to_s3(
            self,
            json_data,
            data_path,
            mode="w",
            encoding="utf-8",
            ensure_ascii=False,
            default=None
    ):
        """
            Write report to s3 bucket
        """
        buffer = io.BytesIO()
        with gzip.GzipFile(fileobj=buffer, mode=mode) as file_:
            with io.TextIOWrapper(file_, encoding=encoding) as textio_obj:
                textio_obj.write(json.dumps(json_data, ensure_ascii=ensure_ascii, default=default))
        # write to s3
        buffer.seek(0)
        self.s3_resource.Bucket(self.bucket).put_object(
            Key=os.path.join(self.full_path, data_path).replace('\\', '/'),
            Body=buffer)

    def write_metadata(self, metadata: dict):
        """"
            Creates required GA/ViewID/metricName structure
        """
        # create directory structure if not exists
        self.full_path = self.set_full_path(nested_dirs=[
            metadata.get("viewID", '.'),
            metadata.get("metricName", '')])
        self.write_to_s3(json_data=metadata, data_path=self.metadata_file, mode="w")

    def write_file(self):
        """
            upload python dict into s3 bucket with gzip archive
        """
        # generate a unix timestamp suffix for file
        suff = self.timestamp_suffix()
        data_path = "{}_{}.json.gz".format(self.file_name, suff)
        self.write_to_s3(self.data, data_path, mode="wb")
        self.data = []
