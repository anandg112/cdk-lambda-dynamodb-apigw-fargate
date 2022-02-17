import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_lambda_dynamodb_fargate.cdk_lambda_dynamodb_fargate_stack import CdkLambdaDynamodbFargateStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_lambda_dynamodb_fargate/cdk_lambda_dynamodb_fargate_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkLambdaDynamodbFargateStack(app, "cdk-lambda-dynamodb-fargate")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
