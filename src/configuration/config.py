import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_rds as rds

REGION = "us-east-1"
ACCOUNT = "080266302756"

source_bucketname = "file-landing-bucket-28-09" # source bucket that we will upload files to
destination_bucketname = "file-destination-bucket-28-09" # destination bucket that new file will be stored

glue_db_name = "sampledb" # databasename of glue catalog