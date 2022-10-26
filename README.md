## Isolated Voltage Source Webserver and GUI

A webserver using FastAPI for interfacing with a UDP-controlled isolated voltage source. The frontend is written in vanilla html and javascript.

<!-- <img style="display: block; margin-left: auto; margin-right: auto; width: 30%" src="GUI.PNG"> -->

<p align="center">
  <img width="300" src="GUI.PNG">
</p>

-- Andrew Mueller 2022

The webserver is packaged using docker. Docker commands to deploy or build the container:


### Stop and remove existing container:
```console
docker rm -f vsource_controll_container
```

### Build command:
```console
docker build -t vsource_controll .
```

run command:
### to make a new container from updated image:
```console
docker run -d --restart unless-stopped --name vsource_controll_container -p 80:80 vsource_controll 
```


### to run existing container
```console
docker run -d -p 80:80 vsource_controll -d --restart unless-stopped
```

Note: if you're changing something like CSS, you might need to rebuild the container with no cache:
```console
docker build -t vsource_controll . --no-cache
```

