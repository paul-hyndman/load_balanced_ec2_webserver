from aws_cdk import (
    core,
    aws_ec2 as _ec2,
    aws_iam as _iam,
    aws_elasticloadbalancingv2 as _elbv2,
    aws_autoscaling as _autoscaling
)


class CustomEc2Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Read bootstrap script to install Apache and copy index.html from S3
        with open("user-data/install_httpd.sh", mode="r") as file:
            user_data = file.read()

        # Get latest ami
        amzn_linux_ami = _ec2.MachineImage.latest_amazon_linux(
            generation=_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=_ec2.AmazonLinuxEdition.STANDARD,
            storage=_ec2.AmazonLinuxStorage.EBS,
            virtualization=_ec2.AmazonLinuxVirt.HVM
        )

        # Use VPC created earlier
        vpc = _ec2.Vpc.from_lookup(self,
                                   "importedVPC",
                                   # Use console to find ID previously created VPC
                                   vpc_id="vpc-06958939da3ec17cc")

        # Create Load Balancer
        alb = _elbv2.ApplicationLoadBalancer(
            self,
            "albId",
            vpc=vpc,
            internet_facing=True,
            load_balancer_name="WebServerAlb"
        )

        # ALB allows internet traffic
        alb.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80),
            description="Allow internet access on ALB port 80"
        )

        # Add ALB lister
        listener = alb.add_listener(
            id="listenerId",
            port=80,
            open=True)

        # Web Server IAM Role
        web_server_iam_role = _iam.Role(
            self,
            "webserverRoleId",
            assumed_by=_iam.ServicePrincipal(
                'ec2.amazonaws.com'),
            managed_policies=[
                _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"),
                _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")
            ]
        )

        # Create Autoscaling Group with two EC2 instances
        web_server_asg = _autoscaling.AutoScalingGroup(
            self,
            "webServerAsgId",
            vpc=vpc,
            vpc_subnets=_ec2.SubnetSelection(
                subnet_type=_ec2.SubnetType.PRIVATE
            ),
            instance_type=_ec2.InstanceType(
                instance_type_identifier="t2.micro"
            ),
            machine_image=amzn_linux_ami,
            role=web_server_iam_role,
            min_capacity=2,
            max_capacity=4,
            user_data=_ec2.UserData.custom(user_data),
            block_devices=[
                _autoscaling.BlockDevice(
                    device_name="/dev/sdb",
                    volume=_autoscaling.BlockDeviceVolume.ebs(
                        volume_size=50,
                        delete_on_termination=True,
                        encrypted=False,
                        volume_type=_autoscaling.EbsDeviceVolumeType.STANDARD)
                )
            ]
        )

        # Tell ASG security group to allow traffic from the ALB
        web_server_asg.connections.allow_from(
            alb,
            _ec2.Port.tcp(80),
            description="ASG security group is allowed to receive traffic from ALB"
        )

        # Add AutoScaling Group Instances to ALB Target Group
        listener.add_targets(
            "listenerId",
            port=80,
            targets=[web_server_asg]
        )

        # Echo Load Balancer URL in CloudFormation Output
        core.CfnOutput(
            self,
            "albDNS",
            value=f"http://{alb.load_balancer_dns_name}",
            description="Web server ALB DNS-based URL"
        )

        # # Create EC2 instance
        # web_server = _ec2.Instance(self,
        #                            "webserverId",
        #                            instance_type=_ec2.InstanceType(instance_type_identifier="t2.micro"),
        #                            instance_name="WebServer001",
        #                            machine_image=amzn_linux_ami,
        #                            vpc=vpc,
        #                            vpc_subnets=_ec2.SubnetSelection(
        #                                subnet_type=_ec2.SubnetType.PUBLIC
        #                            ),
        #                            user_data=_ec2.UserData.custom(user_data),
        #                            )
        #
        # # Add additional EBS Storage which is not required here, but useful when user data
        # # loads JDKs or other large files
        # web_server.instance.add_property_override(
        #     "BlockDeviceMappings", [
        #         {
        #             "DeviceName": "/dev/sdb",
        #             "Ebs": {
        #                 "VolumeSize": "50",
        #                 "DeleteOnTermination": "true"
        #             }
        #         }
        #     ]
        # )
        #
        # core.CfnOutput(self,
        #                "webServer001Ip",
        #                description="WebServer Public Ip Address",
        #                value=f"http://{web_server.instance_public_ip}")
        #
        # # Allow incoming web traffic
        # web_server.connections.allow_from_any_ipv4(
        #     _ec2.Port.tcp(80), description="Allow incoming web traffic"
        # )
        #
        # # Add permission to web server instance profile.  Not required here, but useful
        # web_server.role.add_managed_policy(
        #     _iam.ManagedPolicy.from_aws_managed_policy_name(
        #         "AmazonSSMManagedInstanceCore"
        #     )
        # )
        #
        # # Useful if your application reads from S3 buckets, but not required here
        # web_server.role.add_managed_policy(
        #     _iam.ManagedPolicy.from_aws_managed_policy_name(
        #         # In prod this would be custom policy vs. policy allowing read from any S3
        #         "AmazonS3ReadOnlyAccess"
        #     )
        # )
