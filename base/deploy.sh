#!/bin/bash

if [[ -z "${DOCKER_REGISTRY}" && -z "${KRULES_PROJECT_NAME}" ]]; then
  echo "NOT EXISTS!"
else
  TARGET_IMAGE=${DOCKER_REGISTRY}/base-${KRULES_PROJECT_NAME}
  NAMESPACE=iot-demo

  docker build -t ${TARGET_IMAGE} .
  docker push ${TARGET_IMAGE}
  docker inspect --format='{{index .RepoDigests 0}}' ${TARGET_IMAGE} >.digest
  kubectl apply -n ${NAMESPACE} -k k8s/
  kubectl patch cm config-krules-project -n ${NAMESPACE} -p '{"data": {"imageBase": "$(shell cat .digest)"}}'
fi