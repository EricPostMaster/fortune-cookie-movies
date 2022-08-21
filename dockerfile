FROM python:3.10-slim

COPY requirements.txt /tmp/
COPY ./app /app
WORKDIR "/app"

RUN pip3 install -r /tmp/requirements.txt

ENTRYPOINT [ "python3" ]
CMD [ "fcm_app.py" ]