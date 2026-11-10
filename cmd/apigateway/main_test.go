package main

import (
	"bytes"
	"context"
	"encoding/json"
	"io"
	"log/slog"
	"strings"
	"testing"

	"github.com/aws/aws-lambda-go/events"
	"github.com/qsweber/phone-numbers/internal/server"
)

// fakeServer records the request it receives and returns a fixed response.
type fakeServer struct {
	got  server.Request
	resp server.Response
}

func (f *fakeServer) Handle(_ context.Context, req server.Request) server.Response {
	f.got = req
	return f.resp
}

func (f *fakeServer) Ping() server.Response { return server.Response{} }

func (f *fakeServer) Match(server.Request) server.Response { return server.Response{} }

var discardLogger = slog.New(slog.NewJSONHandler(io.Discard, nil))

func TestHandler_MapsRequestAndResponse(t *testing.T) {
	srv := &fakeServer{resp: server.Response{StatusCode: 200, Body: `{"ok":true}`, Headers: map[string]string{"X-Test": "1"}}}

	resp, err := newHandler(srv, discardLogger)(context.Background(), events.APIGatewayV2HTTPRequest{
		RequestContext: events.APIGatewayV2HTTPRequestContext{
			HTTP: events.APIGatewayV2HTTPRequestContextHTTPDescription{Method: "GET"},
		},
		RawPath:               "/v1/match",
		Headers:               map[string]string{"accept": "application/json"},
		QueryStringParameters: map[string]string{"value": "1800837863"},
	})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	got := srv.got
	if got.Method != "GET" || got.Path != "/v1/match" {
		t.Errorf("request = %+v", got)
	}
	if got.Headers["accept"] != "application/json" || got.QueryParameters["value"] != "1800837863" {
		t.Errorf("headers/query not passed through: %+v", got)
	}
	if resp.StatusCode != 200 || resp.Body != `{"ok":true}` || resp.Headers["X-Test"] != "1" {
		t.Errorf("response = %+v", resp)
	}
}

func TestHandler_LogsOneLinePerRequest(t *testing.T) {
	srv := &fakeServer{resp: server.Response{StatusCode: 404}}
	var buf bytes.Buffer
	logger := slog.New(slog.NewJSONHandler(&buf, nil))

	_, err := newHandler(srv, logger)(context.Background(), events.APIGatewayV2HTTPRequest{
		RequestContext: events.APIGatewayV2HTTPRequestContext{
			RequestID: "req-1",
			HTTP: events.APIGatewayV2HTTPRequestContextHTTPDescription{
				Method:    "GET",
				SourceIP:  "203.0.113.7",
				UserAgent: "scanner/1.0",
			},
		},
		RawPath:               "/v1/nope",
		Headers:               map[string]string{"x-secret": "secret-header"},
		QueryStringParameters: map[string]string{"value": "5551234567"},
	})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	lines := strings.Split(strings.TrimSpace(buf.String()), "\n")
	if len(lines) != 1 {
		t.Fatalf("got %d log lines, want 1: %q", len(lines), buf.String())
	}

	var entry map[string]any
	if err := json.Unmarshal([]byte(lines[0]), &entry); err != nil {
		t.Fatalf("log line is not JSON: %v", err)
	}
	want := map[string]any{
		"msg":       "request",
		"requestId": "req-1",
		"method":    "GET",
		"path":      "/v1/nope",
		"status":    float64(404),
		"sourceIp":  "203.0.113.7",
		"userAgent": "scanner/1.0",
	}
	for key, value := range want {
		if entry[key] != value {
			t.Errorf("%s = %v, want %v", key, entry[key], value)
		}
	}
	if _, ok := entry["durationMs"]; !ok {
		t.Error("durationMs is missing")
	}

	for _, secret := range []string{"secret-header", "5551234567"} {
		if strings.Contains(lines[0], secret) {
			t.Errorf("log line leaks %q: %s", secret, lines[0])
		}
	}
}
