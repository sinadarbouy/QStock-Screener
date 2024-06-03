requirements:
	pip install -r requirements.txt

build:
	docker build -t app:0.1 --load .

run:
	python3 main.py
	

