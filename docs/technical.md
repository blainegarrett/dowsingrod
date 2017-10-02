# Pref Service Technical Documentation

## Microservice Philosophy
The design of this service is to fit the microservice model. That is, this services' sole responsibility is to collect `Preference` data and turn it into `AssocationRules`. Because of this, it does not claim to know anything about the `Items` or `Users` (eg. physical distance between `Items`, if an `Item` still exists, etc). We simply persist the foreign id.

## Environment
Currently, the service is designed to run on Google Cloud. The data is designed to be persisted to the Google Datastore using the ndb api. The python application code is meant to be run on Google App Engine "standard" python environment.

Locally, the service can be run using the Google Cloud SDK. This stubs out many of the services (async task queues, datastore, etc) so that the service can be run on your computer. (See installation instructions).

**Note**: Data persisted to Google Appengine must be manually exported via available REST APIs or remote console.

**Note**: Google Appengine and the Google Datastore are "pay per use" with reasonably high free quotas.

## Project layout
Each core piece of the the project contains three key layers
* **Handlers** - webapp2 handlers that can be interacted with via REST http calls using http "verbs" (GET, PUT, POST, etc). This layer also handles authentication, serving results in a REST format, and handling errors.
* **Services** - The core business logic layer that the `handlers` talk to. These are agnostic of the database implementation and speak in internal "models"
* **Api** - The lowest level logic that interacts with the database implementation. This handles things like transactions, running queries, etc.

Each core piece of the project ideally speaks to each other through the service layer (although rules are meant to be broken). This design allows for the handler layer to be swapped out (eg. for XML format or to use messaging) as well as the api layer to be swapped out (eg. for a SQL backend).

## Testing and QA
Unit tests can be ran via `make unit` on the command line within the main project directory.
Unit test coverage currently is pretty spotty and some time should be dedicated to increasing coverage.

Currently, unit tests and manual QA are the only forms of test coverage.

