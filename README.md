# Tasklist Project
*This is a demo task list project written in django, vuejs and powered by docker.*



# Development mode:

This project supports webpack hot reloading for the frontend and the usual development server that django has.
Any change that happens in the frontend it is proxied at the nginx web-server and then served at the browser.
It makes things simplier at the development cycle this way.

In order to run the whole project in development mode you have to do 2 things.
At the root of the repo:
  * docker-compose build --no-cache && docker-compose up
  * Wait for a little bit.
  * Done
 
Once the project is up and running you have full control at developing.
You can make any change at the source code of Django and it will be loaded immediately.

Last but not least, you can take advantage of the hot-reload that Webpack has.
So whatever change you make at the frontend, it has an immediate impact after the browser
autoreloads!!!

You can create a **Superuser** account in dev mode by checking the box "*are you a superuser*"
when you sign up. No need to put the command python manage.py createsuperuser on terminal.


# Production mode:


Now in the production side you have to follow a slightly different path.
Again at the root of the repo:
  * docker-compose -f docker-compose.prod.yml build --no-cache
  * docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
  * Done
  
  We use the -f flag in order to overide everything at docker-compose.yml
  
# Basic Structure

* ###  Backend
         This is the django application. There are no surprises in this point.
* ### Frontend
         This is the frontend application as it states. Everything that we care about developement is
         located at the src folder. In both production and developement mode whatever change there has 
         to be done should live in this folder. In addition it is preferred each Django application
         to have a corresponding directory inside the src folder of the Frontend directory
         e.g. 


              ├── frontend
              │   ├── login
              |
              ├── backend
              │   ├── login
* ### Config
        In this directory for now lives the Nginx configuration. We need this configuration to overide the 
        default configuration Nginx has.
        

        
              
