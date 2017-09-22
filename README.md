# DivRods Preference Service
Server API for divrods reccomendation engine

## Installation Instructions
Quick start guide to get up and running.

#### Dependencies
* python 2.7
* pip python package manager ([installation instructions](https://pip.pypa.io/en/stable/installing/))
* virtualenv ([installation instruction](http://virtualenvwrapper.readthedocs.io/en/latest/install.html))
* gcloud sdk ([installation instructions](https://cloud.google.com/sdk/downloads))
* Also, this only been tested on Mac. Your miliage may vary on other environments

#### Check Out Code
Clone repo from `git@github.com:divrods/pref-service.git`
into ~/sites/dowsingrod/ or your preferred directory

#### Install Dependencies
Setup Virtual Env so we don't clutter global python dependencies
`cd ~/sites/divrods/pref_service`

`mkvirtualenv divrods_pref_service -a .`

`make install`


#### Symlink GAE env
Type `which dev_appserver.py ` or `locate dev_appserver.py ` and copy this path.

Open your shell profile (`pico ~/.bash_profile `) and add the following line using your path:

`export GAE_PYTHONPATH='/Users/blainegarrett/google-cloud-sdk/platform/google_appengine'` or the directory you installed to

Run `source .bash_profile` or open a new shell and type.
`ls $GAE_PYTHONPATH`
`echo $GAE_PYTHONPATH`

If these echo your path, we should be set. Run `make unit` in the project dir to run unit tests.
Enter `make run` to run the service locally. By default the service will run at http://localhost:9090

## Issues/TODOs:
See https://github.com/divrods/pref-service/issues and https://github.com/divrods/pref-service/projects/1


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

###  <a name="get_preferences"></a> List Preferences
This is mostly for debugging and admin UI. Returned resources are sorted by sync_timestamp DESC
```
GET /api/rest/v1.0/preferences
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
    "status": 200
}
```

### <a name="get_preferences_resource"></a>  Get a Preference (verbose)
This is mostly for debugging.
```
GET /api/rest/v1.0/preferences/:resource_id
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

### <a name="post_preferences"></a> Bulk Create Preferences (aka Sync)
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


### <a name="delete_rulesets"></a> Delete Rules
```
DELETE /api/rest/v1.0/sync
```
Deletes all the association rules



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
