# kaistack.clients.openapi_clients.cluster.ClusterServiceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_cluster_config**](ClusterServiceApi.md#get_cluster_config) | **GET** /v1/cluster/config | 
[**get_nodes**](ClusterServiceApi.md#get_nodes) | **GET** /v1/cluster/nodes | 
[**get_system_component**](ClusterServiceApi.md#get_system_component) | **GET** /v1/cluster/systemstatus | 


# **get_cluster_config**
> CodegenGetClusterConfigResponse get_cluster_config()



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.cluster
from kaistack.clients.openapi_clients.cluster.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.cluster.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.cluster.ClusterServiceApi(api_client)
    
    try:
        api_response = api_instance.get_cluster_config()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ClusterServiceApi->get_cluster_config: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**CodegenGetClusterConfigResponse**](CodegenGetClusterConfigResponse.md)

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

# **get_nodes**
> CodegenGetNodesResponse get_nodes()



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.cluster
from kaistack.clients.openapi_clients.cluster.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.cluster.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.cluster.ClusterServiceApi(api_client)
    
    try:
        api_response = api_instance.get_nodes()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ClusterServiceApi->get_nodes: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**CodegenGetNodesResponse**](CodegenGetNodesResponse.md)

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

# **get_system_component**
> CodegenGetSystemStatusResponse get_system_component()



### Example

```python
from __future__ import print_function
import time
import kaistack.clients.openapi_clients.cluster
from kaistack.clients.openapi_clients.cluster.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with kaistack.clients.openapi_clients.cluster.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = kaistack.clients.openapi_clients.cluster.ClusterServiceApi(api_client)
    
    try:
        api_response = api_instance.get_system_component()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ClusterServiceApi->get_system_component: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**CodegenGetSystemStatusResponse**](CodegenGetSystemStatusResponse.md)

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

