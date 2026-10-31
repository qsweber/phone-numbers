package server

import (
	"context"
	"encoding/json"
	"testing"

	"github.com/qsweber/phone-numbers/internal/trie"
)

func newTestServer() Server {
	return New(ServiceContext{Trie: trie.New([]string{"test", "me"})})
}

func TestPing(t *testing.T) {
	for _, path := range []string{"/v1/ping", "/api/v0/status"} {
		resp := newTestServer().Handle(context.Background(), Request{Method: "GET", Path: path})
		if resp.StatusCode != 200 {
			t.Fatalf("%s: expected 200, got %d", path, resp.StatusCode)
		}

		var out pingOutput
		if err := json.Unmarshal([]byte(resp.Body), &out); err != nil {
			t.Fatalf("%s: failed to unmarshal body: %v", path, err)
		}
		if !out.Ok {
			t.Errorf("%s: expected ok to be true", path)
		}
	}
}

func TestMatch(t *testing.T) {
	for _, path := range []string{"/v1/match", "/api/v0/match"} {
		resp := newTestServer().Handle(context.Background(), Request{
			Method:          "GET",
			Path:            path,
			QueryParameters: map[string]string{"value": "1800837863"},
		})
		if resp.StatusCode != 200 {
			t.Fatalf("%s: expected 200, got %d", path, resp.StatusCode)
		}

		var out matchOutput
		if err := json.Unmarshal([]byte(resp.Body), &out); err != nil {
			t.Fatalf("%s: failed to unmarshal body: %v", path, err)
		}
		expected := matchOutput{Input: "1800837863", Match: "1800 test me"}
		if out != expected {
			t.Errorf("%s: expected %+v, got %+v", path, expected, out)
		}
	}
}

func TestMatchMissingValue(t *testing.T) {
	resp := newTestServer().Handle(context.Background(), Request{Method: "GET", Path: "/v1/match"})
	if resp.StatusCode != 400 {
		t.Fatalf("expected 400, got %d", resp.StatusCode)
	}
}

func TestNotFound(t *testing.T) {
	resp := newTestServer().Handle(context.Background(), Request{Method: "GET", Path: "/nope"})
	if resp.StatusCode != 404 {
		t.Fatalf("expected 404, got %d", resp.StatusCode)
	}
}
