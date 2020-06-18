# Phone Numbers

![CI](https://github.com/qsweber/phone-numbers/workflows/CI/badge.svg) ![Test Coverage](https://img.shields.io/badge/tests-86%25-yellow) ![Type Coverage](https://img.shields.io/badge/types-67%25-red)

Gives you an easy to remember alphanumeric for your phone number.

## Example

Navigate to this URL:

```
https://tmia51806i.execute-api.us-west-2.amazonaws.com/production/api/v0/match?value=1800837863
```

And you should get this output:

```
{
  "input": "1800837863",
  "match": "1800 test me"
}
```

## How it works

It first transforms a dictionary into a [Trie](https://en.wikipedia.org/wiki/Trie). Then it transforms your phone number into all possible letter combinations. Finally, it uses the Trie to determine the best representation of your phone number as a series of words.
