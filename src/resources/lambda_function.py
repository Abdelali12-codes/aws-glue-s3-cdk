from aws_cdk import (
    Resource,
    Duration,
    aws_lambda as _lambda,
    aws_iam as iam
)
import os 
from ..configuration.config import glue_db_name

DIR = os.path.dirname(os.path.dirname(os.path.relpath(__file__)))

class LambdaFunction(Resource):
    def __init__(self, scope, id,source_bucket, destination_bucket , job_name, glue_service_role: iam.IRole, **kwargs):
        super().__init__(scope, id)

        self.lambda_function = _lambda.Function(
            self, "ProcessDataFileRenameV1",
            function_name="lambda_processor",
            runtime=_lambda.Runtime.PYTHON_3_10,  # Update to a supported version if needed
            handler="app.lambda_handler",
            code=_lambda.Code.from_asset(os.path.join(DIR, 'lambda_src')),  # Assuming the Lambda code is in the current directory
            description="Lambda function to process renaming of data files using AWS Glue.",
            memory_size=128,
            timeout=Duration.seconds(300),
            environment={
                "GlueServiceRole": glue_service_role.role_arn,
                "DestinationBucket": destination_bucket,
                "SourceBucketName": source_bucket,
                "JobName": job_name,
                "DatabaseName": glue_db_name
            }
        )


        self.lambda_function.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "glue:GetCrawler",
                    "glue:BatchGetCrawlers",
                    "glue:StartCrawler",
                    "glue:StartJobRun",
                    "glue:CreateCrawler"
                ],
                resources=["*"]
            )
        )

        self.lambda_function.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["iam:PassRole"],
                resources=[glue_service_role.role_arn]
            )
        )