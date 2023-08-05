# agilicus_api.MessagesApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_message**](MessagesApi.md#create_message) | **POST** /v1/user_messages/{user_id}/message | Create a message (to a user)
[**create_message_user**](MessagesApi.md#create_message_user) | **POST** /v1/user_messages | create a user with messaging endpoints
[**list_message_users**](MessagesApi.md#list_message_users) | **GET** /v1/user_messages | List all users
[**replace_message_user**](MessagesApi.md#replace_message_user) | **PUT** /v1/user_messages | update a user with messaging endpoints


# **create_message**
> Message create_message(user_id, message)

Create a message (to a user)

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

    try:
        # Create a message (to a user)
        api_response = api_instance.create_message(user_id, message)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling MessagesApi->create_message: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path | 
 **message** | [**Message**](Message.md)| Message | 

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

# **create_message_user**
> MessageUser create_message_user(message_user)

create a user with messaging endpoints

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
    message_user = agilicus_api.MessageUser() # MessageUser | Message

    try:
        # create a user with messaging endpoints
        api_response = api_instance.create_message_user(message_user)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling MessagesApi->create_message_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **message_user** | [**MessageUser**](MessageUser.md)| Message | 

### Return type

[**MessageUser**](MessageUser.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully created user |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_message_users**
> ListMessageUsersResponse list_message_users(limit=limit)

List all users

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
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)

    try:
        # List all users
        api_response = api_instance.list_message_users(limit=limit)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling MessagesApi->list_message_users: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]

### Return type

[**ListMessageUsersResponse**](ListMessageUsersResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of all users |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_message_user**
> MessageUser replace_message_user(message_user)

update a user with messaging endpoints

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
    message_user = agilicus_api.MessageUser() # MessageUser | Message

    try:
        # update a user with messaging endpoints
        api_response = api_instance.replace_message_user(message_user)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling MessagesApi->replace_message_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **message_user** | [**MessageUser**](MessageUser.md)| Message | 

### Return type

[**MessageUser**](MessageUser.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully updated user |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

