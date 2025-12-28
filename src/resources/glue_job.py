from aws_cdk import (
    Resource,
    aws_glue as glue,
    aws_iam as iam,
    aws_s3_assets as assets
)
import os 

DIR = os.path.dirname(os.path.dirname(os.path.relpath(__file__)))


class GlueJob(Resource):
    def __init__(self, scope, id, job_role: iam.IRole, **kwargs):
        super().__init__(scope, id)
        
        scriptasset = assets.Asset(self, "jobscript",
                 path= os.path.join(DIR, 'job_script/job_script.py')                   
                )
        
        scriptasset.grant_read(job_role)

        glue_job = glue.CfnJob(self, "gluejob",
            name="glue-job",
            glue_version= "4.0",
            command=glue.CfnJob.JobCommandProperty(
                name="glueetl",
                python_version="3",
                script_location=f"s3://{scriptasset.s3_bucket_name}/{scriptasset.s3_object_key}"
            ),
            role=job_role.role_arn,
            default_arguments= {
                "--DestinationBucketName": "",
                "--SourceBucketName": "",
                "--ObjectKey": "",
                "--FileName": "",
                "--DatabaseName": ""
            }
        )
        self.job_name = glue_job.name
