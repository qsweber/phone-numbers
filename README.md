# Phone Numbers

[![Build Status](https://travis-ci.org/qsweber/phone-numbers.svg?branch=master)](https://travis-ci.org/qsweber/phone-numbers) [![Coverage Status](https://coveralls.io/repos/github/qsweber/phone-numbers/badge.svg?branch=master)](https://coveralls.io/github/qsweber/phone-numbers?branch=master)

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
