docker run -d --name mosquitto \
--restart=always \
-u 501:20 \
-p 1883:1883 -p 9001:9001 \
-v /$PWD/data:/mosquitto/data:rw \
-v /$PWD/log:/mosquitto/log:rw \
-v /$PWD/config:/mosquitto/config:rw \
eclipse-mosquitto

docker exec -it mosquitto //bin/sh

https://blog.tarswork.com/zh/post/use-docker-to-set-up-an-mosquitto-mqtt-broker
https://weirenxue.github.io/2021/07/01/mqtt_mosquitto_docker/
https://stackoverflow.com/questions/45971412/docker-volume-format-for-windows
