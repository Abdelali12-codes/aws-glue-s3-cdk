#!/usr/bin/env python3
import os

import aws_cdk as cdk

from src.glue_s3_stack import GlueS3Stack
from src.configuration.config import *


app = cdk.App()
GlueS3Stack(app, "GlueS3Stack",
    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
    env=cdk.Environment(account=ACCOUNT, region=REGION)
    )

app.synth()
