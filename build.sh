#!/bin/bash


BUILD_DIR=_dirty

mkdir -p $BUILD_DIR

rm -rf $BUILD_DIR/*

cp -r ./*  $BUILD_DIR/ 2> /dev/null

pushd $BUILD_DIR

# get the latest blogroll from the file host
curl -L "https://files.implicit.computer/f/feeds.opml.xml" > /tmp/feeds && mv /tmp/feeds ./static/feeds.opml.xml

# run pre-build script
chmod +x ./scripts/pre_build.py && ./scripts/pre_build.py


# run the site build
ZOLA_VERSION=$(cat zola_version | xargs )
curl -L "https://github.com/getzola/zola/releases/download/v$ZOLA_VERSION/zola-v$ZOLA_VERSION-x86_64-unknown-linux-gnu.tar.gz" | tar xz && ./zola build

# post-build script
chmod +x ./scripts/post_build.py && ./scripts/post_build.py

popd

cp -r $BUILD_DIR/public .


rm -rf $BUILD_DIR
