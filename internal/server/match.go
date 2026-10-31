package server

import (
	"errors"

	"github.com/qsweber/phone-numbers/internal/sentence"
)

type matchOutput struct {
	Input string `json:"input"`
	Match string `json:"match"`
}

func (s *ServerImpl) Match(req Request) Response {
	value, ok := req.QueryParameters["value"]
	if !ok || value == "" {
		return errorResponse(400, errors.New("missing required query parameter: value"))
	}

	return jsonResponse(200, matchOutput{
		Input: value,
		Match: sentence.FromNumber(s.serviceContext.Trie, value),
	})
}
