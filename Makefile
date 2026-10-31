build-apigateway-lambda::
	GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -o ./bootstrap ./cmd/apigateway/main.go
	rm -f ./handler.zip
	zip -j ./handler.zip ./bootstrap
