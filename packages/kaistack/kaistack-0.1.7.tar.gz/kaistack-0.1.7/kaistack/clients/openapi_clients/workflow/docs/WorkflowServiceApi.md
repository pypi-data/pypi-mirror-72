# kaistack.clients.openapi_clients.workflow.WorkflowServiceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_run**](WorkflowServiceApi.md#create_run) | **POST** /v1/workflow/runs | 
[**get_all_models_latest_version**](WorkflowServiceApi.md#get_all_models_latest_version) | **GET** /v1/models | 
[**get_argo_workflow**](WorkflowServiceApi.md#get_argo_workflow) | **GET** /v1/workflow/pipeline/{runId} | 
[**get_artifact_with_properties**](WorkflowServiceApi.md#get_artifact_with_properties) | **GET** /v1/artifacts/full/{id} | 
[**get_artifacts_with_filter**](WorkflowServiceApi.md#get_artifacts_with_filter) | **GET** /v1/artifacts | 
[**get_experiment_pipeline_runs**](WorkflowServiceApi.md#get_experiment_pipeline_runs) | **GET** /v1/workflow/experiments/{experimentId}/runs | 
[**get_metrics**](WorkflowServiceApi.md#get_metrics) | **GET** /v1/metrics | 
[**get_model_all_versions**](WorkflowServiceApi.md#get_model_all_versions) | **GET** /v1/models/{name} | 
[**get_params**](WorkflowServiceApi.md#get_params) | **GET** /v1/params | 
[**get_pipeline_experiment_name**](WorkflowServiceApi.md#get_pipeline_experiment_name) | **GET** /v1/workflow/pipeline/{runId}/experiment | 
[**get_pipeline_run_id**](WorkflowServiceApi.md#get_pipeline_run_id) | **GET** /v1/workflow/{workflowName}/run | 
[**get_pipeline_runs**](WorkflowServiceApi.md#get_pipeline_runs) | **GET** /v1/workflow/pipeline/{pipelineRunId}/runs | 
[**get_run**](WorkflowServiceApi.md#get_run) | **GET** /v1/workflow/runs/{id} | 
[**get_run_by_name**](WorkflowServiceApi.md#get_run_by_name) | **GET** /v1/workflow/runs/name/{name} | 
[**log_artifact_meta**](WorkflowServiceApi.md#log_artifact_meta) | **POST** /v1/artifacts/meta | 
[**log_metrics**](WorkflowServiceApi.md#log_metrics) | **POST** /v1/metrics | 
[**log_params**](WorkflowServiceApi.md#log_params) | **POST** /v1/params | 
[**resubmit_workflow**](WorkflowServiceApi.md#resubmit_workflow) | **PUT** /v1/workflow/{namespace}/{name}/resubmit | 
[**resume_workflow**](WorkflowServiceApi.md#resume_workflow) | **PUT** /v1/workflow/{namespace}/{name}/resume | 
[**retry_workflow**](WorkflowServiceApi.md#retry_workflow) | **PUT** /v1/workflow/{namespace}/{name}/retry | 
[**suspend_workflow**](WorkflowServiceApi.md#suspend_workflow) | **PUT** /v1/workflow/{namespace}/{name}/suspend | 
[**terminate_workflow**](WorkflowServiceApi.md#terminate_workflow) | **PUT** /v1/workflow/{namespace}/{name}/terminate | 
[**update_pipeline_default_version**](WorkflowServiceApi.md#update_pipeline_default_version) | **POST** /v1/pipeline/{pipelineId}/default_version/{version} | 


# **create_run**
> CodegenCreateRunResponse create_run(body)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.workflow
from kaistack.clients.openapi_clients.workflow.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.workflow.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.workflow.WorkflowServiceApi(api_client)
    body = kaistack.clients.openapi_clients.workflow.CodegenRun() # CodegenRun | 

    try:
        api_response = api_instance.create_run(body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->create_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CodegenRun**](CodegenRun.md)|  | 

### Return type

[**CodegenCreateRunResponse**](CodegenCreateRunResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_models_latest_version**
> CodegenGetAllModelsLatestVersionResponse get_all_models_latest_version()



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.workflow
from kaistack.clients.openapi_clients.workflow.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.workflow.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.workflow.WorkflowServiceApi(api_client)
    
    try:
        api_response = api_instance.get_all_models_latest_version()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->get_all_models_latest_version: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**CodegenGetAllModelsLatestVersionResponse**](CodegenGetAllModelsLatestVersionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_argo_workflow**
> CodegenGetArgoWorkflowResponse get_argo_workflow(run_id)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.workflow
from kaistack.clients.openapi_clients.workflow.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.workflow.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.workflow.WorkflowServiceApi(api_client)
    run_id = 'run_id_example' # str | 

    try:
        api_response = api_instance.get_argo_workflow(run_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->get_argo_workflow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_id** | **str**|  | 

### Return type

[**CodegenGetArgoWorkflowResponse**](CodegenGetArgoWorkflowResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_artifact_with_properties**
> CodegenGetArtifactWithPropertiesResponse get_artifact_with_properties(id)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.workflow
from kaistack.clients.openapi_clients.workflow.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.workflow.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.workflow.WorkflowServiceApi(api_client)
    id = 'id_example' # str | 

    try:
        api_response = api_instance.get_artifact_with_properties(id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->get_artifact_with_properties: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**CodegenGetArtifactWithPropertiesResponse**](CodegenGetArtifactWithPropertiesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_artifacts_with_filter**
> CodegenGetArtifactsResponse get_artifacts_with_filter(filter_experiment=filter_experiment, filter_pipeline_run_id=filter_pipeline_run_id, filter_run_id=filter_run_id)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.workflow
from kaistack.clients.openapi_clients.workflow.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.workflow.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.workflow.WorkflowServiceApi(api_client)
    filter_experiment = 'filter_experiment_example' # str |  (optional)
filter_pipeline_run_id = 'filter_pipeline_run_id_example' # str |  (optional)
filter_run_id = 'filter_run_id_example' # str |  (optional)

    try:
        api_response = api_instance.get_artifacts_with_filter(filter_experiment=filter_experiment, filter_pipeline_run_id=filter_pipeline_run_id, filter_run_id=filter_run_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->get_artifacts_with_filter: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter_experiment** | **str**|  | [optional] 
 **filter_pipeline_run_id** | **str**|  | [optional] 
 **filter_run_id** | **str**|  | [optional] 

### Return type

[**CodegenGetArtifactsResponse**](CodegenGetArtifactsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_experiment_pipeline_runs**
> CodegenGetExperimentRunsResponse get_experiment_pipeline_runs(experiment_id)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.workflow
from kaistack.clients.openapi_clients.workflow.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.workflow.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.workflow.WorkflowServiceApi(api_client)
    experiment_id = 'experiment_id_example' # str | 

    try:
        api_response = api_instance.get_experiment_pipeline_runs(experiment_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->get_experiment_pipeline_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **experiment_id** | **str**|  | 

### Return type

[**CodegenGetExperimentRunsResponse**](CodegenGetExperimentRunsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_metrics**
> CodegenGetMetricsResponse get_metrics(filter_experiment=filter_experiment, filter_pipeline_run_id=filter_pipeline_run_id, filter_run_id=filter_run_id)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.workflow
from kaistack.clients.openapi_clients.workflow.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.workflow.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.workflow.WorkflowServiceApi(api_client)
    filter_experiment = 'filter_experiment_example' # str |  (optional)
filter_pipeline_run_id = 'filter_pipeline_run_id_example' # str |  (optional)
filter_run_id = 'filter_run_id_example' # str |  (optional)

    try:
        api_response = api_instance.get_metrics(filter_experiment=filter_experiment, filter_pipeline_run_id=filter_pipeline_run_id, filter_run_id=filter_run_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->get_metrics: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter_experiment** | **str**|  | [optional] 
 **filter_pipeline_run_id** | **str**|  | [optional] 
 **filter_run_id** | **str**|  | [optional] 

### Return type

[**CodegenGetMetricsResponse**](CodegenGetMetricsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_model_all_versions**
> CodegenGetModelAllVersionsResponse get_model_all_versions(name)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.workflow
from kaistack.clients.openapi_clients.workflow.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.workflow.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.workflow.WorkflowServiceApi(api_client)
    name = 'name_example' # str | 

    try:
        api_response = api_instance.get_model_all_versions(name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->get_model_all_versions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 

### Return type

[**CodegenGetModelAllVersionsResponse**](CodegenGetModelAllVersionsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_params**
> CodegenGetParamsResponse get_params(filter_experiment=filter_experiment, filter_pipeline_run_id=filter_pipeline_run_id, filter_run_id=filter_run_id)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.workflow
from kaistack.clients.openapi_clients.workflow.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.workflow.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.workflow.WorkflowServiceApi(api_client)
    filter_experiment = 'filter_experiment_example' # str |  (optional)
filter_pipeline_run_id = 'filter_pipeline_run_id_example' # str |  (optional)
filter_run_id = 'filter_run_id_example' # str |  (optional)

    try:
        api_response = api_instance.get_params(filter_experiment=filter_experiment, filter_pipeline_run_id=filter_pipeline_run_id, filter_run_id=filter_run_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->get_params: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter_experiment** | **str**|  | [optional] 
 **filter_pipeline_run_id** | **str**|  | [optional] 
 **filter_run_id** | **str**|  | [optional] 

### Return type

[**CodegenGetParamsResponse**](CodegenGetParamsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_pipeline_experiment_name**
> CodegenGetPipelineExperimentNameResponse get_pipeline_experiment_name(run_id)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.workflow
from kaistack.clients.openapi_clients.workflow.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.workflow.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.workflow.WorkflowServiceApi(api_client)
    run_id = 'run_id_example' # str | 

    try:
        api_response = api_instance.get_pipeline_experiment_name(run_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->get_pipeline_experiment_name: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_id** | **str**|  | 

### Return type

[**CodegenGetPipelineExperimentNameResponse**](CodegenGetPipelineExperimentNameResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_pipeline_run_id**
> CodegenGetPipelineRunIdResponse get_pipeline_run_id(workflow_name)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.workflow
from kaistack.clients.openapi_clients.workflow.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.workflow.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.workflow.WorkflowServiceApi(api_client)
    workflow_name = 'workflow_name_example' # str | 

    try:
        api_response = api_instance.get_pipeline_run_id(workflow_name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->get_pipeline_run_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workflow_name** | **str**|  | 

### Return type

[**CodegenGetPipelineRunIdResponse**](CodegenGetPipelineRunIdResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_pipeline_runs**
> CodegenGetPipelineRunsResponse get_pipeline_runs(pipeline_run_id)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.workflow
from kaistack.clients.openapi_clients.workflow.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.workflow.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.workflow.WorkflowServiceApi(api_client)
    pipeline_run_id = 'pipeline_run_id_example' # str | 

    try:
        api_response = api_instance.get_pipeline_runs(pipeline_run_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->get_pipeline_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pipeline_run_id** | **str**|  | 

### Return type

[**CodegenGetPipelineRunsResponse**](CodegenGetPipelineRunsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_run**
> CodegenGetRunResponse get_run(id)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.workflow
from kaistack.clients.openapi_clients.workflow.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.workflow.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.workflow.WorkflowServiceApi(api_client)
    id = 'id_example' # str | 

    try:
        api_response = api_instance.get_run(id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->get_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**CodegenGetRunResponse**](CodegenGetRunResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_run_by_name**
> CodegenGetRunByNameResponse get_run_by_name(name)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.workflow
from kaistack.clients.openapi_clients.workflow.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.workflow.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.workflow.WorkflowServiceApi(api_client)
    name = 'name_example' # str | 

    try:
        api_response = api_instance.get_run_by_name(name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->get_run_by_name: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 

### Return type

[**CodegenGetRunByNameResponse**](CodegenGetRunByNameResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **log_artifact_meta**
> CodegenLogArtifactMetaResponse log_artifact_meta(body)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.workflow
from kaistack.clients.openapi_clients.workflow.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.workflow.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.workflow.WorkflowServiceApi(api_client)
    body = kaistack.clients.openapi_clients.workflow.CodegenArtifactMeta() # CodegenArtifactMeta | 

    try:
        api_response = api_instance.log_artifact_meta(body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->log_artifact_meta: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CodegenArtifactMeta**](CodegenArtifactMeta.md)|  | 

### Return type

[**CodegenLogArtifactMetaResponse**](CodegenLogArtifactMetaResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **log_metrics**
> CodegenLogMetricsResponse log_metrics(body)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.workflow
from kaistack.clients.openapi_clients.workflow.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.workflow.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.workflow.WorkflowServiceApi(api_client)
    body = 'body_example' # str | grpc-gateway does not support repeated field in body. Pass a json string instead

    try:
        api_response = api_instance.log_metrics(body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->log_metrics: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **str**| grpc-gateway does not support repeated field in body. Pass a json string instead | 

### Return type

[**CodegenLogMetricsResponse**](CodegenLogMetricsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **log_params**
> CodegenLogParamsResponse log_params(body)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.workflow
from kaistack.clients.openapi_clients.workflow.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.workflow.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.workflow.WorkflowServiceApi(api_client)
    body = 'body_example' # str | grpc-gateway does not support repeated field in body. Pass a json string instead

    try:
        api_response = api_instance.log_params(body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->log_params: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **str**| grpc-gateway does not support repeated field in body. Pass a json string instead | 

### Return type

[**CodegenLogParamsResponse**](CodegenLogParamsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resubmit_workflow**
> CodegenWorkflowActionResponse resubmit_workflow(namespace, name)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.workflow
from kaistack.clients.openapi_clients.workflow.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.workflow.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.workflow.WorkflowServiceApi(api_client)
    namespace = 'namespace_example' # str | 
name = 'name_example' # str | 

    try:
        api_response = api_instance.resubmit_workflow(namespace, name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->resubmit_workflow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**|  | 
 **name** | **str**|  | 

### Return type

[**CodegenWorkflowActionResponse**](CodegenWorkflowActionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resume_workflow**
> CodegenWorkflowActionResponse resume_workflow(namespace, name)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.workflow
from kaistack.clients.openapi_clients.workflow.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.workflow.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.workflow.WorkflowServiceApi(api_client)
    namespace = 'namespace_example' # str | 
name = 'name_example' # str | 

    try:
        api_response = api_instance.resume_workflow(namespace, name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->resume_workflow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**|  | 
 **name** | **str**|  | 

### Return type

[**CodegenWorkflowActionResponse**](CodegenWorkflowActionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retry_workflow**
> CodegenWorkflowActionResponse retry_workflow(namespace, name)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.workflow
from kaistack.clients.openapi_clients.workflow.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.workflow.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.workflow.WorkflowServiceApi(api_client)
    namespace = 'namespace_example' # str | 
name = 'name_example' # str | 

    try:
        api_response = api_instance.retry_workflow(namespace, name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->retry_workflow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**|  | 
 **name** | **str**|  | 

### Return type

[**CodegenWorkflowActionResponse**](CodegenWorkflowActionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **suspend_workflow**
> CodegenWorkflowActionResponse suspend_workflow(namespace, name)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.workflow
from kaistack.clients.openapi_clients.workflow.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.workflow.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.workflow.WorkflowServiceApi(api_client)
    namespace = 'namespace_example' # str | 
name = 'name_example' # str | 

    try:
        api_response = api_instance.suspend_workflow(namespace, name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->suspend_workflow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**|  | 
 **name** | **str**|  | 

### Return type

[**CodegenWorkflowActionResponse**](CodegenWorkflowActionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **terminate_workflow**
> CodegenWorkflowActionResponse terminate_workflow(namespace, name)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.workflow
from kaistack.clients.openapi_clients.workflow.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.workflow.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.workflow.WorkflowServiceApi(api_client)
    namespace = 'namespace_example' # str | 
name = 'name_example' # str | 

    try:
        api_response = api_instance.terminate_workflow(namespace, name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->terminate_workflow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**|  | 
 **name** | **str**|  | 

### Return type

[**CodegenWorkflowActionResponse**](CodegenWorkflowActionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_pipeline_default_version**
> CodegenUpdatePipelineDefaultVersionResponse update_pipeline_default_version(pipeline_id, version)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.workflow
from kaistack.clients.openapi_clients.workflow.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.workflow.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.workflow.WorkflowServiceApi(api_client)
    pipeline_id = 'pipeline_id_example' # str | 
version = 'version_example' # str | 

    try:
        api_response = api_instance.update_pipeline_default_version(pipeline_id, version)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->update_pipeline_default_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pipeline_id** | **str**|  | 
 **version** | **str**|  | 

### Return type

[**CodegenUpdatePipelineDefaultVersionResponse**](CodegenUpdatePipelineDefaultVersionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

