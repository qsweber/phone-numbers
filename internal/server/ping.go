package server

import (
	"time"
)

type pingOutput struct {
	Ok        bool   `json:"ok"`
	Timestamp string `json:"timestamp"`
}

func (s *ServerImpl) Ping() Response {
	return jsonResponse(200, pingOutput{
		Ok:        true,
		Timestamp: time.Now().UTC().Format(time.RFC3339),
	})
}
