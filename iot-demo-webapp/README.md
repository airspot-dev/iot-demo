# iot-demo-webapp

> A Vue.js project

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# run unit tests
npm run unit

# run e2e tests
npm run e2e

# run all tests
npm test
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).


docker build -t <username>/iot-web-app .
docker push <usernam>/iot-web-app .
replace deployment image in k8s.yaml
kubectl apply -f k8s.yaml

kubectl port-forward svc/iot-web-app 3000:80
go to http://127.0.0.1:3000
