package sentence

import (
	"strings"

	"github.com/qsweber/phone-numbers/internal/trie"
)

var lettersByNumber = map[byte]string{
	'2': "abc",
	'3': "def",
	'4': "ghi",
	'5': "jkl",
	'6': "mno",
	'7': "prs",
	'8': "tuv",
	'9': "wxy",
}

// letterOption is a single digit of the phone number along with the letters
// it can represent.
type letterOption struct {
	digit   byte
	letters string
}

// FromNumber converts a phone number into the most memorable series of words.
func FromNumber(t *trie.Trie, number string) string {
	cleaned := cleanInput(number)

	options := make([]letterOption, len(cleaned))
	for i := 0; i < len(cleaned); i++ {
		letters, ok := lettersByNumber[cleaned[i]]
		if !ok {
			letters = string(cleaned[i])
		}
		options[i] = letterOption{digit: cleaned[i], letters: letters}
	}

	var sb strings.Builder
	lastIsDigit := false
	for _, word := range findCollectionOfLongestWords(t, options) {
		wordIsDigit := isDigits(word)
		if sb.Len() > 0 && !(lastIsDigit && wordIsDigit) {
			sb.WriteByte(' ')
		}
		sb.WriteString(word)
		lastIsDigit = wordIsDigit
	}

	return sb.String()
}

func findLongestWord(node *trie.Node, options []letterOption, wordSoFar, validWordSoFar string) string {
	if len(options) == 0 {
		return validWordSoFar
	}

	best := validWordSoFar
	found := false
	letters := options[0].letters
	for i := 0; i < len(letters); i++ {
		next := node.Child(letters[i])
		if next == nil {
			continue
		}

		word := wordSoFar + string(letters[i])
		valid := validWordSoFar
		if next.IsWord {
			valid = word
		}

		result := findLongestWord(next, options[1:], word, valid)
		// The first longest result wins ties, matching the order of letters.
		if !found || len(result) > len(best) {
			best = result
			found = true
		}
	}

	return best
}

func findCollectionOfLongestWords(t *trie.Trie, options []letterOption) []string {
	if len(options) == 0 {
		return nil
	}

	bestWord := ""
	bestStart := 0
	for start := range options {
		word := findLongestWord(t.Root, options[start:], "", "")
		if len(word) <= 1 {
			word = string(options[start].digit)
		}

		if bestWord == "" || len(word) > len(bestWord) {
			bestWord = word
			bestStart = start
		}
	}

	before := options[:bestStart]
	after := options[bestStart+len(bestWord):]

	result := findCollectionOfLongestWords(t, before)
	result = append(result, bestWord)
	result = append(result, findCollectionOfLongestWords(t, after)...)

	return result
}

func cleanInput(number string) string {
	var sb strings.Builder
	for i := 0; i < len(number); i++ {
		if number[i] >= '0' && number[i] <= '9' {
			sb.WriteByte(number[i])
		}
	}

	return sb.String()
}

func isDigits(s string) bool {
	if s == "" {
		return false
	}
	for i := 0; i < len(s); i++ {
		if s[i] < '0' || s[i] > '9' {
			return false
		}
	}

	return true
}
