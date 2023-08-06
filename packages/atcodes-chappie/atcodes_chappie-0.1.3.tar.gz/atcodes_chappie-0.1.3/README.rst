  

# chappie is a module including common tools and utilities for python projects.

**Environment variables**

---------------------

  
***CHAPPIE_AWS_PROFILE***

Connect to an aws account, if not defined, it takes the default account by default.

In the current version it is used to connect aws s3 and sns client (the sns client is not completed yet).

***CHAPPIE_STORAGE_SERVICE***

Define the storage service to use, if one is not indicated, chappie will select the local file system to be used by default.

*Supported services:*
 - **local** (for local file system)
 - **s3** (for aws s3 service)
 
 ***CHAPPIE_STORAGE_BUCKET_NAME***

Define the file container for your application, if not specified, it will create by default a container called: main-storage-bucket-nqhnuwm4u8jakcxu inside a folder called file_manager.

***CHAPPIE_NOTIFIER_SERVICE***

Define the notification service to use, if one is not specified, it will use "[rollbar](https://rollbar.com/)" by default.

Note: the integration configuration must be previously defined in the configuration file of your project.
 
 *Supported services:*
 - **[rollbar](https://rollbar.com/)** (for local file system).
 - **[sentry](https://sentry.io/)** (for aws s3 service).
  
 ***CHAPPIE_BASE_PROJECT_DIR***

This variable is used to create the file container folder at the same level of your project for when using the local file system; if it is not defined, the location of the folder will be at the same level as where the chappie project was installed.


**Installation**

------------

- Create a virtual environment:
    *> virtualenv -p python3 venv*

- Activate the virtual environment:
    *> source venv/bin/activate*
   
- Install the chappie utilities:
    *> pip install atcodes-chappie; pip freeze > requirements.txt*
 
 
 
 
## This project is for free use, if you have any questions please write to admin@atcodes.co
