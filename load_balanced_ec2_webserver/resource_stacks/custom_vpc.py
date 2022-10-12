from aws_cdk import (
    core,
    aws_ec2 as _ec2
)


class CustomVpcStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        app = core.App()

        prod_configs = app.node.try_get_context('envs')['dev']
        vpc = _ec2.Vpc(
            self,
            "customVpcId",
            cidr=prod_configs['vpc_configs']['vpc_cidr'],
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                _ec2.SubnetConfiguration(
                    name="publicSubnet", cidr_mask=prod_configs['vpc_configs']['cidr_mask'], subnet_type=_ec2.SubnetType.PUBLIC
                ),
                _ec2.SubnetConfiguration(
                    name="privateSubnet", cidr_mask=prod_configs['vpc_configs']['cidr_mask'], subnet_type=_ec2.SubnetType.PRIVATE
                ),
                _ec2.SubnetConfiguration(
                    name="dbSubnet", cidr_mask=prod_configs['vpc_configs']['cidr_mask'], subnet_type=_ec2.SubnetType.ISOLATED
                )
            ]
        )

        core.CfnOutput(self,
                       "customVpcOut",
                       value=vpc.vpc_id,
                       export_name="customVpcId")
