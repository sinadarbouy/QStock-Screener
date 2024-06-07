tag = $$(git log -1 --format=%h)
requirements:
	pip install -r requirements.txt

build:
	docker build -t app:$(tag) --load  .

run:
	python3 main.py
	

