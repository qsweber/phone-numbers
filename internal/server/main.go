package server

import (
	"context"
	"encoding/json"
	"errors"
)

type Request struct {
	Method          string
	Path            string
	Headers         map[string]string
	QueryParameters map[string]string
}

type Response struct {
	StatusCode int
	Body       string
	Headers    map[string]string
}

type Server interface {
	Handle(ctx context.Context, req Request) Response
	Ping() Response
	Match(req Request) Response
}

type ServerImpl struct {
	serviceContext ServiceContext
}

func New(serviceContext ServiceContext) Server {
	return &ServerImpl{
		serviceContext: serviceContext,
	}
}

func (s *ServerImpl) Handle(ctx context.Context, req Request) Response {
	if req.Method == "OPTIONS" {
		return Response{StatusCode: 200, Headers: preflightHeaders()}
	}

	switch req.Path {
	case "/v1/ping", "/api/v0/status":
		return s.Ping()
	case "/v1/match", "/api/v0/match":
		return s.Match(req)
	default:
		return errorResponse(404, errors.New("route not found"))
	}
}

func corsHeaders() map[string]string {
	return map[string]string{
		"Access-Control-Allow-Origin": "*",
		"Cache-Control":               "no-store",
		"Content-Type":                "application/json",
	}
}

func preflightHeaders() map[string]string {
	return map[string]string{
		"Access-Control-Allow-Origin":  "*",
		"Access-Control-Allow-Methods": "GET, OPTIONS",
		"Access-Control-Allow-Headers": "Content-Type",
		"Cache-Control":                "no-store",
	}
}

func jsonResponse(statusCode int, value any) Response {
	body, err := json.Marshal(value)
	if err != nil {
		return errorResponse(500, err)
	}

	return Response{StatusCode: statusCode, Body: string(body), Headers: corsHeaders()}
}

func errorResponse(statusCode int, err error) Response {
	body, marshalErr := json.Marshal(map[string]string{"error": err.Error()})
	if marshalErr != nil {
		return Response{StatusCode: statusCode, Body: `{"error":"failed to marshal error response"}`, Headers: corsHeaders()}
	}

	return Response{StatusCode: statusCode, Body: string(body), Headers: corsHeaders()}
}
