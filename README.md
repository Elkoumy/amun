# Amun

### Installing the Docker Image
First download the repository locally in your machine. Then, build the image using the following command:
```
sudo docker build -f Amun.docker -t amun-app .
```
To run the docker image, please use the following command:
```
sudo docker run --rm -p 3000:3000 amun-app
```

You can now use the application using [http://localhost:3000/](http://localhost:3000/).




