# dowsingrod
Server API for "dowsingrod project" reccomendation engine project


## Installation
Full installation instructions coming soon (https://github.com/blainegarrett/dowsingrod/issues/4)
ls $GAE_PYTHONPATH
echo $GAE_PYTHONPATH


## Issues/TODOs:
See https://github.com/blainegarrett/dowsingrod/issues and https://github.com/blainegarrett/dowsingrod/projects/1


## REST API Documentation v1.0

### Preference Resource Object
Below is the input and output representation of a `PreferenceModel`


Name | Type | Note | Description
------------ | -------------
item_id | string | *required* | identifier of item preference is for
user_id | string | *required* | identifier of user recording the preference, used for calculation "transaction" set
pref | boolean | *required* | true or false of if the user liked or disliked the item
timestamp | ISO Datestamp | *optional* | timestamp of when the preference took place. Useful for when batch syncing preferences
synced_timestamp | ISO Datestamp | *output only* | timestamp when model was persisted
resource_id | string | *output only* | resource_id for this `PreferenceModel`
resource_type | string | *output only* | always `PreferenceModel`
resource_url | string | *output only* | restful url to resource

#### Example Input
```
        {
            "item_id": "item2",
            "pref": false,
            "timestamp": "2017-03-12T16:40:26Z",
            "user_id": "user2",
        }
```
#### Example Output
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

### AssociationRule Resource Object
Below is the input and output representation of a `AssociationRule`. Note for `ant` and `con`, the values of the arrays are `rule_item_key` which is in the format of "<item_id>:<0 or 1>" representing a "like" or "dislike" for item designated by `item_id`


Name | Type | Note | Description
------------ | -------------
ant | array | *required* | Rule antecedant list of `rule_item_key` strings described above
con | array | *required* | Rule consequent list of `rule_item_key` strings described above
confidence | float | *required* | Confidence the rule is correct in the range of [0...1]
resource_id | string | *output only* | resource_id for this `AssociationRule`
resource_type | string | *output only* | always `AssociationRule`
resource_url | string | *output only* | restful url to resource


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
            "resource_url": "/api/rest/v1.0/recommendation/QXNzb2NpYXRpb25SdWxlRW50aXR5Hh82NTIwNzkxMTQ3NDc5MDQw",
            "rule_key": "bread:1"
        },
```


### List Preferences
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



### Generate Rules
```
POST /api/rest/v1.0/sync
```
#### JSON Body
No body is allowed

#### Query Parameters
min_confidence
min_support


Name | Type | Note | Description
------------ | -------------
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
            "resource_url": "/api/rest/v1.0/recommendation/QXNzb2NpYXRpb25SdWxlRW50aXR5Hh82NTIwNzkxMTQ3NDc5MDQw",
            "rule_key": "bread:1"
        },
        ...
    ],
    "status": 200
}
```


### Delete Rules
```
DELETE /api/rest/v1.0/sync
```
Deletes all the association rules



### Get Reccomendations - get Latest Association Rules
```
GET /api/rest/v1.0/recommendation
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
            "resource_url": "/api/rest/v1.0/recommendation/QXNzb2NpYXRpb25SdWxlRW50aXR5Hh82NTIwNzkxMTQ3NDc5MDQw",
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