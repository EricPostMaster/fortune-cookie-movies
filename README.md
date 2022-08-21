# What if fortune cookies were filled with movie plots?

You've probably wondered that many times. Or maybe you haven't - that's fine too.

This repo is a project currently in progress to create some sort of application using spaCy to transform brief movie synopses into fortune cookie statements and, hopefully, a web app that will be fun to use.

Thanks for visiting!

## Running the web app

There are a few ways to run this app, all shown below. Once you run one of the commands below the app should be available at [http://localhost:8050](http://localhost:8050).

### With Docker Compose

Getting started with Docker Compose is probably the easiest, assuming you have Docker and Docker Compose installed already. If you do then just run the below:

```
docker-compose up -d
```

The image should be automatically built as part of the above command. To build the image without starting the service you can run the following:

```
docker-compose build
```

To stop the docker-compose application run the below:

```
docker-compose down
```

### With Docker

If you have Docker installed, but not Docker Compose, that's okay. First we need to build the image:

```
docker build --tag fcm-app .
```

Once the image is built you can run the app with the below Docker command:

```
docker run -p 8050:8050 fcm-app
```

#### Possible errors
```
subprocess.CalledProcessError: Command '['/usr/bin/java', '-version']' returned non-zero exit status 1.
```
- If you're on MacOS, make sure you have a Java installed.

```
OSError: [E050] Can't find model 'en_core_web_trf'. It doesn't seem to be a Python package or a valid path to a data directory.
```
- `python -m spacy download en_core_web_trf`  
or
- `python3 -m spacy download en_core_web_trf`