from aws_cdk import (
    core,
    aws_s3 as _s3
)
from constructs import Construct


class S3CreateProject(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define S3 stack
        s3bucket = _s3.Bucket(
            self,
            "s3BucketId",
            # Supply your unique bucket name
            bucket_name="my-s3buckets-got-a-hole-in-it",  # hat tip to Clarence Williams
            encryption=_s3.BucketEncryption.S3_MANAGED,
            versioned=False,
            block_public_access=_s3.BlockPublicAccess.BLOCK_ALL
        )

        # Can check for name in Cloud Formation->Stacks (S3CreateProject) ->Output
        core.CfnOutput(
            self,
            "cdkBucketOutput1",
            value=s3bucket.bucket_name,
            description="CDK bucket",
            export_name="cdkBucketOutput1"
        )
