from aws_cdk import (
    Duration,
    Stack,
    aws_dynamodb,
    aws_lambda,
    aws_apigateway
)
from constructs import Construct

class CdkLambdaDynamodbStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #define the tables stores Todo items
        table = aws_dynamodb.Table(self, "Table", partition_key=aws_dynamodb.Attribute(
            name="id",
            type=aws_dynamodb.AttributeType.STRING),
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST          
        )
        
        #define the Lambda functions
        list_handler = aws_lambda.Function(self, "TodoListFunction", code=aws_lambda.Code.from_asset("./lambda"),
                                           handler="list.list",
                                           timeout=Duration.minutes(5),
                                           runtime=aws_lambda.Runtime.PYTHON_3_7)
        
        create_handler = aws_lambda.Function(self, "TodoCreateFunction", code=aws_lambda.Code.from_asset("./lambda"),
                                           handler="create.create",
                                           timeout=Duration.minutes(5),
                                           runtime=aws_lambda.Runtime.PYTHON_3_7)
        
        get_handler = aws_lambda.Function(self, "TodoGetFunction", code=aws_lambda.Code.from_asset("./lambda"),
                                           handler="get.get",
                                           timeout=Duration.minutes(5),
                                           runtime=aws_lambda.Runtime.PYTHON_3_7)
        
        update_handler = aws_lambda.Function(self, "TodoUpdateFunction", code=aws_lambda.Code.from_asset("./lambda"),
                                           handler="update.update",
                                           timeout=Duration.minutes(5),
                                           runtime=aws_lambda.Runtime.PYTHON_3_7)
        
        delete_handler = aws_lambda.Function(self, "TodoDeleteFunction", code=aws_lambda.Code.from_asset("./lambda"),
                                           handler="delete.delete",
                                           timeout=Duration.minutes(5),
                                           runtime=aws_lambda.Runtime.PYTHON_3_7)
        
        
        # pass the table name to each handler through an environment variable and grant the handler read/write permissions on the table
        handler_list = [list_handler, create_handler, get_handler, update_handler, delete_handler]

        for handler in handler_list:
            handler.add_environment('DYNAMODB_TABLE', table.table_name)
            table.grant_read_write_data(handler)
            
        #define the API endpoint
        api = aws_apigateway.LambdaRestApi(self, "TodoApi", handler=list_handler, proxy=False)
        
        #define LambdaIntegrations
        list_lambda_integration = aws_apigateway.LambdaIntegration(list_handler)
        create_lambda_integration = aws_apigateway.LambdaIntegration(create_handler)
        get_lambda_integration = aws_apigateway.LambdaIntegration(get_handler)
        update_lambda_integration = aws_apigateway.LambdaIntegration(update_handler)
        delete_lambda_integration = aws_apigateway.LambdaIntegration(delete_handler)
        
        #define REST API model and associate methods with LambdaIntegrations
        api.root.add_method('ANY')
        
        todos = api.root.add_resource('todos')
        todos.add_method('GET', list_lambda_integration)
        todos.add_method('POST', create_lambda_integration)
        
        todo = todos.add_resource('{id}')
        todo.add_method('GET', get_lambda_integration)
        todo.add_method('PUT', update_lambda_integration)
        todo.add_method('DELETE', delete_lambda_integration)
        