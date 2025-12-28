# steps to run this project on your laptop

1. go to src folder in configuration folder and changes values you have in config.py file based on your requirements
2. deploy the cdk stack using cdk deploy command
3. when deployment finish
4. go to source bucket, the name of source bucket will be in config.py file under src/configuration folder
5. create folder called (uploads for example), then inside that folder and upload the glue_example.csv file that you can find it at the root folder of the project
6. after you upload the file in source bucket, will trigger lambda that will start glue crawler and glue job that will create the file in destionation bucket
7. once the glue job finish succefully
8. navigate to destination bucket (its name is on config.py that is under src/configuration folder), and you can verify that the file is there
