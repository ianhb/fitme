
#Setup
##Docker Machine
To create a docker machine, first install docker machine. On Windows or OSX install the docker toolbox, on Linux install
docker, docker-compose and docker-machine. Documentation on installation is available [here] (https://docs.docker.com/). Since
docker only runs on the Linux kernel, if running on Windows or OSX, docker machine is required, otherwise docker can be run natively
on Linux.

Once installed, create a docker machine with the boot2docker image using `docker-machine -d virtualbox fitme`.
This creates a docker machine called fitme. To start using fitme as the default docker instance, run `eval "$(docker-machine 
env fitme)"`, which sets environment parameters to use fitme as the default machine to run docker containers on.
To get the ip of the docker-machine, use `docker-machine ip fitme`.

##Docker Compose
For the initial setup, navigate to the root directory of the fitme source and run `docker-compose build`. This downloads
the required images (python and postgresql) and build the source. To create the containers, run `docker-compose up`.
This command also starts the containers, so to continue use Ctrl + C to stop them. Restart the services by using `docker-compose start`.
This starts the services in the background. 

###Linux
To setup the database to use the fitme tables on Linux, use the *run* command from docker-compose to migrate the tables
and to create a super user by running: 

`docker-compose run web python manage.py migrate`

`docker-compose run web python manage.py createsuperuser`

This will create a prompt to create a super user account for managing the database

###Windows (Possibly Mac)
Since docker-compose run isn't supported for Windows, the migration and super user account creation have to be done manually
from inside the container. To connect to a bash instance within the container, run `docker exec -i -t fitme_web_1 bash` and run the 
following commands:


`python manage.py migrate`

`python manage.py createsuperuser`

`exit`

#Updating Fitme
To update Fitme without erasing the data in the database, rebuild the web container with `docker-compose build web` and restart
the service with the new image with `docker-compose restart web`

By default, fitme will run on the server at port 8000 (or whatever is specified in the Dockerfile). To connect to it, point the browser
at the ip of the container (either the docker machine ip or the local ip if no docker-machine is used) at port 8000.

#Fixtures
Included in the repository are fixtures to populate the database. They must be loaded in a particular order to work.
This includes super user account with credentials admin fitmepassword

1. user_init
2. exercise_init
3. supplement_init
4. brands
5. foods_0
6. foods_1
7. exercises
8. supplements
9. servings

