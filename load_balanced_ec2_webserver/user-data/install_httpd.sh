#!/bin/bash
sudo yum install -y httpd
sudo chkconfig httpd on
sudo service httpd start
# Copy index page from S3 to Apache default
sudo aws s3 cp s3://my-s3buckets-got-a-hole-in-it/index.html /var/www/html/index.html