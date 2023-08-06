# agilicus_api.MessagesApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_message_endpoint**](MessagesApi.md#create_message_endpoint) | **POST** /v1/messages | Create a messaging endpoint
[**create_user_message**](MessagesApi.md#create_user_message) | **POST** /v1/messages/{user_id}/send | send a message to a user on all (optionally of a type) endpoints.
[**delete_message_endpoint**](MessagesApi.md#delete_message_endpoint) | **DELETE** /v1/messages/{message_endpoint_id} | Delete a messaging endpoint
[**get_message_endpoint**](MessagesApi.md#get_message_endpoint) | **GET** /v1/messages/{message_endpoint_id} | Get a message endpoint
[**list_message_endpoints**](MessagesApi.md#list_message_endpoints) | **GET** /v1/messages | List all message endpoints (all users)
[**replace_message_endpoint**](MessagesApi.md#replace_message_endpoint) | **PUT** /v1/messages/{message_endpoint_id} | Update a messaging endpoint


# **create_message_endpoint**
> MessageEndpoint create_message_endpoint(message_endpoint, user_id=user_id)

Create a messaging endpoint

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.MessagesApi(api_client)
    message_endpoint = agilicus_api.MessageEndpoint() # MessageEndpoint | Message
user_id = '1234' # str | Query based on user id (optional)

    try:
        # Create a messaging endpoint
        api_response = api_instance.create_message_endpoint(message_endpoint, user_id=user_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling MessagesApi->create_message_endpoint: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **message_endpoint** | [**MessageEndpoint**](MessageEndpoint.md)| Message | 
 **user_id** | **str**| Query based on user id | [optional] 

### Return type

[**MessageEndpoint**](MessageEndpoint.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully created messaging endpoint |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_user_message**
> Message create_user_message(user_id, message, message_endpoint_type=message_endpoint_type)

send a message to a user on all (optionally of a type) endpoints.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.MessagesApi(api_client)
    user_id = '1234' # str | user_id path
message = agilicus_api.Message() # Message | Message
message_endpoint_type = agilicus_api.MessageEndpointType() # MessageEndpointType | messaging endpoint type (optional)

    try:
        # send a message to a user on all (optionally of a type) endpoints.
        api_response = api_instance.create_user_message(user_id, message, message_endpoint_type=message_endpoint_type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling MessagesApi->create_user_message: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path | 
 **message** | [**Message**](Message.md)| Message | 
 **message_endpoint_type** | [**MessageEndpointType**](.md)| messaging endpoint type | [optional] 

### Return type

[**Message**](Message.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Return the message with uuid filled in |  -  |
**404** | User not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_message_endpoint**
> delete_message_endpoint(message_endpoint_id, user_id=user_id)

Delete a messaging endpoint

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.MessagesApi(api_client)
    message_endpoint_id = '1234' # str | messaging endpoint id
user_id = '1234' # str | Query based on user id (optional)

    try:
        # Delete a messaging endpoint
        api_instance.delete_message_endpoint(message_endpoint_id, user_id=user_id)
    except ApiException as e:
        print("Exception when calling MessagesApi->delete_message_endpoint: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **message_endpoint_id** | **str**| messaging endpoint id | 
 **user_id** | **str**| Query based on user id | [optional] 

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Messaging endpoint deleted |  -  |
**404** | Messaging endpoint not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_message_endpoint**
> MessageEndpoint get_message_endpoint(message_endpoint_id, user_id=user_id)

Get a message endpoint

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.MessagesApi(api_client)
    message_endpoint_id = '1234' # str | messaging endpoint id
user_id = '1234' # str | Query based on user id (optional)

    try:
        # Get a message endpoint
        api_response = api_instance.get_message_endpoint(message_endpoint_id, user_id=user_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling MessagesApi->get_message_endpoint: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **message_endpoint_id** | **str**| messaging endpoint id | 
 **user_id** | **str**| Query based on user id | [optional] 

### Return type

[**MessageEndpoint**](MessageEndpoint.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return the detail of the message endpoint |  -  |
**404** | Messaging endpoint not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_message_endpoints**
> ListMessageEndpointsResponse list_message_endpoints(user_id=user_id, limit=limit)

List all message endpoints (all users)

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.MessagesApi(api_client)
    user_id = '1234' # str | Query based on user id (optional)
limit = 500 # int | limit the number of rows in the response (optional) (default to 500)

    try:
        # List all message endpoints (all users)
        api_response = api_instance.list_message_endpoints(user_id=user_id, limit=limit)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling MessagesApi->list_message_endpoints: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| Query based on user id | [optional] 
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]

### Return type

[**ListMessageEndpointsResponse**](ListMessageEndpointsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of all message endpoints (for all users if user_id not present) |  -  |
**404** | No messaging endpoints exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_message_endpoint**
> MessageEndpoint replace_message_endpoint(message_endpoint_id, message_endpoint, user_id=user_id)

Update a messaging endpoint

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.MessagesApi(api_client)
    message_endpoint_id = '1234' # str | messaging endpoint id
message_endpoint = agilicus_api.MessageEndpoint() # MessageEndpoint | Message
user_id = '1234' # str | Query based on user id (optional)

    try:
        # Update a messaging endpoint
        api_response = api_instance.replace_message_endpoint(message_endpoint_id, message_endpoint, user_id=user_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling MessagesApi->replace_message_endpoint: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **message_endpoint_id** | **str**| messaging endpoint id | 
 **message_endpoint** | [**MessageEndpoint**](MessageEndpoint.md)| Message | 
 **user_id** | **str**| Query based on user id | [optional] 

### Return type

[**MessageEndpoint**](MessageEndpoint.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully updated messaging endpoint |  -  |
**404** | Messaging endpoint not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

