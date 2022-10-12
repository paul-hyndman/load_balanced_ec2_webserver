#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

from resource_stacks.s3_create import S3CreateProject

from resource_stacks.custom_vpc import CustomVpcStack

from resource_stacks.custom_ec2 import CustomEc2Stack

app = cdk.App()
# For demo, use your account and preferred region
# see https://docs.aws.amazon.com/cdk/v2/guide/environments.html
env_dev = cdk.Environment(account="991417388566", region="us-east-1")

# To incrementally deploy, deploy in order:
#   S3
#   VPC
#   EC2
S3CreateProject(app, "S3CreateProject", env=env_dev)
CustomVpcStack(app, "CustomVpcStack", env=env_dev)
CustomEc2Stack(app, "CustomEc2Stack", env=env_dev)
app.synth()
