# cloudmersive_configuration_api_client
Config API lets you easily manage configuration at scale.

This Python package provides a native API client for [Cloudmersive Configuration](https://www.cloudmersive.com/)

- API version: v1
- Package version: 3.0.1
- Build package: io.swagger.codegen.languages.PythonClientCodegen

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import cloudmersive_configuration_api_client 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import cloudmersive_configuration_api_client
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import cloudmersive_configuration_api_client
from cloudmersive_configuration_api_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Apikey
configuration = cloudmersive_configuration_api_client.Configuration()
configuration.api_key['Apikey'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Apikey'] = 'Bearer'

# create an instance of the API class
api_instance = cloudmersive_configuration_api_client.OrchestratorApi(cloudmersive_configuration_api_client.ApiClient(configuration))
request = cloudmersive_configuration_api_client.HttpOrchestrationRequest() # HttpOrchestrationRequest | 

try:
    # Orchestrate multiple HTTP API calls with a single API call in the order specified.  Call other Cloudmersive APIs or third party APIs.  For Cloudmersive APIs, the API Key will automatically propogate to the child calls without needing to be set explicitly.  Name each task and reference the output of a previous task in the inputs to a given task.
    api_response = api_instance.orchestrator_http_simple(request)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrchestratorApi->orchestrator_http_simple: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *https://api.cloudmersive.com*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*OrchestratorApi* | [**orchestrator_http_simple**](docs/OrchestratorApi.md#orchestrator_http_simple) | **POST** /config/orchestrator/http/simple | Orchestrate multiple HTTP API calls with a single API call in the order specified.  Call other Cloudmersive APIs or third party APIs.  For Cloudmersive APIs, the API Key will automatically propogate to the child calls without needing to be set explicitly.  Name each task and reference the output of a previous task in the inputs to a given task.
*SettingsApi* | [**settings_create_setting**](docs/SettingsApi.md#settings_create_setting) | **POST** /config/settings/create | Create a setting in the specified bucket
*SettingsApi* | [**settings_list_settings**](docs/SettingsApi.md#settings_list_settings) | **POST** /config/settings/list | Enumerate the settings in a bucket
*SettingsApi* | [**settings_update_setting**](docs/SettingsApi.md#settings_update_setting) | **POST** /config/settings/update | Update a setting


## Documentation For Models

 - [CreateSettingRequest](docs/CreateSettingRequest.md)
 - [CreateSettingResponse](docs/CreateSettingResponse.md)
 - [HttpFormDataParameter](docs/HttpFormDataParameter.md)
 - [HttpGetParameter](docs/HttpGetParameter.md)
 - [HttpOrchestrationHeader](docs/HttpOrchestrationHeader.md)
 - [HttpOrchestrationRequest](docs/HttpOrchestrationRequest.md)
 - [HttpOrchestrationResponse](docs/HttpOrchestrationResponse.md)
 - [HttpOrchestrationTask](docs/HttpOrchestrationTask.md)
 - [HttpRawBinaryParameter](docs/HttpRawBinaryParameter.md)
 - [HttpRawTextParameter](docs/HttpRawTextParameter.md)
 - [HttpWwwFormUrlEncodedParameter](docs/HttpWwwFormUrlEncodedParameter.md)
 - [ListSettingsRequest](docs/ListSettingsRequest.md)
 - [ListSettingsResponse](docs/ListSettingsResponse.md)
 - [SettingValue](docs/SettingValue.md)
 - [TaskOutputReference](docs/TaskOutputReference.md)
 - [UpdateSettingRequest](docs/UpdateSettingRequest.md)
 - [UpdateSettingResponse](docs/UpdateSettingResponse.md)


## Documentation For Authorization


## Apikey

- **Type**: API key
- **API key parameter name**: Apikey
- **Location**: HTTP header


## Author



