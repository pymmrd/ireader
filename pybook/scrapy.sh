#! /bin/sh

for page in $(seq 1 27)
do
 scrapy crawl magic -a start_url=http://www.quanben.com/book4/0/$page/ -o lover_$page.json -t json
done

for page in $(seq 1 16)
do
 scrapy crawl magic -a start_url=http://www.quanben.com/book5/0/$page/ -o time_travel_$page.json -t json
done

for page in $(seq 1 7)
do
 scrapy crawl magic -a start_url=http://www.quanben.com/book6/0/$page/ -o game_$page.json -t json
done

for page in $(seq 1 1)
do
 scrapy crawl magic -a start_url=http://www.quanben.com/book7/0/$page/ -o monster_$page.json -t json
done

for page in $(seq 1 4)
do
 scrapy crawl magic -a start_url=http://www.quanben.com/book8/0/$page/ -o science_$page.json -t json
done

for page in $(seq 1 1)
do
 scrapy crawl magic -a start_url=http://www.quanben.com/book9/0/$page/ -o other_$page.json -t json
done
