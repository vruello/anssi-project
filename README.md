# Windowsploit

This project is educational purposes only. 

## How to use

- Download the docker image (link incoming)

Open a shell : 
- `docker load -i <file.tgz>`
- `docker run -it -p 4444:4444 -p 8888:80 -v ~/path/to/this/repository:/home/root <image-name>`. 
- `msfrpcd -P <secret> -n -f -a 127.0.0.1`

In another shell : 
- `docker ps` : find the container name of the running image. 
- `docker exec -it <container-name> bash` 
- `cd home/root`
- `python manage.py runserver 0.0.0.0:80`

On your local machine, browse on `localhost:8888` and click on `Launch` to set up the listener. 