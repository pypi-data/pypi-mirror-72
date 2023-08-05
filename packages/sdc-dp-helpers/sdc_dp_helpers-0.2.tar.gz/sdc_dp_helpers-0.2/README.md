# SDC DataPipeline Helpers

Contains code to enable data pipelines from Google Analytics through the v4 API. It leverages the the packages in `./sdc_dp_helpers/google_analytics/` code to drastically simplify the code in designing a new data pipeline. It achieves this by abstracting functionality that is commonly reused but still allows the user to write for their own use-case by exteding base class functionality.

### Requirements

- GCP service account with `Google Analytics read policy`
- GCP `service account email` added to Google Analytics

## Quick Start

Getting started with pulling batch data from ga and dumping in to .json

1. Make sure your python environment is set up.

2. Place \<client-secret-key\>.p12 in a folder like `./google_secrets` directory

3. Run

```
    make install-requirements
```
    You can find a requirements.yml in the repository.
3. Create an initial config.yaml

    Run the following code once off to create an initial data pipeline config.
    You can either write a python script or open a python repl to run the following:

```
    from sdc_dp_helpers.google_analytics.utils import init_config

    init_config('data_pipeline_config.yaml')
```
Remember to add the:
- client_secret _(in the reader config portion of the config)_
- scopes _(in the reader config portion of the config)_
- service_account_email _(in the reader config portion of the config)_
- viewIDs _(in the query config portion of the config)_

3. Writing your first pipeline.

    Start with the file provided at: `./data_pipeline.py`

4. Run the code

    note: this config should be in the same directory as data_pipeline.py

## Using & Extending

The data pipeline comprises 4 components, namely:
| components | description |
|---|---|
| reader class | reader class which pulls data through a request to the external API or source |
| writer class | writer class which writes data to file or destination |
| config_manager class | config loader, parser and query builder |
| data_pipeline script | `your data pipeline` script which executes the your pipeline |

The code is set up to simplify the the creation of new data pipelines and allow code sharing when it comes to data pipelines.
As such, when a pipeline has been constructed previously from a given external API or source, a new user need only write a `data pipeline script`. In some cases, a new user may require a different destination writer and can easily add this to the `writer class` 

### A class for writing data: Extending the BaseWriter class
The core advantage of of this pipeline is that querying data is separate from writing data to file. This allows each user to decide for themselves how they best like their data. Whether JSON or CSV or whether writing to blob storage or database instance. It leaves the power in your hands by allowing python to act like a "glue" language connecting up different parts. Theoretically, the reader and writer can leverage a different processing stacks without effecting one another.

## Future work

### Leveraging Serverless infrastructure

Executing production pipelines on serverless infrastructure would be a very benefical exercise. However, work would need to 
be done to adequately set up stateful serverless infrastructure to allow adequate control and scalability.

### Building a decorator for potential failure Modes

Two known failure modes exist. These are simply handled in typical `try-catch-except` statements if needed for now.
- HttpError - more general http errors
- HttpError:Service Unavailable - GA specific error
- TimeoutError - server or host not responding in time
- OSError - fails to complete os_handshake

## References
These are helpful references which someone may use to learn more about what you have done here.

- `Introduction to Analytics v4 API`: https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py
- `GA and Sampling`: [Understanding GA report sampling](https://www.bounteous.com/insights/2013/06/24/how-solve-google-analytics-sampling-8-ways-get-more-data/) 
- `GA sampling when samples > 500k`: [Setting queries to keep samples below GA sample limit](https://www.getresponse.com/blog/using-google-analytics)
- `Components of A query in GA`: [Understanding various parts incl. Metrics, Sampling, Dimensions, etc](https://medium.com/analytics-for-humans/a-cheat-sheet-for-mastering-google-analytics-api-requests-39d36e0f3a4a)
- `Duplicate records pulled`: [Is this Transaction duplicates](https://www.simoahava.com/analytics/prevent-google-analytics-duplicate-transactions-with-customtask/)
- `dateRange are inclusive`: [GA startDate, endDates are inclusive](https://stackoverflow.com/questions/21303291/google-analytics-api-start-and-end-date)
- `PyYaml: Extending the functionality`: [Extending the YAML loader with PyYaml](https://pyyaml.org/wiki/PyYAMLDocumentation)
- `Data completeness: isDataGolden` : [isDataGolden is True when a new request will not return any new results](https://developers.google.com/analytics/devguides/reporting/core/v4/rest/v4/reports/batchGet)
