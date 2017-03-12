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

#### JSON Body
The body of a POST request must be an array of `PreferenceModel` objects. See `Preference Resource Object` section above.

#### Request
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