# Webmark Api
 

[![Build Status](https://travis-ci.com/EricMuller/qcm-rest-api.svg?branch=master)](https://travis-ci.com/EricMuller/qcm-rest-api)[![License](http://img.shields.io/:license-mit-blue.svg)](https://opensource.org/licenses/mit-license.php)[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=com.emu.apps.qcm%3Aqcm-rest-api&metric=alert_status)](https://sonarcloud.io/dashboard/index/com.emu.apps.qcm:qcm-rest-api) [![Known Vulnerabilities](https://snyk.io/test/github/EricMuller/qcm-rest-api/badge.svg)](https://snyk.io/test/github/EricMuller/qcm-rest-api)[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/2888/badge)](https://bestpractices.coreinfrastructure.org/projects/2888) 


Webmark api is a sample Bookmark Rest API .


You can also:
  
  - Create some Bookmarks.
  - Create some Tags.
  - Upload Bookmarks from json files.

### Quality Gate

in progress


### Tech

Webmark Api uses a number of open source projects to work properly:

* [Django] - Create stand-alone backend Spring applications
* [DjangoRest]  - provides repository support for the Java Persistence API (JPA)

### Continuous integration

* [Travis] - Test and Deploy with Confidence [travis-ci](https://travis-ci.com/)

### Installation

Webmark Api requires [Python](https://www.python.org/) v3.6+ to run.

Install the dependencies and devDependencies and start the server.

```sh
$ cd mywebmarks-backend
$source ./env/bin/activate
$python manage.py makemigrations users webmarks_base webmarks_bookmarks webmarks_notes upload storage 
$python manage.py migrate 
$python manage.py loaddata initial_data
$python manage.py runserver
```

Verify the deployment by navigating to your server address in your preferred browser.

```sh
http://127.0.0.1:8000/
```
### windows10 tips

https://www.scivision.co/python-windows-visual-c++-14-required/
https://dimitri.janczak.net/2017/05/20/python-3-6-visual-studio-2017/

<!--#"C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
#python -m pip install -U pip setuptools
#pip install pywin32-->


### Deploy





### Todos

 - Write MORE features
 -
 
### License



Code is under the [MIT Licence ](https://opensource.org/licenses/mit-license.php).





