# Image2Map4BTA
converts images to BTA/Beta 1.7.3 (maybe?)'s map.dat format

## Running the backend with docker  
to build the docker image, run  
`docker build -t image2map4bta .`  
then to start it, you can either run it like a regular docker image with port 8000 forwarded or you can use this docker compose  
```
version: "2.0"

services:
  image2map4bta:
    restart: always
    image: image2map4bta
    deploy:
      resources:
        limits:
          memory: 256M
    ports:
      - 8000:8000
```

## Running the backend on bare metal  
go into backend/ and run `pip3 install -r requirements.txt`  
after this you can run `gunicorn -w 2 -b 0.0.0.0:8000 app:app` to start it  

## Using the application  
if running locally: load up the index.html file in your browser.  
if running publically: add index.html as a url on your web server (you may need to change the location of the API inside of the HTML if you're running them on different machines).
