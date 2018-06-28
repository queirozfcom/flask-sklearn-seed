flask-sklearn-seed
==============================

This is a **full** template for building a simple flask-based API and server that serves a trained Scikit-learn model.

Additionaly:

- API and code-level tests

- Logging

- Error handling

- CLI for training the model

## Quickstart

    TODO finishthis

- git clone

- create virtualenv, activate virtualenv

- install requirements-prod

- start the server

## Using the app

- Training via the CLI

    - To train a model: `$ python -m app.models.train_model <path/to/training_set.csv> <version-number>`

- Tests

    - To run utils tests: `$ python -m app.tests.utils_tests`

    - To run API tests: `$ python -m app.tests.web_tests`

- Starting the server

    ```
    $ python -m app.app
     * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
    ```

## Code Organization

This is how this project's code is structured.

Loosely based on [Queirozf.com: How to Structure Software Projects: Python Examples](http://queirozf.com/entries/how-to-structure-software-projects-python-example)
and [Cookie Cutter Data Science](https://drivendata.github.io/cookiecutter-data-science/)

```
.
│
├── README.md                                 <----- this file
│
├── app
│   ├── app.py                                <----- main project file. contains routes and initialization code
│   │
│   ├── settings.py
│   │
│   ├── helpers                               <----- helpers contain helper code that is SPECIFIC to this application
│   │   ├── features.py                              they are placed here so as not to overly pollute the business logic
│   │   ├── files.py                                 with scaffolding code.
│   │   └── validation.py
│   │
│   ├── models                                <----- code for training models
│   │   └── train_model.py
│   │
│   └── utils                                 <----- utils contain helper code that is NOT SPECIFIC to this application,
│       └── files.py                                i.e. it could be extracted and used elsewhere
│
├── data                                      <----- data files, intermediate representation, if needed.
│   ├── interim
│   ├── processed
│   └── raw
│       └── training_set.csv
│
├── logs                                      <----- logs folder
│   ├── application.log
│
├── notebooks                                 <----- jupyter notebooks for data exploration and analyses
│   └── view-data.ipynb
│
├── requirements-dev.txt                      <----- packages required to DEVELOP this project (train model, notebooks, tests, CLI commands)
├── requirements-prod.txt                     <----- packages required to DEPLOY this project (only serves the API)
│
├── tests                                     <----- test code
│   ├── utils_tests.py
│   └── web_tests.py
│
├── trained-models                            <------ trained models (serialized) are kept here
│   ├── trained-model-v0.p
│   ├── trained-model-v1.p
│   └── ...
│
└── venv3                                     <------ python virtualenv
```

## API Docs

### Healthcheck

A simple healthcheck, to be used for monitoring (e.g. in AWS Elastic Beanstalk) a given model version.

**Example: Correct Request, valid version**

```
REQUEST
GET /v0/healthcheck
RESPONSE 200
OK
```

**Example: Correct Request, invalid version**

```
REQUEST
GET /v31254/healthcheck
RESPONSE 200
Not OK
```

### Predict

Returns a prediction, calculated by a previously trained model, whose version is `<version>`.

**Example: Correct Request**

```
REQUEST
POST /v0/predict
{
	"id": "19826478126",
	"score_3": 100.0,
	"score_4": -0.414120,
	"score_5": 0.2131,
	"score_6": -123.2
}
RESPONSE 200
{
    "id": "19826478126",
    "prediction": 0.345
}
```

**Example: Model version not found**

```
REQUEST
POST /v43287/predict
{
	"id": "19826478126",
	"score_3": 100.0,
	"score_4": -0.414120,
	"score_5": 0.2131,
	"score_6": -123.2
}
RESPONSE 404
{
    "message": "Trained model version 'v43287' was not found."
}
```

**Example: Invalid request arguments**

```
REQUEST
POST /v0/predict
{
	"id": "19826478126",
	"score_3": 100.0,
	"score_6": -123.2
}
RESPONSE 400
{
    "message": "Missing keys: 'score_4', 'score_5'"
}
```


### Other info

- Logging

   Logging is needed for keeping track of how people use your app (collect usage metrics) and to help diagnose errors
   in case something goes wrong.

   I've used an external package (`concurrent-log-handler`) because the default `RotatingFileHandler` does not support
   compression of old log files. This is to make sure logging itself doesn't cause problems due to lack of disk space.

- Caching

   There are a couple of caching mechanisms for flask (e.g. https://github.com/sh4nks/flask-caching) but, since
   Logistic Regression is an eager learning method (i.e. inference is quite fast because most of the work is done at training
   time), it didn't seem to be worth the extra complexity.

   Maybe if you are using lazy methods (such as k-NN), caching would be more useful.
