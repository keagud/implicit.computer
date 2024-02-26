FROM rust:1.76-alpine3.18 AS build

# download and build zola from source
WORKDIR /build-zola
RUN apk add git alpine-sdk curl coreutils openssl libressl-dev musl-dev 
RUN curl -L https://github.com/getzola/zola/archive/refs/tags/v0.18.0.tar.gz -o zola.tar.gz
RUN mkdir zola
RUN tar xzf zola.tar.gz -C ./zola --strip-components=1

WORKDIR /build-zola/zola
RUN cargo update
RUN cargo fetch --target x86_64-unknown-linux-musl
RUN cargo build --release 

WORKDIR /output
RUN cp  /build-zola/zola/target/release/zola .

# the actual runtime environment
FROM joseluisq/static-web-server:2-alpine
COPY --from=build /output/zola /bin/zola
RUN apk add git python3 busybox-openrc
WORKDIR /site
COPY . .

RUN chmod +x /site/entrypoint.sh
RUN python3 gitwatch.py

# set up cron to listen for updates every minute
RUN echo "* * * * * /site/gitwatch.py" > /opt/cronjob && \
  chmod 0644 /opt/cronjob && \
  crontab /opt/cronjob


ARG port=8080
ENV env_port $port
EXPOSE $port

CMD ["/site/entrypoint.sh" ]








