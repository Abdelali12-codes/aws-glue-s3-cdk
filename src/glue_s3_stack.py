from aws_cdk import (
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_iam as iam,
    aws_s3_notifications as s3n,
    Stack,
    RemovalPolicy
)
from constructs import Construct
from .resources import *
import os
from .configuration.config import source_bucketname, destination_bucketname

DIR = os.path.dirname(os.path.relpath(__file__))

class GlueS3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define the S3 buckets (replace with actual bucket names or pass as parameters)
        landing_bucket = s3.Bucket(self, "file-landing-bucket",
                                   bucket_name= source_bucketname,
                block_public_access=s3.BlockPublicAccess.BLOCK_ALL
            )
        
        destination_bucket = s3.Bucket(self, "file-destination-bucket",
                                   bucket_name= destination_bucketname,
                block_public_access=s3.BlockPublicAccess.BLOCK_ALL
            )
        
        # iam permissions
        iam_permissions = IamPermissions(self, "iampermissions", landing_bucket= landing_bucket,
                       destination_bucket= destination_bucket)
        

        # glue job
        glue_job = GlueJob(self, "gluejob", job_role= iam_permissions.glue_service_role)
        
        # lambda
        lambda_processor = LambdaFunction(self, "lambdaprocessor",
                                          job_name=glue_job.job_name,
                                          source_bucket= landing_bucket.bucket_name,
                                          destination_bucket= destination_bucket.bucket_name,
                                          glue_service_role= iam_permissions.glue_service_role
                                        )
        
       
        # Set up S3 event notification to trigger Lambda
        landing_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(lambda_processor.lambda_function)
        )

        