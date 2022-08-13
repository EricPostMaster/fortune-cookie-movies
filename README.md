# What if fortune cookies were filled with movie plots?

You've probably wondered that many times. Or maybe you haven't - that's fine too.

This repo is a project currently in progress to create some sort of application using spaCy to transform brief movie synopses into fortune cookie statements and, hopefully, a web app that will be fun to use.

Thanks for visiting!

## Running the web app
Make sure you're in `fcm_dashApp/` and run `python fcm_app.py`

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