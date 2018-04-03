DOCKER_RUN := docker run -v src:/site/src -e AWS_SECRET_ACCESS_KEY -e AWS_ACCESS_KEY_ID serverlessdaystlv/site

build:
	docker build -t serverlessdaystlv/site .

create-s3-bucket:
	$(DOCKER_RUN) aws s3 mb s3://tlv.serverlessdays.io --region eu-central-1

upload: build
	$(DOCKER_RUN) node node_modules/gulp/bin/gulp.js build; ls; pwd; aws s3 sync dist s3://tlv.serverlessdays.io --acl public-read

local: build
	$(DOCKER_RUN) node node_modules/gulp/bin/gulp.js
