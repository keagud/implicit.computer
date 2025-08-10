#!/bin/bash

ZOLA_VERSION=$(cat zola_version | xargs )
curl -L "https://github.com/getzola/zola/releases/download/v$ZOLA_VERSION/zola-v$ZOLA_VERSION-x86_64-unknown-linux-gnu.tar.gz" | tar xz && ./zola build
