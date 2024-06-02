#!/bin/sh


zola --root /var/site build \
	--output-dir /var/www/html \
	--base-url / \
	--force
