package main

import (
	"fmt"

	"github.com/aws/aws-cdk-go/awscdk/v2"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

func NewPhoneNumbersStack(scope constructs.Construct, id string, cfg EnvConfig, props *awscdk.StackProps) awscdk.Stack {
	stack := awscdk.NewStack(scope, jsii.String(id), props)

	projectStackName := "phone-numbers-" + cfg.Env

	role := createBaseRole(stack, projectStackName)

	apigatewayResources := createAPIGatewayResources(stack, projectStackName, cfg, role)

	createCustomDomainResources(stack, cfg)

	awscdk.NewCfnOutput(stack, jsii.String("LambdaName"), &awscdk.CfnOutputProps{
		Value: apigatewayResources.Function.FunctionName(),
	})
	awscdk.NewCfnOutput(stack, jsii.String("InvocationURL"), &awscdk.CfnOutputProps{
		Value: jsii.String(fmt.Sprintf(
			"https://%s.execute-api.%s.amazonaws.com/v1/{message}",
			*apigatewayResources.Api.Ref(),
			cfg.Region,
		)),
	})

	return stack
}
