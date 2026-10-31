package words

import (
	_ "embed"
	"strings"
)

//go:embed words.txt
var raw string

// Load returns the dictionary of words embedded in the binary.
func Load() []string {
	lines := strings.Split(raw, "\n")
	result := make([]string, 0, len(lines))
	for _, line := range lines {
		word := strings.TrimSpace(line)
		if word != "" {
			result = append(result, word)
		}
	}

	return result
}
