package main

import (
	"context"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	"github.com/qsweber/phone-numbers/internal/server"
)

var serviceCtx server.ServiceContext

func init() {
	serviceCtx = server.NewServiceContext()
}

func handler(ctx context.Context, request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	srv := server.New(serviceCtx)
	req := server.Request{
		Method:          request.HTTPMethod,
		Path:            request.Path,
		Headers:         request.Headers,
		QueryParameters: request.QueryStringParameters,
	}

	resp := srv.Handle(ctx, req)

	return events.APIGatewayProxyResponse{
		StatusCode: resp.StatusCode,
		Body:       resp.Body,
		Headers:    resp.Headers,
	}, nil
}

func main() {
	lambda.Start(handler)
}
