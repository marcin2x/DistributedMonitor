lsof -i:8080 -t | xargs kill -9
lsof -i:8000 -t | xargs kill -9
