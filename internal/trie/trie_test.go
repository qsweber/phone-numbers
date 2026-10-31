package trie

import "testing"

func TestNew(t *testing.T) {
	tr := New([]string{"foo", "food", "for"})

	f := tr.Root.Child('f')
	if f == nil || f.IsWord {
		t.Fatalf("expected non-word node for 'f'")
	}
	fo := f.Child('o')
	if fo == nil || fo.IsWord {
		t.Fatalf("expected non-word node for 'fo'")
	}
	foo := fo.Child('o')
	if foo == nil || !foo.IsWord {
		t.Fatalf("expected word node for 'foo'")
	}
	food := foo.Child('d')
	if food == nil || !food.IsWord {
		t.Fatalf("expected word node for 'food'")
	}
	forNode := fo.Child('r')
	if forNode == nil || !forNode.IsWord {
		t.Fatalf("expected word node for 'for'")
	}
	if tr.Root.Child('x') != nil {
		t.Fatalf("expected no node for 'x'")
	}
	if len(tr.Root.children) != 1 || len(fo.children) != 2 || len(food.children) != 0 {
		t.Fatalf("unexpected trie shape")
	}
}
