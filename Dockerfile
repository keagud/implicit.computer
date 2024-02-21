FROM rust:1.76-alpine3.19 AS build

WORKDIR build-zola
RUN apk add git && apk add alpine-sdk
RUN git clone https://github.com/getzola/zola.git
WORKDIR /build-zola/zola
RUN git checkout 77c87f5
RUN cargo build --release 

WORKDIR /output
RUN cp /build-zola/zola/target/release/zola  .


FROM python:3.11-alpine3.19 
COPY --from=build /output/zola /bin/zola
RUN apk add git
WORKDIR /site
COPY . .




