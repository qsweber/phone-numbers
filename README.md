# Phone Numbers

![CI](https://github.com/qsweber/phone-numbers/actions/workflows/production.yml/badge.svg)

Gives you an easy to remember alphanumeric for your phone number.

## Example

Navigate to this URL:

```
https://phone-numbers-api.quinnweber.com/v1/match?value=1800837863
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

The dictionary (`internal/words/words.txt`) is embedded in the Lambda binary and the Trie is built once per cold start.

## Layout

- `cmd/apigateway/main.go`: AWS Lambda entrypoint behind API Gateway
- `internal/server`: request routing and handlers
- `internal/sentence`: turns a phone number into a sentence of words
- `internal/trie`: the Trie data structure
- `internal/words`: the embedded dictionary
- `cdk`: AWS CDK (Go) infrastructure code

## Endpoints

- `GET /v1/ping`: health check (also served at the legacy `/api/v0/status`)
- `GET /v1/match?value=<phone number>`: returns the best match (also served at the legacy `/api/v0/match`)

## Prerequisites

1. Go 1.25.8+
2. (Optional, for deployment) Node.js 20+, the AWS CDK CLI, and AWS credentials

## Test

```bash
go test ./...
```

## Build Lambda Artifact

```bash
make build-apigateway-lambda
```

This produces:

- bootstrap
- handler.zip

## Deploy With CDK

The `cdk/` directory is a standalone Go module containing a CDK app that defines two stacks,
`phone-numbers-dev` and `phone-numbers-prod`, each targeting `us-west-2`.

Pull requests deploy `phone-numbers-dev` and merges to `master` deploy `phone-numbers-prod`
via GitHub Actions. To deploy by hand:

1. Install the pinned CDK CLI (only needed once):

```bash
cd cdk && npm install
```

2. Build the Lambda artifact (from the repo root) so the CDK app has something to package:

```bash
make build-apigateway-lambda
```

3. Review and deploy a stack:

```bash
cd cdk
npx cdk diff phone-numbers-dev
npx cdk deploy phone-numbers-dev
```

Swap `phone-numbers-dev` for `phone-numbers-prod` to deploy the other environment.

4. Tear down when done:

```bash
npx cdk destroy phone-numbers-dev
```
