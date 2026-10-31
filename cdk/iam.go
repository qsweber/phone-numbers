package main

import (
	"github.com/aws/aws-cdk-go/awscdk/v2/awsiam"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

var assumeRolePolicyDocument = map[string]interface{}{
	"Version": "2012-10-17",
	"Statement": []interface{}{
		map[string]interface{}{
			"Sid":    "",
			"Effect": "Allow",
			"Principal": map[string]interface{}{
				"Service": "lambda.amazonaws.com",
			},
			"Action": "sts:AssumeRole",
		},
	},
}

var logPolicyDocument = map[string]interface{}{
	"Version": "2012-10-17",
	"Statement": []interface{}{
		map[string]interface{}{
			"Effect": "Allow",
			"Action": []interface{}{
				"logs:CreateLogGroup",
				"logs:CreateLogStream",
				"logs:PutLogEvents",
			},
			"Resource": "arn:aws:logs:*:*:*",
		},
	},
}

// createBaseRole builds the Lambda execution role. The function only needs to write logs: the
// dictionary is embedded in the binary, so there is no S3 (or other) access to grant.
func createBaseRole(scope constructs.Construct, projectStackName string) awsiam.CfnRole {
	return awsiam.NewCfnRole(scope, jsii.String("TaskExecRole"), &awsiam.CfnRoleProps{
		RoleName:                 jsii.String(projectStackName + "-task-exec-role"),
		AssumeRolePolicyDocument: assumeRolePolicyDocument,
		Policies: []interface{}{
			&awsiam.CfnRole_PolicyProperty{
				PolicyName:     jsii.String(projectStackName + "-lambda-log-policy"),
				PolicyDocument: logPolicyDocument,
			},
		},
	})
}
