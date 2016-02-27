<img src="https://ownpush.com/wp-content/uploads/2016/02/ownpush_128-logoSpelledout.png">

# OTP Demo Server #
## Overview ##
The purpose of this app is to showcase how a developer would integrate <a href="https://ownpush.com" target="_blank">OwnPush</a> into their application for secure, end-to-end encrypted push messaging without Google Services, and as such without a negative drain to the device's battery. The OTP Demo App demonstrates a use case for secure messaging whereby the user is given a One-Time Password (OTP) securely. The OTP Demo Server is part of the OTP Demo App, and can be setup via the following process:
 
## Quick Start

### Basics

1. Activate a virtualenv
1. Install the requirements

### Set Environment Variables

Update *config.py*, and then run:

```sh
$ export APP_SETTINGS="project.config.DevelopmentConfig"
```

or

```sh
$ export APP_SETTINGS="project.config.ProductionConfig"
```

### Create DB

```sh
$ python manage.py create_db
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py create_admin
$ python manage.py create_data
```

### Run the Application

```sh
$ python manage.py runserver
```

### Testing

Without coverage:

```sh
$ python manage.py test
```

With coverage:

```sh
$ python manage.py cov
```