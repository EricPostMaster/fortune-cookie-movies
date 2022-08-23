# Fortune Cookie Movies :fortune_cookie::film_projector::popcorn:

**Question:** What if fortune cookies were filled with movie plots where you were the main character???

**Answer:** They'd be way cooler!

## How it started:

One day I was looking for interesting uses of Natural Language Processing (NLP) and happened upon Alex Reben's [AI Misfortunes](https://areben.com/project/a-i-misfortunes/) project. If you haven't seen it, he trained a neural network on thousands of fortune cookies, and now it writes mysterious and often hilarious one-liners that are even sold as wall art! :fortune_cookie::arrow_right::framed_picture:

I thought, "Hmm... I wonder if I could turn that around and turn something that isn't a fortune cookie and into a fortune cookie??" :thinking: Movie plots are nice, short statements that summarize a story that will unfold, and people are generally pretty familiar with popular movie plots, so it seemed like a perfect place to start!

Thus, Fortune Cookie Movies was born. :film_projector::arrow_right::fortune_cookie:


## How it's going:

Try out the [Fortune Cookie Movies app](http://http://3.17.184.0:8050/) yourself! Grab some extra buttery popcorn and test your movie knowledge with a fortune cookie movie quiz or tempt fate with a random movie fortune. Adventure awaits! 

Here's what the app looks like:

<img src="https://github.com/EricPostMaster/fortune-cookie-movies/blob/main/fortune_cookie_movies_demo.gif" 
alt="Web app demo GIF" width="500" border="10" />


## How it works:

If you've read this far, you probably want to know what's under the hood. If not, you're about to hear about it anyway!

Essentially, the repo is broken into three parts: retrieving the data, transforming the data, and the web application.

### Retrieving the data

Data is pulled from IMDb using [imdb-api](https://www.imdb-api.com), which at the time of this writing is free to use up to 100 calls per day. If you're starting from scratch, the script will take an initial movie ID as a seed, and then it will populate the dataset from there using similar movies returned in the JSON payload.

### Transforming the data

The current script uses the [spaCy English language transformer pipeline](https://spacy.io/models/en#en_core_web_trf). I tried using the small pipeline to get started, and while it saves a lot of memory, performance is just so much better with the transformer model. The movie plots are transformed and saved ahead of time. I then used [Tortus](https://pypi.org/project/tortus/) package to annotate the plots as Good, Okay, or Bad to decide which ones would be served up to users. The initial app only shows those that were tagged as Good, but Okay fortunes are still intelligible.

### Web application

The app is built on Plotly Dash. It is Dockerized and pushed to AWS Elastic Container Registry. If you're interested in doing something similar, you can follow [this _excellent_ tutorial](https://towardsdatascience.com/how-to-use-docker-to-deploy-a-dashboard-app-on-aws-8df5fb322708) from Melvin Varughese.


## Contribute!

This app exists because cool people contributed a bit of their time and expertise to make it a reality. You are welcome to submit ideas and improvements by creating issues and pull requests on this repo!

Contributors:
* [Jay Seabrum](https://github.com/xjseabrum)
* [Teresa Behr](https://github.com/teresabehr)
* [Michael Long](https://github.com/michael-long88)
* [Caleb Keller](https://github.com/wrathagom)
* [Eric Sims (that's me)](https://github.com/EricPostMaster)

### Running the web app

There are a few ways to run this app, all shown below. Once you run one of the commands below the app should be available at [http://localhost:8050](http://localhost:8050).

#### With Docker Compose

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

#### With Docker

If you have Docker installed, but not Docker Compose, that's okay. First we need to build the image:

```
docker build --tag fcm-app .
```

Once the image is built you can run the app with the below Docker command:

```
docker run -p 8050:8050 fcm-app
```

##### Possible errors
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
