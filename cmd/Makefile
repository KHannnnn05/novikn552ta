start_parse:
	cd parser/optlist && python3 -m scrapy crawl main && cd ../..
	python3 parser/suplbiz/main.py
	python3 telegram/sender.py

start_bot:
	python3 telegram/main.py

