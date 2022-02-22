from aws_cdk import (aws_ecs, aws_ec2, Stack)
from constructs import Construct

class FargateStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        vpc = aws_ec2.Vpc(self, "MyVpc", cidr="10.0.0.0/16", max_azs=3)
        
        #define an ECS cluster hosted within the requested VPC
        cluster = aws_ecs.Cluster(self, 'cluster', vpc=vpc)
        
        #define our task definition with a single container
        ## the image is built and published from a local asset directory
        task_definition = aws_ecs.FargateTaskDefinition(self, "LoadTestTask")
        task_definition.add_container('TaurusLoadTest', image=aws_ecs.ContainerImage.from_asset("loadtest-cdk"),
                                      environment={'BASE_URL': "https://laxlkl0xg9.execute-api.us-east-1.amazonaws.com/prod/"})
        
        #define our fargate service, TPS determines how many instances we want from our task (each task produces a single TPS)
        aws_ecs.FargateService(self, 'service',
                               cluster=cluster,
                               task_definition=task_definition,
                               desired_count=5)