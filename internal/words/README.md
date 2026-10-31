# Dictionary

`words.txt` is built from [SCOWL](http://wordlist.aspell.net/) (Spell Checker Oriented Word
Lists) version 2020.12.07, size 50, which roughly matches the words a typical spell checker
accepts. Using a frequency-tiered list keeps obscure words out of the matches.

It contains the `english-words` and `american-words` lists at levels 10 through 50, limited to
lowercase `a-z` words (dropping proper names, abbreviations, and words with apostrophes or
accents). Single letters other than `a` and `i`, and letter plurals such as `cs` and `ms`, are
removed.

To regenerate:

```bash
curl -sSL -o scowl.tar.gz https://downloads.sourceforge.net/wordlist/scowl-2020.12.07.tar.gz
tar xzf scowl.tar.gz
cd scowl-2020.12.07/final
cat english-words.{10,20,35,40,50} american-words.{10,20,35,40,50} \
  | iconv -f latin1 -t utf-8 \
  | grep -E '^[a-z]+$' \
  | grep -vxE '[b-hj-z]|cs|es|gs|ks|ls|ms|rs|ts' \
  | sort -u > words.txt
```

SCOWL's copyright and permission notice is in `SCOWL-LICENSE`.
