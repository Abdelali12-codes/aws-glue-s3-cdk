import json
import boto3
import logging
import os
from urllib.parse import unquote_plus

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

glue = boto3.client('glue')
GlueServiceRole = os.environ['GlueServiceRole']
DestinationBucket = os.environ['DestinationBucket']
SourceBucketName = os.environ['SourceBucketName']
JobName = os.environ['JobName']
DatabaseName = os.environ['DatabaseName']

def lambda_handler(event, context):
    logger.info(json.dumps(event))
    for record in event['Records']:
        # Grab the file name from the event record which triggered the lambda function
        # Construct the path for data file, name file, and renamed file. 
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        data_file_name = key.split('/')[0]
        s3_data_file_path = 's3://' + bucket + '/' + data_file_name + '/'

        # Create a crawler for the data file if it does not already exist and run it.
        try:
            crawler = glue.get_crawler(Name=data_file_name)
            logger.info(f"Crawler for {data_file_name} already exists, attempting to start it.")
            glue.start_crawler(Name=data_file_name)
        except glue.exceptions.EntityNotFoundException as e:
            logger.info(f"Crawler for {data_file_name} does not exist, creating it.")
            glue.create_crawler(
                Name=data_file_name,
                Role=GlueServiceRole,
                DatabaseName=glue_db_name,
                Description='Crawler for data files',
                Targets={
                    'S3Targets': [
                        {
                            'Path': s3_data_file_path,
                            'Exclusions': []
                        },
                    ]
                },
                SchemaChangePolicy={
                    'UpdateBehavior': 'UPDATE_IN_DATABASE',
                    'DeleteBehavior': 'DELETE_FROM_DATABASE'
                }
            )
            glue.start_crawler(Name=data_file_name)
        except glue.exceptions.CrawlerRunningException as e:
            logger.info(f"Crawler for {data_file_name} is already running.")
        except Exception as e:
            logger.error(f"Error starting crawler for {data_file_name}: {e}")


        # Run the agnostic Glue job to rename the files by passing the file name argument.
        try:
            glue.start_job_run(
                JobName=JobName,
                Arguments={
                    '--SourceBucketName': SourceBucketName,
                    '--DestinationBucketName': DestinationBucket,
                    '--ObjectKey': key,
                    '--FileName': data_file_name,
                    '--DatabaseName': DatabaseName
                }
            )
        except Exception as e:
            logger.error(f"Glue Job runtime issue: {e}")
