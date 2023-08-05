# IssuerClient

Object describing the properties of an IssuerClient
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier | [optional] [readonly] 
**issuer_id** | **str** | Unique identifier | [optional] [readonly] 
**name** | **str** | issuer client id | 
**secret** | **str** | issuer client secret | [optional] 
**application** | **str** | application associated with client | [optional] 
**org_id** | **str** | org_id associated with client | [optional] 
**restricted_organisations** | **list[str]** | List of organisation IDs which are allowed to authenticate using this client. If a user is not a member of one of these organisations, their authentication attempt will be denied. Note that this list intersects with &#x60;organisation_scope&#x60;. For example, if &#x60;organisation_scope&#x60; is &#x60;here-and-down&#x60; and this list contains two organisations below the current organisation, only those two will be allowed, despite there potentially being more sub organisations. If the list is empty, no restrictions are applied by this field. Note that other restrictions may be applied, such as by &#x60;organisation_scope&#x60;.  | [optional] 
**organisation_scope** | **str** | How to limit which organisations are allowed to authenticate using this client. Note that this interacts with &#x60;restricted_organisations&#x60;: that list, if not empty, further limits the allowed organisations. * &#x60;any&#x60; indicates that there are no restrictions. All organisations served by   the issuer will be allowed to log in using this client. * &#x60;here-only&#x60; indicates that   only the organisation referenced by &#x60;org_id&#x60; may be used. * &#x60;here-and-down&#x60; indicates that the organisation referenced by &#x60;org_id&#x60;   and its children may be used.  | [optional] [default to 'here_only']
**redirects** | **list[str]** | List of redirect uris | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


