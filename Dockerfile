FROM python:3.9

RUN mkdir /app
WORKDIR /app

COPY src /app/src/
COPY requirements.txt /app/

RUN ls /app/src
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV FLASK_APP "/app/src"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True

EXPOSE 5000

RUN flask routes
RUN flask init-db

ENTRYPOINT ["flask"]
CMD ["run"]
