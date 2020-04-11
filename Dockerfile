FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apk --no-cache add gcc musl-dev
RUN pip3 install --no-cache-dir flask gevent==1.4.0 gunicorn==19.9.0 connexion[swagger-ui] oslash

COPY api /usr/src/app/api
COPY tx-utils/src /usr/src/app

ENTRYPOINT ["gunicorn"]

CMD ["-w", "4", "-b", "0.0.0.0:8080", "api.server:create_app()"]

