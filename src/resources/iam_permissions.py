from aws_cdk import (
    Resource,
    aws_iam as iam,
    aws_s3 as s3
)

class IamPermissions(Resource):
    def __init__(self, scope, id, landing_bucket: s3.IBucket, destination_bucket: s3.IBucket, **kwargs):
        super().__init__(scope, id)

        self.glue_service_role = iam.Role(
            self, "GlueServiceRole",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
            role_name="GlueServiceRole",
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSGlueServiceRole")
            ]
        )

        self.glue_service_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    's3:*Object',
                    's3:ListBucket'
                ],
                resources=[
                    destination_bucket.bucket_arn,  # The destination bucket ARN
                    destination_bucket.arn_for_objects("*"),
                    landing_bucket.arn_for_objects("*")  # The landing bucket with wildcard
                ]
            )
        )