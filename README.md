# Project Setup

## Project description

***Basic DRF project starter. It includes everything you need to start a project using DRF.Main features are given below***

    1.  Authentication using JWT
    2.  Redis Setup 
    3.  Celery Setup
    4.  RabbitMQ
    5.  Custom Pagination 
    6.  Many helper function
    7.  Error handling 
    8.  Custom permission class
    9.  Dynamic serializer
    10. Useful bash scripts
    11. Data seeders
    12. Test case 
    13. Swagger Documentation 
    14. And More

## Project Architecture

***base directory feature***

    1.  In apis folder you will found custom renderer class. 
        Also find a CustomSwaggerAutoSchema class so that you sectionize your api documentation
        like this  ```swagger_tags = ["Users"]``` in your views.

    2. In cache folder you will find a redis_cache file where you will find few function 
       to set, get, delete from redis
   
    3. In helpers folder you will find a decorators file consist of exception_handler decorator 
       to handle any exception like this ```@method_decorator(exception_handler)```. 
       Here you will also find a email to file which is used to send email using sendgrid. 
       Also there is a file for custom pagination and a utils file for some utility function

    4. In middleware folders you will find two file app_logger which is 
       responsible to show log in terminal and another 
       file auth.py which is responsible to check token is valid.
   
    5. In this folder you will also find some file like models.py consist base model 
       for all others model,  permissions.py consist of few permissions classes, 
       serializers.py for base serializer class.Permission usages : 
    
       permission_classes = (HasRequiredPermissionForMethod,)
       get_permission_required = ['app.permission_name']
       post_permission_required = ['app.permission_name']
    
    6. In scripts folder you will find few helper scripts to run fresh migrations, create db, initial database with seeders.
    
    7. In seeders folder you write script to generate fake data. Also there is an example how you can dot it.
    
    8. In tests folder you can write unit test. You can flow the given example.
    
    9. In accounts app you will find pre made api for authentication like login, logout, profile update, reset password, refresh token and more


## How to run this project using virtual ENV

    1. Create virtual env python3 -m venv ./venv
    2. Active venv source venv/bin/activate
    3. Install dependencies pip install -r requirements.txt
    4. Enter src directory cd src
    5. Run bash scripts/export-env.sh in src folder
    6. Run python manage.py makemigrations in src folder
    7. Run python manage.py migrate in src folder
