
# Installation Instructions
Quick start guide to get up and running.

#### Dependencies
* python 2.7
* pip python package manager ([installation instructions](https://pip.pypa.io/en/stable/installing/))
* virtualenv ([installation instruction](http://virtualenvwrapper.readthedocs.io/en/latest/install.html))
* gcloud sdk ([installation instructions](https://cloud.google.com/sdk/downloads))
* Also, this only been tested on Mac. Your mileage may vary on other environments

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

`export GAE_PYTHONPATH='/Users/blainegarrett/google-cloud-sdk/platform/google_appengine'` or the directory you installed the gcloud sdk to

Run `source .bash_profile` or open a new shell and type.
`ls $GAE_PYTHONPATH`
`echo $GAE_PYTHONPATH`

If these echo your path, we should be set. Run `make unit` in the project dir to run unit tests.
Enter `make run` to run the service locally. By default the service will run at http://localhost:9090

### Running Unit Tests
In the root project directory enter `make run`

## Issues/TODOs:
See https://github.com/divrods/pref-service/issues and https://github.com/divrods/pref-service/projects/1

