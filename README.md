# django_vuejs_docker
*This is a demo taks list project written in django, vuejs and powered by docker.*



# Development mode:

This project supports webpack hot reloading for the frontend and the usual development server that django has.
Any change that happens in the frontend it is proxied at the nginx web-server and then served at the browser.
It makes things simplier at the development cycle this way.

In order to run the whole project in development mode you have to do 2 things.
At the root of the repo:
  * docker-compose build --no-cache && docker-compose up
  * Wait for a little bit.
  * Done
 


# Production mode:


Now in the production side you have to follow a slightly different path.
Again at the root of the repo:
  * docker-compose -f docker-compose.prod.yml build --no-cache
  * docker-compose -f docker-compose.yml -f docker-compose.prod.yml
  * Done again !!!
  
  We use the -f flag in order to overide everything at docker-compose.yml
  
