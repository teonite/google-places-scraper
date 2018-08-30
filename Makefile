.PHONY: build test crawl

build:
        docker-compose build

test: build
        docker-compose run --rm scrapy pytest

crawl: build
        docker-compose run --rm scrapy scrapy crawl GooglePlacesSpider -a cords='53.4284953,14.5494097' -a radius=100 -a api_key=$(api_key)