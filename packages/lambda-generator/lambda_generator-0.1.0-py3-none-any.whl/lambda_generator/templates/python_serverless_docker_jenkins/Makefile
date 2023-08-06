-include .env
export


PROJECT=project-name
ORG_NAME=organization-name
LINE_LENGTH_VALUE=90

format:
	black --line-length ${LINE_LENGTH_VALUE} .

lint:
	docker build -f dockers/Dockerfile-lint -t ${ORG_NAME}/${PROJECT}:lint .
	docker run -t ${ORG_NAME}/${PROJECT}:lint

test:
	docker build -f dockers/Dockerfile-test -t ${ORG_NAME}/${PROJECT}:test .
	docker run -e SENTRY_URL=${SENTRY_URL} \
    -e EXAMPLE_VARIABLE_ENV=${EXAMPLE_VARIABLE_ENV} \
    -t ${ORG_NAME}/${PROJECT}:test

deploy:
	docker build -f dockers/Dockerfile-deploy -t ${ORG_NAME}/${PROJECT}:deploy .
	docker run -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
		-e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
		-e SENTRY_URL=${SENTRY_URL} \
    -e STAGE=${STAGE} \
    -e EXAMPLE_VARIABLE_ENV=${EXAMPLE_VARIABLE_ENV} \
		-t ${ORG_NAME}/${PROJECT}:deploy
