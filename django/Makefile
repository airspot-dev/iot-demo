SHELL=/bin/bash
TARGET_IMAGE:=lorenzocampo/django-iot-demo:pre17
NAMESPACE:=iot-demo


all: build push resources


build:
	docker build --no-cache -t ${TARGET_IMAGE} .

migrate:
	docker run --env-file env ${TARGET_IMAGE} sh -c "python manage.py makemigrations && python manage.py migrate"

shell:
	docker run --env-file env -ti ${TARGET_IMAGE} sh

run:
	docker run --env-file env -p 80:8000 ${TARGET_IMAGE}

resources:
	kubectl apply -n ${NAMESPACE} -k k8s/

push:
	docker push ${TARGET_IMAGE}