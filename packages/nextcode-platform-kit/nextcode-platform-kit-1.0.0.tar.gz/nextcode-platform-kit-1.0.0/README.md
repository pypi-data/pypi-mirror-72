# Platform-kit (platkit)

Platform kit is a python library which contains common functionality for Restful Flask Applications maintained by the Platform Services team of Wuxi Nextcode. The python package is called **platkit**

## Getting started

To install the latest release you can do the following:

```bash
$ pip install nextcode-platform-kit
```

Note that there is a low-privilege user embedded into the pip command above and you might want to use another user instead.

If you are working in the platkit source you can clone it into a local folder and then install it in *develop* mode
```bash
$ python setup.py develop
```

## Installing in flask applications
We assume you are using **pipenv** to manage the dependencies un your flask app. You can add platkit into your project by running the following
```
pipenv install nextcode-platform-kit
```

If you are actively developing platkit you can install a developer version with `pipenv install -e /path/to/platform-kit`. Note that currently this will override your Pipfile platkit entry and you must be careful not to check that in. Hopefully we can fix this later.

## Creating a new Flask Service

There is a cookiecutter template for a new flask service which uses platkit. The service has a database dependency and has some example models to get you started.

To create a service repo from the cookiecutter template you can do the following:

```bash
$ pip install cookiecutter
cookiecutter /Users/[myself]/work/platform-kit/service-template --output-dir=/Users/[myself]/work/
```

The script will ask you some questions and then create the service code files with some basic functionality. To initialize your new service you can do the following:
```bash
$ cd ~/work/my-new-service
$ make setup
$ make createdb
$ make test
```
If this runs without issues the service should be good to go and you can start adding your endpoints and models.

You can now run your service with:
```bash
$ make serve
```

Your service should be available at http://127.0.0.1:8080

### Skip the database
You can specify `use_db = n` when cookiecutter is run to skip all references to database. You will need to manually remove the `models/db.py` module if you want but it should not be in your way. Likewise you will want to remove the `migrations` folder and `scripts/createdb.py`.

### Authentication
Your new service will assume that the keycloak service on the platform-dev account will be used for authentication. The public key is saved in the `settings.ini` file that is loaded up when your service starts. If you authenticate against this keycloak instance you can use the access_token against your protected endpoints with `Authorization: Bearer [token]`. We assume you are familiar with the process and will not elaborate on it further in this document.

### Project Structure
A new platkit based flask service assumes the following structure
```
 
 - tests/ # split into folders depending on purpose
  - unittests/
   - ...
  - endpointtests/
   - ...
 - scripts/ # various scripts for managing the project
  - ...
 - migrations/ # alembic migration scripts for flask-db
 - [package_name]/
  - endpoints/ # all flask_restplus endpoints go in here, preferrably split up by endpoint name.
    - ...
  - models/
   - db.py # sql-alchemy models
   - responses.py # flask-restplus response models
  - BUILD_INFO.yml
  - config.py # flask config, read from settings.ini / environment through python-decouple.
```

### Reverse proxy middleware AKA constructing correct URLs behind a reverse-proxy
platkit includes a middleware - `platkit/middleware/reverse_proxied.py` - designed to make flask behave when running behind reverse-proxies.
It works by reading headers forwarded by well-behaved proxies that indicate the path to the
flask service on the proxy.

The middleware can be told to use a different header by setting the following environment variable:
```bash
PLATKIT_PROXY_PREFIX=HTTP_X_NEW_HEADER
```