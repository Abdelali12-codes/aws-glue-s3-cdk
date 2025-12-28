import sys
import boto3
import os
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

# Parse the input arguments
args = getResolvedOptions(sys.argv, ['DestinationBucketName', 'SourceBucketName', 'ObjectKey', 'FileName', 'DatabaseName'])

# Create GlueContext and SparkContext
glueContext = GlueContext(SparkContext.getOrCreate())
job = Job(glueContext)

# Load the data from the Glue catalog
dynamicframe = glueContext.create_dynamic_frame.from_catalog(
    database=args['DatabaseName'],
    table_name=args['FileName']
)

# Extract filename and directory from ObjectKey
filename = os.path.basename(args['ObjectKey'])
directory = os.path.dirname(args['ObjectKey']) if '/' in args['ObjectKey'] else ""

# Construct the output path, ensuring the file name is included
output_path = f"s3://{args['DestinationBucketName']}/{directory}"

# Write the transformed data to the destination bucket in CSV format with a specific output file name
datasink4 = glueContext.write_dynamic_frame.from_options(
    frame=dynamicframe,
    connection_type="s3",
    connection_options={"path": output_path},
    format="csv",
    format_options={"quoteChar": '"', "separator": ","},  # Optional: specify CSV options
    transformation_ctx="datasink4"
)

# Initialize a boto3 S3 client
s3_client = boto3.client('s3')

# Delete the file from the source bucket
s3_client.delete_object(Bucket=args['SourceBucketName'], Key=args['ObjectKey'])

response = s3_client.list_objects_v2(Bucket=args['DestinationBucketName'], Prefix=directory)

pattern = "run-"

if 'Contents' in response:
    for obj in response['Contents']:
        object_key = obj['Key']
        
        # Check if the object key contains the pattern 'run-'
        if pattern in object_key:
            print(f"Processing: {object_key}")
            new_key = directory + "/" + filename
            
            # Copy the object to the new key (same bucket, new key)
            s3_client.copy_object(
                Bucket=args['DestinationBucketName'],
                CopySource={'Bucket': args['DestinationBucketName'], 'Key': object_key},
                Key=new_key
            )
            print(f"Copied to: {new_key}")
			 # Delete the original object
            s3_client.delete_object(Bucket=args['DestinationBucketName'], Key=object_key)
            print(f"Deleted original: {object_key}")
else:
    print("No objects found in the uploads directory.")

# Commit the Glue job
job.commit()
