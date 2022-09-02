# Amun

### Installing the Docker Image
First download the repository locally in your machine. Then, build the image using the following command:
```
docker build -f Amun.docker -t amun-app .
```
To run the docker image, please use the following command:
```
docker run --rm -m 6000M -p 3000:3000 amun-app
```

You can now use the application using [http://localhost:3000/](http://localhost:3000/).




