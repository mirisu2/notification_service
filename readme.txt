docker build -t localhost:5000/notify:v0.0.1 .
docker run -d --rm --name notify -p 5005:80 localhost:5000/notify:v0.0.1
