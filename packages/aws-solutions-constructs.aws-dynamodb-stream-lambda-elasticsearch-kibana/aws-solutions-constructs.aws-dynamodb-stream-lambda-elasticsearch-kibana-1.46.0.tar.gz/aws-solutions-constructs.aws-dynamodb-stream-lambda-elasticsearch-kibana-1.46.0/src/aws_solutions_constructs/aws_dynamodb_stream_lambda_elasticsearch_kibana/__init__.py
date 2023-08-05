"""
# aws-dynamodb-stream-lambda-elasticsearch-kibana module

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> All classes are under active development and subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

| **Reference Documentation**:| <span style="font-weight: normal">https://docs.aws.amazon.com/solutions/latest/constructs/</span>|
|:-------------|:-------------|

<div style="height:8px"></div>

| **Language**     | **Package**        |
|:-------------|-----------------|
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_dynamodb_stream_elasticsearch_kibana`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-dynamodb-stream-lambda-elasticsearch-kibana`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.dynamodbstreamlambdaelasticsearchkibana`|

This AWS Solutions Construct implements Amazon DynamoDB table with stream, AWS Lambda function and Amazon Elasticsearch Service with the least privileged permissions.

Here is a minimal deployable pattern definition:

```javascript
const { DynamoDBStreamToLambdaToElasticSearchAndKibana, DynamoDBStreamToLambdaToElasticSearchAndKibanaProps } = require('@aws-solutions-constructs/aws-dynamodb-stream-lambda-elasticsearch-kibana');

const props: DynamoDBStreamToLambdaToElasticSearchAndKibanaProps = {
    deployLambda: true,
    lambdaFunctionProps: {
        code: lambda.Code.asset(`${__dirname}/lambda`),
        runtime: lambda.Runtime.NODEJS_12_X,
        handler: 'index.handler'
    },
    domainName: 'test-domain'
};

new DynamoDBStreamToLambdaToElasticSearchAndKibana(stack, 'test-dynamodb-stream-lambda-elasticsearch-kibana', props);
```

## Initializer

```text
new DynamoDBStreamToLambdaToElasticSearchAndKibana(scope: Construct, id: string, props: DynamoDBStreamToLambdaToElasticSearchAndKibanaProps);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`DynamoDBStreamToLambdaToElasticSearchAndKibanaProps`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|deployLambda|`boolean`|Whether to create a new Lambda function or use an existing Lambda function|
|existingLambdaObj?|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|Existing instance of Lambda Function object|
|lambdaFunctionProps?|[`lambda.FunctionProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.FunctionProps.html)|Optional user provided props to override the default props for Lambda function|
|dynamoTableProps?|[`dynamodb.TableProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-dynamodb.TableProps.html)|Optional user provided props to override the default props for DynamoDB Table|
|dynamoEventSourceProps?|[`aws-lambda-event-sources.DynamoEventSourceProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda-event-sources.DynamoEventSourceProps.html)|Optional user provided props to override the default props for DynamoDB Event Source|
|esDomainProps?|[`elasticsearch.CfnDomainProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-elasticsearch.CfnDomainProps.html)|Optional user provided props to override the default props for the Elasticsearch Service|
|domainName|`string`|Domain name for the Cognito and the Elasticsearch Service|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|dynamoTable|[`dynamodb.Table`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-dynamodb.Table.html)|Returns an instance of dynamodb.Table created by the construct|
|lambdaFunction|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|Returns an instance of lambda.Function created by the construct|
|userPool|[`cognito.UserPool`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cognito.UserPool.html)|Returns an instance of cognito.UserPool created by the construct|
|userPoolClient|[`cognito.UserPoolClient`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cognito.UserPoolClient.html)|Returns an instance of cognito.UserPoolClient created by the construct|
|identityPool|[`cognito.CfnIdentityPool`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cognito.CfnIdentityPool.html)|Returns an instance of cognito.CfnIdentityPool created by the construct|
|elasticsearchDomain|[`elasticsearch.CfnDomain`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-elasticsearch.CfnDomain.html)|Returns an instance of elasticsearch.CfnDomain created by the construct|
|cloudwatchAlarms|[`cloudwatch.Alarm[]`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cloudwatch.Alarm.html)|Returns a list of cloudwatch.Alarm created by the construct|

## Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

### Amazon DynamoDB Table

* Set the billing mode for DynamoDB Table to On-Demand (Pay per request)
* Enable server-side encryption for DynamoDB Table using AWS managed KMS Key
* Creates a partition key called 'id' for DynamoDB Table
* Retain the Table when deleting the CloudFormation stack

### AWS Lambda Function

* Configure least privilege access IAM role for Lambda function
* Enable reusing connections with Keep-Alive for NodeJs Lambda function

### Amazon Cognito

* Set password policy for User Pools
* Enforce the advanced security mode for User Pools

### Amazon Elasticsearch Service

* Deploy best practices CloudWatch Alarms for the Elasticsearch Domain
* Secure the Kibana dashboard access with Cognito User Pools
* Enable server-side encryption for Elasticsearch Domain using AWS managed KMS Key
* Enable node-to-node encryption for Elasticsearch Domain
* Configure the cluster for the Amazon ES domain

## Architecture

![Architecture Diagram](architecture.png)

---


© Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *

import aws_cdk.aws_cloudwatch
import aws_cdk.aws_cognito
import aws_cdk.aws_dynamodb
import aws_cdk.aws_elasticsearch
import aws_cdk.aws_lambda
import aws_cdk.aws_lambda_event_sources
import aws_cdk.core


class DynamoDBStreamToLambdaToElasticSearchAndKibana(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-solutions-constructs/aws-dynamodb-stream-lambda-elasticsearch-kibana.DynamoDBStreamToLambdaToElasticSearchAndKibana"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, deploy_lambda: bool, domain_name: str, dynamo_event_source_props: typing.Optional[aws_cdk.aws_lambda_event_sources.DynamoEventSourceProps]=None, dynamo_table_props: typing.Optional[aws_cdk.aws_dynamodb.TableProps]=None, es_domain_props: typing.Optional[aws_cdk.aws_elasticsearch.CfnDomainProps]=None, existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function]=None, lambda_function_props: typing.Optional[aws_cdk.aws_lambda.FunctionProps]=None) -> None:
        """
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param deploy_lambda: Whether to create a new lambda function or use an existing lambda function. If set to false, you must provide a lambda function object as ``existingObj`` Default: - true
        :param domain_name: Cognito & ES Domain Name. Default: - None
        :param dynamo_event_source_props: Optional user provided props to override the default props. Default: - Default props are used
        :param dynamo_table_props: Optional user provided props to override the default props. Default: - Default props are used
        :param es_domain_props: Optional user provided props to override the default props for the API Gateway. Default: - Default props are used
        :param existing_lambda_obj: Existing instance of Lambda Function object. If ``deploy`` is set to false only then this property is required Default: - None
        :param lambda_function_props: Optional user provided props to override the default props. If ``deploy`` is set to true only then this property is required Default: - Default props are used

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Constructs a new instance of the LambdaToDynamoDB class.
        """
        props = DynamoDBStreamToLambdaToElasticSearchAndKibanaProps(deploy_lambda=deploy_lambda, domain_name=domain_name, dynamo_event_source_props=dynamo_event_source_props, dynamo_table_props=dynamo_table_props, es_domain_props=es_domain_props, existing_lambda_obj=existing_lambda_obj, lambda_function_props=lambda_function_props)

        jsii.create(DynamoDBStreamToLambdaToElasticSearchAndKibana, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="cloudwatchAlarms")
    def cloudwatch_alarms(self) -> typing.List[aws_cdk.aws_cloudwatch.Alarm]:
        return jsii.get(self, "cloudwatchAlarms")

    @builtins.property
    @jsii.member(jsii_name="dynamoTable")
    def dynamo_table(self) -> aws_cdk.aws_dynamodb.Table:
        return jsii.get(self, "dynamoTable")

    @builtins.property
    @jsii.member(jsii_name="elasticsearchDomain")
    def elasticsearch_domain(self) -> aws_cdk.aws_elasticsearch.CfnDomain:
        return jsii.get(self, "elasticsearchDomain")

    @builtins.property
    @jsii.member(jsii_name="identityPool")
    def identity_pool(self) -> aws_cdk.aws_cognito.CfnIdentityPool:
        return jsii.get(self, "identityPool")

    @builtins.property
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> aws_cdk.aws_lambda.Function:
        return jsii.get(self, "lambdaFunction")

    @builtins.property
    @jsii.member(jsii_name="userPool")
    def user_pool(self) -> aws_cdk.aws_cognito.UserPool:
        return jsii.get(self, "userPool")

    @builtins.property
    @jsii.member(jsii_name="userPoolClient")
    def user_pool_client(self) -> aws_cdk.aws_cognito.UserPoolClient:
        return jsii.get(self, "userPoolClient")


@jsii.data_type(jsii_type="@aws-solutions-constructs/aws-dynamodb-stream-lambda-elasticsearch-kibana.DynamoDBStreamToLambdaToElasticSearchAndKibanaProps", jsii_struct_bases=[], name_mapping={'deploy_lambda': 'deployLambda', 'domain_name': 'domainName', 'dynamo_event_source_props': 'dynamoEventSourceProps', 'dynamo_table_props': 'dynamoTableProps', 'es_domain_props': 'esDomainProps', 'existing_lambda_obj': 'existingLambdaObj', 'lambda_function_props': 'lambdaFunctionProps'})
class DynamoDBStreamToLambdaToElasticSearchAndKibanaProps():
    def __init__(self, *, deploy_lambda: bool, domain_name: str, dynamo_event_source_props: typing.Optional[aws_cdk.aws_lambda_event_sources.DynamoEventSourceProps]=None, dynamo_table_props: typing.Optional[aws_cdk.aws_dynamodb.TableProps]=None, es_domain_props: typing.Optional[aws_cdk.aws_elasticsearch.CfnDomainProps]=None, existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function]=None, lambda_function_props: typing.Optional[aws_cdk.aws_lambda.FunctionProps]=None) -> None:
        """
        :param deploy_lambda: Whether to create a new lambda function or use an existing lambda function. If set to false, you must provide a lambda function object as ``existingObj`` Default: - true
        :param domain_name: Cognito & ES Domain Name. Default: - None
        :param dynamo_event_source_props: Optional user provided props to override the default props. Default: - Default props are used
        :param dynamo_table_props: Optional user provided props to override the default props. Default: - Default props are used
        :param es_domain_props: Optional user provided props to override the default props for the API Gateway. Default: - Default props are used
        :param existing_lambda_obj: Existing instance of Lambda Function object. If ``deploy`` is set to false only then this property is required Default: - None
        :param lambda_function_props: Optional user provided props to override the default props. If ``deploy`` is set to true only then this property is required Default: - Default props are used

        summary:
        :summary:: The properties for the DynamoDBStreamToLambdaToElastciSearchAndKibana Construct
        """
        if isinstance(dynamo_event_source_props, dict): dynamo_event_source_props = aws_cdk.aws_lambda_event_sources.DynamoEventSourceProps(**dynamo_event_source_props)
        if isinstance(dynamo_table_props, dict): dynamo_table_props = aws_cdk.aws_dynamodb.TableProps(**dynamo_table_props)
        if isinstance(es_domain_props, dict): es_domain_props = aws_cdk.aws_elasticsearch.CfnDomainProps(**es_domain_props)
        if isinstance(lambda_function_props, dict): lambda_function_props = aws_cdk.aws_lambda.FunctionProps(**lambda_function_props)
        self._values = {
            'deploy_lambda': deploy_lambda,
            'domain_name': domain_name,
        }
        if dynamo_event_source_props is not None: self._values["dynamo_event_source_props"] = dynamo_event_source_props
        if dynamo_table_props is not None: self._values["dynamo_table_props"] = dynamo_table_props
        if es_domain_props is not None: self._values["es_domain_props"] = es_domain_props
        if existing_lambda_obj is not None: self._values["existing_lambda_obj"] = existing_lambda_obj
        if lambda_function_props is not None: self._values["lambda_function_props"] = lambda_function_props

    @builtins.property
    def deploy_lambda(self) -> bool:
        """Whether to create a new lambda function or use an existing lambda function.

        If set to false, you must provide a lambda function object as ``existingObj``

        default
        :default: - true
        """
        return self._values.get('deploy_lambda')

    @builtins.property
    def domain_name(self) -> str:
        """Cognito & ES Domain Name.

        default
        :default: - None
        """
        return self._values.get('domain_name')

    @builtins.property
    def dynamo_event_source_props(self) -> typing.Optional[aws_cdk.aws_lambda_event_sources.DynamoEventSourceProps]:
        """Optional user provided props to override the default props.

        default
        :default: - Default props are used
        """
        return self._values.get('dynamo_event_source_props')

    @builtins.property
    def dynamo_table_props(self) -> typing.Optional[aws_cdk.aws_dynamodb.TableProps]:
        """Optional user provided props to override the default props.

        default
        :default: - Default props are used
        """
        return self._values.get('dynamo_table_props')

    @builtins.property
    def es_domain_props(self) -> typing.Optional[aws_cdk.aws_elasticsearch.CfnDomainProps]:
        """Optional user provided props to override the default props for the API Gateway.

        default
        :default: - Default props are used
        """
        return self._values.get('es_domain_props')

    @builtins.property
    def existing_lambda_obj(self) -> typing.Optional[aws_cdk.aws_lambda.Function]:
        """Existing instance of Lambda Function object.

        If ``deploy`` is set to false only then this property is required

        default
        :default: - None
        """
        return self._values.get('existing_lambda_obj')

    @builtins.property
    def lambda_function_props(self) -> typing.Optional[aws_cdk.aws_lambda.FunctionProps]:
        """Optional user provided props to override the default props.

        If ``deploy`` is set to true only then this property is required

        default
        :default: - Default props are used
        """
        return self._values.get('lambda_function_props')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DynamoDBStreamToLambdaToElasticSearchAndKibanaProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "DynamoDBStreamToLambdaToElasticSearchAndKibana",
    "DynamoDBStreamToLambdaToElasticSearchAndKibanaProps",
]

publication.publish()
