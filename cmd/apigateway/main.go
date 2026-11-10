package main

import (
	"context"
	"log/slog"
	"os"
	"time"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	"github.com/qsweber/phone-numbers/internal/server"
)

type apiGatewayHandler func(ctx context.Context, request events.APIGatewayV2HTTPRequest) (events.APIGatewayV2HTTPResponse, error)

// newHandler adapts HTTP API (payload format 2.0) events to the server's
// Request/Response types, and logs one JSON line per request. Header names arrive lowercased.
func newHandler(srv server.Server, logger *slog.Logger) apiGatewayHandler {
	return func(ctx context.Context, request events.APIGatewayV2HTTPRequest) (events.APIGatewayV2HTTPResponse, error) {
		start := time.Now()
		resp := handle(ctx, srv, request)

		// Headers and the query string are left out on purpose: the query string carries the
		// caller's phone number.
		logger.InfoContext(ctx, "request",
			"requestId", request.RequestContext.RequestID,
			"method", request.RequestContext.HTTP.Method,
			"path", request.RawPath,
			"status", resp.StatusCode,
			"durationMs", time.Since(start).Milliseconds(),
			"sourceIp", request.RequestContext.HTTP.SourceIP,
			"userAgent", request.RequestContext.HTTP.UserAgent,
		)

		return resp, nil
	}
}

func handle(ctx context.Context, srv server.Server, request events.APIGatewayV2HTTPRequest) events.APIGatewayV2HTTPResponse {
	req := server.Request{
		Method:          request.RequestContext.HTTP.Method,
		Path:            request.RawPath,
		Headers:         request.Headers,
		QueryParameters: request.QueryStringParameters,
	}

	resp := srv.Handle(ctx, req)

	return events.APIGatewayV2HTTPResponse{
		StatusCode: resp.StatusCode,
		Body:       resp.Body,
		Headers:    resp.Headers,
	}
}

func main() {
	serviceCtx := server.NewServiceContext()

	logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
	lambda.Start(newHandler(server.New(serviceCtx), logger))
}
