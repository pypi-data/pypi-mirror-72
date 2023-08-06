# MessageEndpoint

A single address on which we can notify a user (e.g. phone#, push context, ...)
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier | [optional] [readonly] 
**created** | **datetime** | Creation time | [optional] [readonly] 
**updated** | **datetime** | Update time | [optional] [readonly] 
**type** | [**MessageEndpointType**](MessageEndpointType.md) |  | [optional] 
**nickname** | **str** | User-supplied name (e.g. My-Yubikey, don&#39;s laptop) | [optional] 
**address** | **str** | Type-specific address info (e.g. phone num, push-context json, ...) | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


