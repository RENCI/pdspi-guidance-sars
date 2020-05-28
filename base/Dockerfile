FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apk update
RUN apk add --no-cache --upgrade bash openssh curl ca-certificates openssl htop g++ make wget rsync build-base libpng-dev \
freetype-dev libexecinfo-dev openblas-dev libgomp lapack-dev libgcc libquadmath musl-dev libgfortran
RUN pip3 install --no-cache-dir flask gevent==1.4.0 gunicorn==19.9.0 connexion[swagger-ui] oslash numpy==1.17.3
RUN pip3 install --no-cache-dir pandas==1.0.1 scipy==1.3.1 cython scikit-learn==0.22.1
