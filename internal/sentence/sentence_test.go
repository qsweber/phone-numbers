package sentence

import (
	"math/rand"
	"testing"

	"github.com/qsweber/phone-numbers/internal/trie"
	"github.com/qsweber/phone-numbers/internal/words"
)

var dictionary = trie.New(words.Load())

func TestFromNumber(t *testing.T) {
	cases := []struct {
		input    string
		expected string
	}{
		{"2679809273", "copy 80 ward"},
		{"0000000000", "0000000000"},
		{"1800837863", "1800 test me"},
		{"abc1(800)-837-863", "1800 test me"},
		{"abcdef", ""},
		{"22738275", "aardvark"},
		{"2273827522738275", "aardvark aardvark"},
		// notice how it doesn't do "aardvark team ..."
		{"227382758326455466", "aardvark tea million"},
	}

	for _, tc := range cases {
		t.Run(tc.input, func(t *testing.T) {
			actual := FromNumber(dictionary, tc.input)
			if actual != tc.expected {
				t.Errorf("FromNumber(%q) = %q, expected %q", tc.input, actual, tc.expected)
			}
		})
	}
}

func TestFromNumberNeverErrors(t *testing.T) {
	for i := 0; i < 10; i++ {
		digits := make([]byte, 10)
		for j := range digits {
			digits[j] = byte('0' + rand.Intn(10))
		}

		actual := FromNumber(dictionary, string(digits))
		if len(actual) < len(digits) {
			t.Errorf("FromNumber(%q) = %q, expected at least %d characters", digits, actual, len(digits))
		}
	}
}
