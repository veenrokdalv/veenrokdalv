restart:
	docker build --tag veenrokdalv-backend:dev-latest .
	docker run --rm -p 8080:8000 -v "counter_data:/app/data/" --name veenrokdalv-backend-8080 veenrokdalv-backend:dev-latest

run:
	docker run --rm -p 8080:8000 -v "counter_data:/app/data/" --name veenrokdalv-backend-8080 veenrokdalv-backend:dev-latest