🚀 Running the Project Locally
------------------------------

### Prerequisites

*   AWS CLI configured with valid credentials
    
*   AWS CDK installed
    
*   Python installed
    
*   Required permissions for S3, Lambda, and AWS Glue
    

### Steps

1.  **Update configuration**
    
    *   src/configuration
        
    *   Open config.py and update the configuration values based on your environment and requirements.
        
2.  cdk deploy
    
3.  **Locate the source S3 bucket**
    
    *   src/configuration/config.py
        
4.  **Upload the input file**
    
    *   In the source bucket, create a folder (for example: uploads)
        
    *   Upload the file glue\_example.csv, which is located at the root of the project, into this folder
        
5.  **Automatic processing**
    
    *   Uploading the file triggers a Lambda function that:
        
        *   Starts the AWS Glue crawler
            
        *   Runs the AWS Glue job
            
        *   Processes the file and writes the output to the destination bucket
            
6.  **Verify the output**
    
    *   Once the Glue job finishes successfully, navigate to the **destination S3 bucket**
    ```        
        src/configuration/config.py
    ```
        
    *   Verify that the processed file exists in the destination bucket