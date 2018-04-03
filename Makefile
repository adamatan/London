AWS = "docker run -e AWS_SECRET_ACCESS_KEY -e AWS_ACCESS_KEY_ID serverlessdaystlv/site"

build:
	docker build -t serverlessdaystlv/site .

create-s3-bucket:
	docker run -e AWS_SECRET_ACCESS_KEY -e AWS_ACCESS_KEY_ID serverlessdaystlv/site \
	  aws s3 mb s3://tlv.serverlessdays.io --region eu-central-1

upload: build
	docker run -e AWS_SECRET_ACCESS_KEY -e AWS_ACCESS_KEY_ID serverlessdaystlv/site \
	  node node_modules/gulp/bin/gulp.js build; aws s3 sync dist s3://tlv.serverlessdays.io --acl public-read
