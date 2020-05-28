FROM renci/alpine-data-science:1.0.0

RUN pip3 install --no-cache-dir covid-modeling==0.1.1

COPY api /usr/src/app/api
COPY tx-utils/src /usr/src/app
COPY data /usr/src/app/data

ENTRYPOINT ["gunicorn"]

CMD ["-w", "4", "-b", "0.0.0.0:8080", "api.server:create_app()"]
