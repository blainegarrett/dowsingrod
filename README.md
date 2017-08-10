# Divrods Preference Service
Server API for divrods reccomendation engine

## Installation Instructions
Quick start guide to get up and running

#### Dependencies
* python 2.7
* pip python package manager ([installation instructions](https://pip.pypa.io/en/stable/installing/))
* virtualenv ([installation instruction](http://virtualenvwrapper.readthedocs.io/en/latest/install.html))
* gcloud sdk ([installation instructions](https://cloud.google.com/sdk/downloads))
* Also, this is this far test mostly on Mac. Your miliage may vary on other environments

#### Check Out Code
Clone repo from `git@github.com:blainegarrett/dowsingrod.git`
into ~/sites/dowsingrod/ or your preferred directory

#### Install Dependencies
Setup Virtual Env so we don't clutter global python dependencies
`cd ~/sites/dowsingrod/`

`mkvirtualenv dowsingrod -a .`

`make install`


#### Symlink GAE env
Type `which dev_appserver.py ` or `locate dev_appserver.py ` and copy this path.

Open your shell profile (`pico ~/.bash_profile `) and add the following line using your path:

`export GAE_PYTHONPATH='/Users/blainegarrett/google-cloud-sdk/platform/google_appengine'`

Run `source .bash_profile` or open a new shell and type.
`ls $GAE_PYTHONPATH`
`echo $GAE_PYTHONPATH`

If these echo your path, we should be set. Run `make unit` in the project dir to run unit tests.


## Issues/TODOs:
See https://github.com/blainegarrett/dowsingrod/issues and https://github.com/blainegarrett/dowsingrod/projects/1


## REST API Documentation v1.0

### Preference Resource Object
Below is the input and output representation of a `PreferenceModel`


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
            "resource_type": "PreferenceModel", // deprecated - use _meta.resource_type
            "resource_url": "/api/rest/v1.0/preferences/UHJlZmVyZW5jZUVudGl0eR4fNTg2NTYxOTY1NjI3ODAxNg"
        }
```


### AssociationRuleSet Resource Object
A resource representing a run the RuleSet generation based on the PreferenceModels at the time it was run.


Name | Type | Note | Description
-----|------|------|-------
min_confidence | float | *optional* | min confidence used to prune rule set is persisted - defaults to .5
min_support | float | *optional* | min support used to prune rule set that is persisted - defaults to .5
created_timestamp | ISO Datestamp | *required* | Timestamp of when RuleSet was generated
total_rules | int | *required* | Confidence the rule is correct in the range of [0...1]
resource_id | string | *verbose & output only* | resource_id for this `AssociationRuleSet`
resource_url | string | *verbose & output only* | restful url to resource

#### Example Output
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
            "resource_type": "AssociationRuleSetEntity",
            "resource_url": "/api/rest/v1.0/recommendations/QXNzb2NpYXRpb25SdWxlU2V0RW50aXR5Hh81Nzk5MjM2NjQxNzUxMDQw",
            "total_rules": 12
        }
```


### AssociationRule Resource Object
Below is the input and output representation of a `AssociationRule`. Note for `ant` and `con`, the values of the arrays are `rule_item_key` which is in the format of "item id:0 or 1" representing a "like" or "dislike" for item designated by `item_id`


Name | Type | Note | Description
-----|------|------|-------
ant | array | *required* | Rule antecedant list of `rule_item_key` strings described above
con | array | *required* | Rule consequent list of `rule_item_key` strings described above
confidence | float | *required* | Confidence the rule is correct in the range of [0...1]
resource_id | string | *verbose & output only* | resource_id for this `AssociationRule`
resource_url | string | *verbose & output only* | restful url to resource


#### Example Output
```
        {
            "_meta": {
                "is_verbose": true,
                "resource_type": "AssociationRuleModel"
            },
            "ant": [
                "Peanut Butter:1", "Jelly:1"
            ],
            "con": [
                "Bread:1"
            ],
            "confidence": 0.7474747474747475,
            "resource_id": "QXNzb2NpYXRpb25SdWxlRW50aXR5Hh82NTIwNzkxMTQ3NDc5MDQw",
            "resource_type": "AssociationRuleModel",
            "resource_url": "/api/rest/v1.0/recommendations/QXNzb2NpYXRpb25SdWxlRW50aXR5Hh82NTIwNzkxMTQ3NDc5MDQw",
            "rule_key": "bread:1"
        },
```


### List Preferences
This is mostly for debugging. Returned resources are sorted by sync_timestamp DESC
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

### Get a Preference
This is mostly for debugging. Returned resources are sorted by sync_timestamp DESC
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
        "resource_type": "PreferenceModel",
        "resource_url": "/api/rest/v1.0/preferences/UHJlZmVyZW5jZUVudGl0eR4fNTg2NTYxOTY1NjI3ODAxNg"
    },
    "status": 200
}
```

### Bulk Create Preferences (aka Sync)
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
            "resource_id": "UHJlZmVyZW5jZUVudGl0eR4fNTMwMjY2OTcwMjg1NjcwNA",
            "resource_type": "PreferenceModel",
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
            "resource_type": "PreferenceModel",
            "resource_url": "/api/rest/v1.0/preferences/UHJlZmVyZW5jZUVudGl0eR4fNjQyODU2OTYwOTY5OTMyOA",
            "synced_timestamp": "2017-03-12T17:48:33Z",
            "timestamp": null,
            "user_id": "u2"
        }
    ],
    "status": 200
}
```



### Generate a new RuleSet
```
POST /api/rest/v1.0/rulesets
```
#### JSON Body
No body is allowed

#### Query Parameters
min_confidence
min_support


Name | Type | Note | Description
-----|------|------|-------
min_confidence | float | *optional* | min confidence used to prune rule set is persisted - defaults to .5
min_support | float | *optional* | min support used to prune rule set that is persisted - defaults to .5


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
        "resource_id": "QXNzb2NpYXRpb25SdWxlU2V0RW50aXR5Hh81NjA2ODIyMTA2ODkwMjQw",
        "resource_type": "AssociationRuleSetModel",
        "resource_url": "/api/rest/v1.0/rulesets/QXNzb2NpYXRpb25SdWxlU2V0RW50aXR5Hh81NjA2ODIyMTA2ODkwMjQw",
        "total_rules": 12
    },
    "status": 200
}
```

### List RuleSets
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
            "resource_type": "AssociationRuleSetModel",
            "resource_url": "/api/rest/v1.0/rulesets/QXNzb2NpYXRpb25SdWxlU2V0RW50aXR5Hh81Nzk5MjM2NjQxNzUxMDQw",
            "total_rules": null
        },
        ...
    ],
    "status": 200
}
```

###  Get a specific RuleSet
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
        "resource_type": "AssociationRuleSetModel",
        "resource_url": "/api/rest/v1.0/rulesets/QXNzb2NpYXRpb25SdWxlU2V0RW50aXR5Hh81Nzk5MjM2NjQxNzUxMDQw",
        "total_rules": null
    },
    "status": 200
}
```


### Delete Rules
```
DELETE /api/rest/v1.0/sync
```
Deletes all the association rules



### Get Reccomendations

Get Latest Association Rules (by `AssociationRuleSetEntity`'s max create_date). Returned resources are sorted by `confidence` DESC
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
                "Bread:1"
            ],
            "con": [
                "Jelly:1"
            ],
            "confidence": 0.7474747474747475,
            "resource_id": "QXNzb2NpYXRpb25SdWxlRW50aXR5Hh82NTIwNzkxMTQ3NDc5MDQw",
            "resource_type": "AssociationRuleModel",
            "resource_url": "/api/rest/v1.0/recommendations/QXNzb2NpYXRpb25SdWxlRW50aXR5Hh82NTIwNzkxMTQ3NDc5MDQw",
            "rule_key": "bread:1"
        },
        ...
    ],
    "status": 200
}
```


### Get Reccomendations based on a User's session

Get a set of rules from the latest rule set for a given user. This will take into account the user's preferences and return only exact matches for the user based on these preferneces.

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
                "Bread:1"
            ],
            "con": [
                "Jelly:1"
            ],
            "confidence": 0.7474747474747475,
            "resource_id": "QXNzb2NpYXRpb25SdWxlRW50aXR5Hh82NTIwNzkxMTQ3NDc5MDQw",
            "resource_type": "AssociationRuleModel",
            "resource_url": "/api/rest/v1.0/recommendations/QXNzb2NpYXRpb25SdWxlRW50aXR5Hh82NTIwNzkxMTQ3NDc5MDQw",
            "rule_key": "bread:1"
        },
        ...
    ],
    "status": 200
}
```




### Temp process to populate test data
```
PUT /api/rest/v1.0/sync
```
Note: This is mostly for local testing and will polute otherwise valid rules
