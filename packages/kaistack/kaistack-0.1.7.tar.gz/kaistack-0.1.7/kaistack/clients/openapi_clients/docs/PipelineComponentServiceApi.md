# kaistack.clients.openapi_clients.PipelineComponentServiceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_component**](PipelineComponentServiceApi.md#create_component) | **POST** /v1/pipeline/components | 
[**delete_component**](PipelineComponentServiceApi.md#delete_component) | **DELETE** /v1/pipeline/components/{id} | 
[**get_component**](PipelineComponentServiceApi.md#get_component) | **GET** /v1/pipeline/components/{id} | 
[**get_component_by_name**](PipelineComponentServiceApi.md#get_component_by_name) | **GET** /v1/pipeline/components/name/{name} | 
[**list_component_versions**](PipelineComponentServiceApi.md#list_component_versions) | **GET** /v1/pipeline/components/verions/{id} | 
[**list_components**](PipelineComponentServiceApi.md#list_components) | **GET** /v1/pipeline/components | 
[**update_component**](PipelineComponentServiceApi.md#update_component) | **PUT** /v1/pipeline/components | 


# **create_component**
> CodegenCreateComponentResponse create_component(body)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients
from kaistack.clients.openapi_clients.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.PipelineComponentServiceApi(api_client)
    body = kaistack.clients.openapi_clients.CodegenPipelineComponent() # CodegenPipelineComponent | 

    try:
        api_response = api_instance.create_component(body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling PipelineComponentServiceApi->create_component: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CodegenPipelineComponent**](CodegenPipelineComponent.md)|  | 

### Return type

[**CodegenCreateComponentResponse**](CodegenCreateComponentResponse.md)

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

# **delete_component**
> CodegenDeleteComponentResponse delete_component(id)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients
from kaistack.clients.openapi_clients.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.PipelineComponentServiceApi(api_client)
    id = 'id_example' # str | 

    try:
        api_response = api_instance.delete_component(id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling PipelineComponentServiceApi->delete_component: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**CodegenDeleteComponentResponse**](CodegenDeleteComponentResponse.md)

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

# **get_component**
> CodegenGetComponentResponse get_component(id)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients
from kaistack.clients.openapi_clients.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.PipelineComponentServiceApi(api_client)
    id = 'id_example' # str | 

    try:
        api_response = api_instance.get_component(id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling PipelineComponentServiceApi->get_component: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**CodegenGetComponentResponse**](CodegenGetComponentResponse.md)

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

# **get_component_by_name**
> CodegenGetComponentByNameResponse get_component_by_name(name, version=version)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients
from kaistack.clients.openapi_clients.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.PipelineComponentServiceApi(api_client)
    name = 'name_example' # str | 
version = 'version_example' # str |  (optional)

    try:
        api_response = api_instance.get_component_by_name(name, version=version)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling PipelineComponentServiceApi->get_component_by_name: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 
 **version** | **str**|  | [optional] 

### Return type

[**CodegenGetComponentByNameResponse**](CodegenGetComponentByNameResponse.md)

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

# **list_component_versions**
> CodegenListComponentVersionsResponse list_component_versions(id)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients
from kaistack.clients.openapi_clients.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.PipelineComponentServiceApi(api_client)
    id = 'id_example' # str | 

    try:
        api_response = api_instance.list_component_versions(id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling PipelineComponentServiceApi->list_component_versions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**CodegenListComponentVersionsResponse**](CodegenListComponentVersionsResponse.md)

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

# **list_components**
> CodegenListComponentsResponse list_components()



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients
from kaistack.clients.openapi_clients.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.PipelineComponentServiceApi(api_client)
    
    try:
        api_response = api_instance.list_components()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling PipelineComponentServiceApi->list_components: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**CodegenListComponentsResponse**](CodegenListComponentsResponse.md)

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

# **update_component**
> CodegenUpdateComponentResponse update_component(body)



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients
from kaistack.clients.openapi_clients.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.PipelineComponentServiceApi(api_client)
    body = kaistack.clients.openapi_clients.CodegenPipelineComponent() # CodegenPipelineComponent | 

    try:
        api_response = api_instance.update_component(body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling PipelineComponentServiceApi->update_component: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CodegenPipelineComponent**](CodegenPipelineComponent.md)|  | 

### Return type

[**CodegenUpdateComponentResponse**](CodegenUpdateComponentResponse.md)

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

