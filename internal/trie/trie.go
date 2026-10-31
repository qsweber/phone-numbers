package trie

// Node is a single letter in the trie. Children are stored in a small slice
// rather than a map to keep the memory footprint of the full dictionary low.
type Node struct {
	IsWord   bool
	children []child
}

type child struct {
	letter byte
	node   *Node
}

// Child returns the node for the given letter, or nil if there is none.
func (n *Node) Child(letter byte) *Node {
	for _, c := range n.children {
		if c.letter == letter {
			return c.node
		}
	}

	return nil
}

func (n *Node) childOrCreate(letter byte) *Node {
	if existing := n.Child(letter); existing != nil {
		return existing
	}

	created := &Node{}
	n.children = append(n.children, child{letter: letter, node: created})

	return created
}

type Trie struct {
	Root *Node
}

func New(words []string) *Trie {
	root := &Node{}
	for _, word := range words {
		if word == "" {
			continue
		}

		current := root
		for i := 0; i < len(word); i++ {
			current = current.childOrCreate(word[i])
		}
		current.IsWord = true
	}

	return &Trie{Root: root}
}
