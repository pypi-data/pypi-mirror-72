# ChallengeSpec

The specification of an authentication challenge. Contains fields which control how the challenge is made. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**challenge_type** | **str** | The type of challenge to issue. This controls how the user is informed of the challenge, as well as how the challenge can be satisfied. The follow types are supported:   - web_push: a &#x60;web_push&#x60; challenge informs the user of the challenge on every device they have     registered via the web push (rfc8030) mechanism. If the user accepts via the link provided in     the web push, the challenge will be satisfied. The user can deny the challenge via this     mechanism as well.  | 
**user_id** | **str** | Unique identifier | [readonly] 
**send_now** | **bool** | Whether to send the challenge now. If the challenge hasn&#39;t yet been set, setting this to true will send the challenge. If the challenge has been sent, changing this has no effect.  | [optional] [default to False]
**timeout_seconds** | **int** | For how long the system will accept answers for the challenge. After this time, if the challenge is not in the &#x60;challenge_passed&#x60; state, it will transition into the &#x60;timed_out&#x60; state.  | [optional] [default to 600]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


