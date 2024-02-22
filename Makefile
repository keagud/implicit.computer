

.PHONY: build run save

build:
	docker build . -t site

save:
	docker build . -t site && docker save site:latest | gzip > site.tar.gz 

run:
	docker build . -t site && docker run -it site:latest sh


