# A demo project illustrating how to deploy a load balanced AWS EC2 web server using Python CDK.
# Project creates AWS artifacts:
#  - VPC
#  - EC2 (EC2, ALB, ASG, Target group, Launch Config)
#  - S3
# User data to launch Apache webserver with custom index.html page is loaded from S3 bucket

Requirements:
 - A command shell such as Git Bash
 - Python
 - CDK
 - Node JS/NPM for miscellaneous package installs

Modify cdk.json with your account in the "envs" configuration

To create the web server:<br>
    1. Run pip install -r requirements.txt from root of project<br>
    2. Modify app.py to deploy S3 buket (uncomment line "S3CreateProject(app, "S3CreateProject", env=env_dev)")<br>
&nbsp;&nbsp;&nbsp;- From project root run "cdk init" to check for errors, then "cdk deploy"<br>
    3. From root of project copy html file to S3<br>
&nbsp;&nbsp;&nbsp;-  aws s3 cp index.html s3://"<<your bucket name>>"/index.html<br>
    4. Modify app.py to deploy VPC (uncomment line "CustomVpcStack(app, "CustomVpcStack", env=env_dev)")<br>
&nbsp;&nbsp;&nbsp;- From project root run "cdk init" to check for errors, then "cdk deploy CustomVpcStack --require-approval never"<br>
&nbsp;&nbsp;&nbsp;- This can take a while to deploy<br>
    5. Verifying deploy of VPC on AWS console<br>
&nbsp;&nbsp;&nbsp;- From AWS console you can find it via VPC->You VPCs<br>
    6. Modify app.py to deploy EC2 (uncomment line "CustomVpcStack(app, "CustomVpcStack", env=env_dev)"<br>
&nbsp;&nbsp;&nbsp;- Modify class CustomEc2Stack to use ID of VPC created in step #4<br>
&nbsp;&nbsp;&nbsp;- From project root run "cdk init" to check for errors, then "cdk deploy CustomEc2Stack --require-approval never"<br>
    7.  Find IP address of new EC2, and plug into browser such as http://<<ip address><br>
&nbsp;&nbsp;&nbsp;- The custom index.html page will display if all went well<br>
&nbsp;&nbsp;&nbsp;- It may take a couple minutes for apache to recognize/load the html page<br>
