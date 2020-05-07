FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
RUN apk --update add bash nano
COPY ./ /app
RUN pip install -r /app/requirements.txt
