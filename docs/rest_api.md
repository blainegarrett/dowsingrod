
# REST API Documentation v1.0

* Resource Objects
 - [Preference](#PreferenceResourceObject)
 - [AssociationRuleSet](#AssociationRuleSetObject)
 - [AssociationRule](#AssociationRuleObject)
 - [Item](#ItemObject)
 - [Transaction/User](#TransactionObject)
* Common REST Handlers
 - [GET /api/rest/v1.0/preferences](#get_preferences) Get a paginated list of recent preferences
 - [POST /api/rest/v1.0/preferences](#post_preferences) - Write one or more preferences
 - [POST /api/rest/v1.0/rulesets](#post_rulesets) - Generate a new RuleSet based on the current snapshot of preferences
 - [GET /api/rest/v1.0/recommendations](#get_recommendations) - Get a list of association rules from the default rule set
 - AuthUser - Needs documentation yet!

## Rest Resource Objects
There are a few key resource objects described below: Preference, AssociationRuleSet, AssociationRule, Item and Transaction.


### <a name="PreferenceResourceObject"></a> Preference Resource Object
A representation of a `PreferenceModel` which stores an individial users/session's like or dislike of a specific item.


Name | Type | Note | Description
-----| ---- | -----| --------
item_id | string | *required* | identifier of item preference is for
user_id | string | *required* | identifier of user recording the preference, used for calculation "transaction" set
pref | boolean | *required* | true or false of if the user liked or disliked the item
timestamp | ISO Datestamp | *optional* | timestamp of when the preference took place. Useful for when batch syncing preferences
synced_timestamp | ISO Datestamp | *output only* | timestamp when model was persisted
resource_id | string | *verbose & output only* | resource_id for this `PreferenceModel`
resource_url | string | *verbose & output only* | restful url to resource

#### Example Input
```
        {
            "item_id": "item2",
            "pref": false,
            "timestamp": "2017-03-12T16:40:26Z",
            "user_id": "user2",
        }
```
#### Example Output (verbose)
```
        {
            "_meta": {
                "is_verbose": true,
                "resource_type": "PreferenceModel"
            },
            "item_id": "item2",
            "pref": false,
            "synced_timestamp": "2017-03-12T16:40:26Z",
            "timestamp": "2017-03-12T16:40:26Z",
            "user_id": "user2",
            "resource_id": "UHJlZmVyZW5jZUVudGl0eR4fNTg2NTYxOTY1NjI3ODAxNg",
            "resource_url": "/api/rest/v1.0/preferences/UHJlZmVyZW5jZUVudGl0eR4fNTg2NTYxOTY1NjI3ODAxNg"
        }
```


### <a name="AssociationRuleSetObject"></a>  AssociationRuleSet Resource Object
A resource representing a run the RuleSet generation based on the PreferenceModels at the time it was run.


Name | Type | Note | Description
-----|------|------|-------
min_confidence | float | *optional* | min confidence used to prune rule set is persisted - defaults to .5
min_support | float | *optional* | min support used to prune rule set that is persisted - defaults to .5
created_timestamp | ISO Datestamp | *required* | Timestamp of when RuleSet was generated
total_rules | int | *required* | Confidence the rule is correct in the range of [0...1]
is_default  | bool | * output only * | If the ruleset is the default one served up
resource_id | string | *verbose & output only* | resource_id for this `AssociationRuleSet`
resource_url | string | *verbose & output only* | restful url to resource

#### Example Output (verbose)
```
        {
            "_meta": {
                "is_verbose": true,
                "resource_type": "AssociationRuleSetEntity"
            },
            "created_timestamp": "2017-03-17T04:50:45Z",
            "min_confidence": 0.345,
            "min_support": 0.45,
            "resource_id": "QXNzb2NpYXRpb25SdWxlU2V0RW50aXR5Hh81Nzk5MjM2NjQxNzUxMDQw",
            "resource_url": "/api/rest/v1.0/recommendations/QXNzb2NpYXRpb25SdWxlU2V0RW50aXR5Hh81Nzk5MjM2NjQxNzUxMDQw",
            "is_default": false,
            "total_rules": 12
        }
```


### <a name="AssociationRuleObject"></a> AssociationRule Resource Object
Below is the output representation of a `AssociationRule`. Note for `ant` and `con`, the values of the arrays are `rule_item_key` which is in the format of "item id:0 or 1" representing a "like" or "dislike" for item designated by `item_id`


Name | Type | Note | Description
-----|------|------|-------
ant | array | *required* | Rule antecedant list of `rule_item_key` strings described above
con | array | *required* | Rule consequent list of `rule_item_key` strings described above
confidence | float | *required* | Confidence the rule is correct in the range of [0...1]
resource_id | string | *verbose & output only* | resource_id for this `AssociationRule`
resource_url | string | *verbose & output only* | restful url to resource


#### Example Output (verbose)
```
        {
            "_meta": {
                "is_verbose": true,
                "resource_type": "AssociationRuleModel"
            },
            "ant": [
                "1163:1", "802:0"
            ],
            "con": [
                "3908:1"
            ],
            "confidence": 0.7474747474747475,
            "resource_id": "QXNzb2NpYXRpb25SdWxlRW50aXR5Hh82NTIwNzkxMTQ3NDc5MDQw",
            "resource_url": "/api/rest/v1.0/recommendations/QXNzb2NpYXRpb25SdWxlRW50aXR5Hh82NTIwNzkxMTQ3NDc5MDQw",
            "rule_key": "3908:1"
        },
```

### <a name="ItemObject"></a> Item Resource Object
An item that has been preferenced. Keeps track of total preferences.

Name | Type | Note | Description
-----|------|------|-------
item_id | str | *output only* | String ID of the item preferenced
created_timestamp | ISO Datestamp | *output only* | timestamp of when the first preference took place.
latest_timestamp | ISO Datestamp | *output only* | timestamp of when the last preference took place.
total_dislikes | int | *output only* | # of dislike preferences
total_likes | int | *output only* | # of like preferences
total_dislikes | int | *output only* | Total # of preferences

### Exmple Output (verbose)
```
        {
            "_meta": {
                "is_verbose": true,
                "resource_type": "ItemModel"
            },
            "created_timestamp": "2017-09-13T16:49:26Z",
            "item_id": "31412",
            "latest_timestamp": "2017-09-13T17:07:40Z",
            "resource_id": "UHJlZmVyZW5jZUl0ZW1FbnRpdHkeMzE0MTI",
            "resource_url": "/api/rest/v1.0/items/UHJlZmVyZW5jZUl0ZW1FbnRpdHkeMzE0MTI",
            "total_dislikes": 5,
            "total_likes": 1,
            "total_preferences": 6
        },
```

### <a name="TransactionObject"></a> Transaction/User Resource Object
A representation of the user/session and all their preferences. This acts as a "transaction" set of data. There
will be one entry per unique user_id passed when creating preferences.

Name | Type | Note | Description
-----|------|------|-------
user_id | str | *output only* | String ID of the user/session
created_timestamp | ISO Datestamp | *output only* | timestamp of when the first preference took place.
latest_timestamp | ISO Datestamp | *output only* | timestamp of when the last preference took place.
rule_item_ids | string list | *output only* | A list of preference keys ("item id:0 or 1" representing a "like" or "dislike")
total_dislikes | int | *output only* | # of dislike preferences
total_likes | int | *output only* | # of like preferences
total_dislikes | int | *output only* | Total # of preferences

### Exmple Output (verbose)
```
        {
            "_meta": {
                "is_verbose": true,
                "resource_type": "TransactionModel"
            },
            "created_timestamp": "2017-09-13T17:07:49Z",
            "latest_timestamp": "2017-09-13T17:07:53Z",
            "resource_id": "UHJlZmVyZW5jZVRyYW5zYWN0aW9uRW50aXR5HmFkbWluX3N1cnZleV85LjMxNjg4NDA0MjY2MzA2Ng",
            "resource_url": "/api/rest/v1.0/transactions/UHJlZmVyZW5jZVRyYW5zYWN0aW9uRW50aXR5HmFkbWluX3N1cnZleV85LjMxNjg4NDA0MjY2MzA2Ng",
            "rule_item_ids": [
                "111619:1",
                "802:1",
                "3908:0",
                "1163:1",
                "589:1"
            ],
            "total_dislikes": 1,
            "total_likes": 4,
            "total_preferences": 5,
            "user_id": "user_1234"
        }
```


## Rest Handlers
### Required Headers
REST requests return JSON as their response body. When making a request, the header `Content-Type: application/json` is required.

All handlers unless otherwise noted require an `Authentication: Basic <token>` header where `<token>` is a base 64 encoded string in the format `username:password`
Users can be managed via the administrative panel.

### Structure of JSON Response
The requested data will be returned in the `results` property of the json body. This may be a list of requested objects (for a collection/list endpoint) or a single requested object (for resource endpoints)
Every response will also have a `status` property containing the HTTP status (matching the request itself) as well as a `messages` list property which will contain the traceback if there is an exception.

An example of the raw json response body for a collection/list endpoint can be seen below
```
{
    "cursor": "bGVFbnRpdHkYgICAgIDi9AsMGAAgAQ==",
    "messages": [ null ],
    "more": false,
    "results": [... //list of result objects],
    "status": 200
}
```

** A Note On Pagination **

The properties `more` and `cursor` only applied to supported list/collection endpoints and designate if there are more objects than those retrieved. The `cursor` property can be passed to the same base url as a query parameter to retrieve the next set of results.


An example of the raw json response body for a resource endpoint can be seen below
```
{
    "messages": [ null ],
    "results": { single response object },
    "status": 200
}
```


### Optional Url Params
The following query parameters are supported by all handlers

Name | Type | Default | Description
-----|------|------|-------
pretty | bool | false | Format the response json content into an easily readable indented format - useful for debugging. Default false helps save bandwidth.
verbose | bool | false | Return all properties of the returned objects including those flagged as verbose_only = True. Default false helps save bandwidth.

### Pagination of Collection/List Handlers
All collection/list handlers (unless otherwise stated) support pagination.

The following optional input query parameters are supported.

Name | Type | Default | Description
-----|------|------|-------
cursor | string | None | A string encoded with the query params from the previous request's response json body. (See above)
limit | int | None | Number of results per request to fetch.



###  <a name="get_preferences"></a> List Preferences
Collection endpoint to return Preference resource objects (sorted by sync_timestamp DESC)
```
GET /api/rest/v1.0/preferences
```

#### Response
```
{
    "results": [
        {
            "_meta": {
                "is_verbose": true,
                "resource_type": "PreferenceModel"
            },
            "item_id": "item2",
            "pref": false,
            "synced_timestamp": "2017-03-12T16:40:26Z",
            "timestamp": "2017-03-12T16:40:26Z",
            "user_id": "user2",
            "resource_id": "UHJlZmVyZW5jZUVudGl0eR4fNTg2NTYxOTY1NjI3ODAxNg",
            "resource_type": "PreferenceModel",
            "resource_url": "/api/rest/v1.0/preferences/UHJlZmVyZW5jZUVudGl0eR4fNTg2NTYxOTY1NjI3ODAxNg"
        }
        ...
    ],
    "cursor": "bGVFbnRpdHkYgICAgIDi9AsMGAAgAQ==",
    "messages": [ null ],
    "more": true,
    "status": 200
}
```

### <a name="get_preferences_resource"></a> Get a Specfic Preference (verbose)
Resource endpoint to return a specific Preference Resource
```
GET /api/rest/v1.0/preferences/:resource_id?verbose=true
```

#### Response
```
{
    "messages": [
        null
    ],
    "results": {
        "_meta": {
            "is_verbose": true,
            "resource_type": "PreferenceModel"
        },
        "item_id": "item2",
        "pref": false,
        "synced_timestamp": "2017-03-12T16:40:26Z",
        "timestamp": "2017-03-12T16:40:26Z",
        "user_id": "user2",
        "resource_id": "UHJlZmVyZW5jZUVudGl0eR4fNTg2NTYxOTY1NjI3ODAxNg",
        "resource_url": "/api/rest/v1.0/preferences/UHJlZmVyZW5jZUVudGl0eR4fNTg2NTYxOTY1NjI3ODAxNg"
    },
    "status": 200
}
```

### <a name="post_preferences"></a> Bulk Write Preferences
Persist one or more Preference resource objects. Multiple input objects are supported to allow async updating from survey data or the device after being offline.

```
POST /api/rest/v1.0/preferences
```

#### Request Body
The body of a POST request must be an JSON encoded array of `PreferenceModel` objects. See `Preference Resource Object` section above.


```
[
    {
        "item_id": "i1",
        "user_id": "u1",
        "pref": true
    },
    {
        "item_id": "i2",
        "user_id": "u2",
        "pref": false}
]
```

#### Response
```
{
    "messages": [
        null
    ],
    "results": [
        {
            "_meta": {
                "is_verbose": true,
                "resource_type": "PreferenceModel"
            },
            "item_id": "i1",
            "pref": true,
            "resource_url": "/api/rest/v1.0/preferences/UHJlZmVyZW5jZUVudGl0eR4fNTMwMjY2OTcwMjg1NjcwNA",
            "synced_timestamp": "2017-03-12T17:48:33Z",
            "timestamp": null,
            "user_id": "u1"
        },
        {
            "_meta": {
                "is_verbose": true,
                "resource_type": "PreferenceModel"
            },
            "item_id": "i2",
            "pref": false,
            "resource_id": "UHJlZmVyZW5jZUVudGl0eR4fNjQyODU2OTYwOTY5OTMyOA",
            "resource_url": "/api/rest/v1.0/preferences/UHJlZmVyZW5jZUVudGl0eR4fNjQyODU2OTYwOTY5OTMyOA",
            "synced_timestamp": "2017-03-12T17:48:33Z",
            "timestamp": null,
            "user_id": "u2"
        }
    ],
    "status": 200
}
```



### <a name="post_rulesets"></a> Generate a new RuleSet
```
POST /api/rest/v1.0/rulesets
```
#### JSON Body
No body is allowed

#### Query Parameters

Name | Type | Note | Description
-----|------|------|-------
min_confidence | float | *optional* | min confidence used to prune rule set is persisted - defaults to .5
min_support | float | *optional* | min support used to prune rule set that is persisted - defaults to .5
is_default  | boolean |  *optional* | if the ruleset should be made default

#### Request Body
```
No Body is allowed

```
#### Response Body
The response body results are a list of `AssociationRule Resource Object`
```
{
    "messages": [
        null
    ],
    "results": {
        "_meta": {
            "is_verbose": true,
            "resource_type": "AssociationRuleSetModel"
        },
        "created_timestamp": "2017-03-17T15:54:45Z",
        "min_confidence": 0.345,
        "min_support": 0.45,
        "is_default": false,
        "resource_id": "QXNzb2NpYXRpb25SdWxlU2V0RW50aXR5Hh81NjA2ODIyMTA2ODkwMjQw",
        "resource_url": "/api/rest/v1.0/rulesets/QXNzb2NpYXRpb25SdWxlU2V0RW50aXR5Hh81NjA2ODIyMTA2ODkwMjQw",
        "total_rules": 12
    },
    "status": 200
}
```

### <a name="get_rulesets"></a> List RuleSets
```
GET /api/rest/v1.0/rulesets
```

#### Response Body
```
{
    "messages": [
        null
    ],
    "results": [
        {
            "_meta": {
                "is_verbose": true,
                "resource_type": "AssociationRuleSetModel"
            },
            "created_timestamp": "2017-03-17T04:50:45Z",
            "min_confidence": 0.345,
            "min_support": 0.45,
            "resource_id": "QXNzb2NpYXRpb25SdWxlU2V0RW50aXR5Hh81Nzk5MjM2NjQxNzUxMDQw",
            "is_default": false,
            "resource_url": "/api/rest/v1.0/rulesets/QXNzb2NpYXRpb25SdWxlU2V0RW50aXR5Hh81Nzk5MjM2NjQxNzUxMDQw",
            "total_rules": null
        },
        ...
    ],
    "status": 200
}
```

###  <a name="post_rulesets_resource_id"></a> Get a specific RuleSet
```
GET /api/rest/v1.0/rulesets/:ruleset_id
```

#### Response Body
```
{
    "messages": [
        null
    ],
    "results": {
        "_meta": {
            "is_verbose": true,
            "resource_type": "AssociationRuleSetModel"
        },
        "created_timestamp": "2017-03-17T04:50:45Z",
        "min_confidence": 0.345,
        "min_support": 0.45,
        "resource_id": "QXNzb2NpYXRpb25SdWxlU2V0RW50aXR5Hh81Nzk5MjM2NjQxNzUxMDQw",
        "is_default": false,
        "resource_url": "/api/rest/v1.0/rulesets/QXNzb2NpYXRpb25SdWxlU2V0RW50aXR5Hh81Nzk5MjM2NjQxNzUxMDQw",
        "total_rules": null
    },
    "status": 200
}
```


### <a name="get_recommendations"></a> Get Reccomendations

Get default AssociationSet's Rules. Returned resources are sorted by `confidence` DESC
```
GET /api/rest/v1.0/recommendations
```

Get Association Rules for a given `AssociationRuleSetEntity` based on its resource_id
```
GET /api/rest/v1.0/recommendations?ruleset_id=:resource_id
```

#### Response Body
The response body results are a list of `AssociationRule Resource Object`
```
{
    "messages": [
        null
    ],
    "results": [
        {
            "_meta": {
                "is_verbose": true,
                "resource_type": "AssociationRuleModel"
            },
            "ant": [
                "1163:1", "802:0"
            ],
            "con": [
                "3908:1"
            ],
            "confidence": 0.7474747474747475,
            "resource_id": "QXNzb2NpYXRpb25SdWxlRW50aXR5Hh82NTIwNzkxMTQ3NDc5MDQw",
            "resource_url": "/api/rest/v1.0/recommendations/QXNzb2NpYXRpb25SdWxlRW50aXR5Hh82NTIwNzkxMTQ3NDc5MDQw",
            "rule_key": "3908:1"
        },
        ...
    ],
    "status": 200
}
```


### Get Reccomendations based on a User's session

Get a set of rules from the latest rule set for a given user. This will take into account the user's preferences and return only exact matches for the user based on these preferneces.
*This is experimental and not in use*
```
GET /api/rest/v1.0/recommendations/:user_id
```

#### Response Body
The response body results are a list of `AssociationRule Resource Object`
```
{
    "messages": [
        null
    ],
    "results": [
        {
            "_meta": {
                "is_verbose": true,
                "resource_type": "AssociationRuleModel"
            },
            "ant": [
                "1163:1", "802:0"
            ],
            "con": [
                "3908:1"
            ],
            "confidence": 0.7474747474747475,
            "resource_id": "QXNzb2NpYXRpb25SdWxlRW50aXR5Hh82NTIwNzkxMTQ3NDc5MDQw",
            "resource_type": "AssociationRuleModel",
            "resource_url": "/api/rest/v1.0/recommendations/QXNzb2NpYXRpb25SdWxlRW50aXR5Hh82NTIwNzkxMTQ3NDc5MDQw",
            "rule_key": "3908:1"
        },
        ...
    ],
    "status": 200
}
```



### <a name="get_transactions"></a> Get Transaction/User/Sessions
```
GET /api/rest/v1.0/transactions
```
Get a set of transaction/user/session data

#### Response Body
```
{
    "cursor": "CmMKHgoRY3JlYXRlZF90aW1lc3RhbXASCQi57pKgrZ7WAhI9ahRkZXZ-cHJlZi1zZXJ2aWNlLWRldnIlCxIbUHJlZmVyZW5jZVRyYW5zYWN0aW9uRW50aXR5IgRjYXJsDBgAIAE=",
    "messages": [
        null
    ],
    "more": false,
    "results": [
        {
            "_meta": {
                "is_verbose": true,
                "resource_type": "TransactionModel"
            },
            "created_timestamp": "2017-09-13T17:07:49Z",
            "latest_timestamp": "2017-09-13T17:07:53Z",
            "resource_id": "UHJlZmVyZW5jZVRyYW5zYWN0aW9uRW50aXR5HmFkbWluX3N1cnZleV85LjMxNjg4NDA0MjY2MzA2Ng",
            "rule_item_ids": [
                "111619:1",
                "802:1",
                "3908:0",
                "1163:1",
                "589:1"
            ],
            "total_dislikes": 1,
            "total_likes": 4,
            "total_preferences": 5,
            "user_id": "admin_survey_9.316884042663066"
        },
        ...
    ]
}

```


### <a name="get_items"></a> Get Preferenced Items
```
GET /api/rest/v1.0/items
```
Get a list of previously preferenced items


```
GET /api/rest/v1.0/items?items=item_1,item2,item3...
```
Get a list of previously preferenced items by a comma separated list of item_ids
Note: Pagination/cursor is not supported as a query param in conjunction with items query param with .


#### Response Body
```
{
    "cursor": "ClsKHgoRY3JlYXRlZF90aW1lc3RhbXASCQjtysD_rJ7WAhI1ahRkZXZ-cHJlZi1zZXJ2aWNlLWRldnIdCxIUUHJlZmVyZW5jZUl0ZW1FbnRpdHkiA2pqagwYACAB",
    "messages": [
        null
    ],
    "more": false,
    "results": [
        {
            "_meta": {
                "is_verbose": true,
                "resource_type": "ItemModel"
            },
            "created_timestamp": "2017-09-13T16:49:26Z",
            "item_id": "31412",
            "latest_timestamp": "2017-09-13T17:07:40Z",
            "resource_id": "UHJlZmVyZW5jZUl0ZW1FbnRpdHkeMzE0MTI",
            "total_dislikes": 5,
            "total_likes": 1,
            "total_preferences": 6
        },
        ...
    ]
}

```
