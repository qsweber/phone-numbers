package main

import (
	"github.com/aws/aws-cdk-go/awscdk/v2"
	"github.com/aws/jsii-runtime-go"
)

// EnvConfig holds the per-stack (dev/prod) settings.
type EnvConfig struct {
	Env     string
	Account string
	Region  string
	ZoneID  string

	// Custom domain for the API Gateway (e.g. "dev-phone-numbers-api.quinnweber.com").
	ApiDomainName string
}

func main() {
	app := awscdk.NewApp(nil)

	account := "120356305272"

	NewPhoneNumbersStack(app, "phone-numbers-dev", EnvConfig{
		Env:           "dev",
		Account:       account,
		Region:        "us-west-2",
		ZoneID:        "Z07290422T6PHN4TKVNW0",
		ApiDomainName: "dev-phone-numbers-api.quinnweber.com",
	}, &awscdk.StackProps{
		Env: &awscdk.Environment{
			Account: jsii.String(account),
			Region:  jsii.String("us-west-2"),
		},
	})

	NewPhoneNumbersStack(app, "phone-numbers-prod", EnvConfig{
		Env:           "prod",
		Account:       account,
		Region:        "us-west-2",
		ZoneID:        "Z07290422T6PHN4TKVNW0",
		ApiDomainName: "phone-numbers-api.quinnweber.com",
	}, &awscdk.StackProps{
		Env: &awscdk.Environment{
			Account: jsii.String(account),
			Region:  jsii.String("us-west-2"),
		},
	})

	app.Synth(nil)
}
