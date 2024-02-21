#!/bin/bash
docker build . -t site && docker run -it site:latest sh
