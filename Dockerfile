FROM rust:1.76-alpine3.18 AS build

WORKDIR build-zola
RUN apk add git && apk add alpine-sdk
RUN git clone https://github.com/getzola/zola.git
WORKDIR /build-zola/zola
RUN git checkout 77c87f5
RUN cargo build --release 

WORKDIR /output
RUN cp /build-zola/zola/target/release/zola  .

FROM joseluisq/static-web-server:2-alpine
COPY --from=build /output/zola /bin/zola
RUN apk add git python3
WORKDIR /site
COPY . .
RUN python3 gitwatch.py
RUN echo "*/5 * * * * /site/gitwatch.py" >> /etc/crontab

ARG port=8080
ENV env_port $port
EXPOSE $port

RUN echo "static-web-server --port $env_port -d ./public" > init.sh

CMD ["./init.sh" ]








