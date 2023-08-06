# agilicus_api.ChallengesApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_challenge**](ChallengesApi.md#create_challenge) | **POST** /v1/challenges | create a challenge
[**delete_challenge**](ChallengesApi.md#delete_challenge) | **DELETE** /v1/challenges/{challenge_id} | Delete the challenge specified by challenge_id
[**get_answer**](ChallengesApi.md#get_answer) | **GET** /v1/challenges/{challenge_id}/answers | answer a challenge
[**get_challenge**](ChallengesApi.md#get_challenge) | **GET** /v1/challenges/{challenge_id} | Get the challenge specified by challenge_id
[**replace_challenge**](ChallengesApi.md#replace_challenge) | **PUT** /v1/challenges/{challenge_id} | Replace the challenge specified by challenge_id


# **create_challenge**
> Challenge create_challenge(challenge)

create a challenge

Creates a challenge according to the provide specification. This challenge will persist for a period of time waiting for the challenge to be passed. It will eventually time out. 

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
    api_instance = agilicus_api.ChallengesApi(api_client)
    challenge = agilicus_api.Challenge() # Challenge | The challenge to create

    try:
        # create a challenge
        api_response = api_instance.create_challenge(challenge)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChallengesApi->create_challenge: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **challenge** | [**Challenge**](Challenge.md)| The challenge to create | 

### Return type

[**Challenge**](Challenge.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully created the challenge. Depending on whether &#x60;send_now&#x60; was true, it could be waiting for an answer.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_challenge**
> delete_challenge(challenge_id)

Delete the challenge specified by challenge_id

### Example

```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with agilicus_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ChallengesApi(api_client)
    challenge_id = 'AbasaWlLLS' # str | A challenge id found in a path.

    try:
        # Delete the challenge specified by challenge_id
        api_instance.delete_challenge(challenge_id)
    except ApiException as e:
        print("Exception when calling ChallengesApi->delete_challenge: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **challenge_id** | **str**| A challenge id found in a path. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Challenge was deleted |  -  |
**404** | Challenge not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_answer**
> ChallengeAnswer get_answer(challenge_id, challenge_answer, challenge_uid, allowed)

answer a challenge

Checks whether the challenge answer is correct. If the challenge is not accepting answers, or the anwer is incorrect, a failure will be returned. Otherwise, the challenge will be considered answered and the user can log in. 

### Example

```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with agilicus_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ChallengesApi(api_client)
    challenge_id = 'AbasaWlLLS' # str | A challenge id found in a path.
challenge_answer = 'AbasaWlLLS' # str | The answer for the challenge
challenge_uid = 'AbasaWlLLS' # str | The user id for the challenge
allowed = false # bool | Whether the challenge was allowed. If true, then the user can proceed with the login. If false, then the user will be denied their login attempt. Set this to false if the login attempt was not desired. 

    try:
        # answer a challenge
        api_response = api_instance.get_answer(challenge_id, challenge_answer, challenge_uid, allowed)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChallengesApi->get_answer: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **challenge_id** | **str**| A challenge id found in a path. | 
 **challenge_answer** | **str**| The answer for the challenge | 
 **challenge_uid** | **str**| The user id for the challenge | 
 **allowed** | **bool**| Whether the challenge was allowed. If true, then the user can proceed with the login. If false, then the user will be denied their login attempt. Set this to false if the login attempt was not desired.  | 

### Return type

[**ChallengeAnswer**](ChallengeAnswer.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully answered the challenge. The user may now proceed with their login. |  -  |
**400** | The challenge answer failed. No particular reason will be given. |  -  |
**404** | Challenge not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_challenge**
> Challenge get_challenge(challenge_id)

Get the challenge specified by challenge_id

### Example

```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with agilicus_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ChallengesApi(api_client)
    challenge_id = 'AbasaWlLLS' # str | A challenge id found in a path.

    try:
        # Get the challenge specified by challenge_id
        api_response = api_instance.get_challenge(challenge_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChallengesApi->get_challenge: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **challenge_id** | **str**| A challenge id found in a path. | 

### Return type

[**Challenge**](Challenge.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return the challenge by id |  -  |
**404** | Challenge not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_challenge**
> Challenge replace_challenge(challenge_id, challenge)

Replace the challenge specified by challenge_id

### Example

```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with agilicus_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ChallengesApi(api_client)
    challenge_id = 'AbasaWlLLS' # str | A challenge id found in a path.
challenge = agilicus_api.Challenge() # Challenge | The challenge to replace. Note that some fields, such as user_id, cannot be modified.

    try:
        # Replace the challenge specified by challenge_id
        api_response = api_instance.replace_challenge(challenge_id, challenge)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChallengesApi->replace_challenge: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **challenge_id** | **str**| A challenge id found in a path. | 
 **challenge** | [**Challenge**](Challenge.md)| The challenge to replace. Note that some fields, such as user_id, cannot be modified. | 

### Return type

[**Challenge**](Challenge.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The challenge was replaced. The result contains the updated challenge. |  -  |
**404** | Challenge not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

