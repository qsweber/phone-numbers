package server

import (
	"log"
	"time"

	"github.com/qsweber/phone-numbers/internal/trie"
	"github.com/qsweber/phone-numbers/internal/words"
)

type ServiceContext struct {
	Trie *trie.Trie
}

// NewServiceContext builds the dictionary trie from the embedded word list.
// This happens once per Lambda cold start, which replaces the pickled trie the
// Python version cached in S3.
func NewServiceContext() ServiceContext {
	start := time.Now()
	t := trie.New(words.Load())
	log.Printf("Built dictionary trie in %s", time.Since(start))

	return ServiceContext{Trie: t}
}
