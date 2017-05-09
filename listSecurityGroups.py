#! /usr/bin/python
import boto3
import sys
import pprint

def get_security_groups(account, region_name_arg = 'us-west-1'):
    print("\n" + region_name_arg + ":")
    pretty = pprint.PrettyPrinter(indent=4)

    sts_client = boto3.client('sts')

    # Call the assume_role method of the STSConnection object and pass the role
    # ARN and a role session name.
    assumed_role = sts_client.assume_role(
        RoleArn="arn:aws:iam::" + account + ":role/SecurityMonkey",
        Policy='{"Version":"2012-10-17","Statement":[{"Sid":"Stmt1","Effect":"Allow","Action":"ec2:describesecuritygroups","Resource":"*"}]}',
        RoleSessionName="TestAssumeRole"
    )

    # Get temporary credentials
    credentials = assumed_role['Credentials']

    # Create connection to Amazon S3
    ec2_resource = boto3.resource(
        'ec2',
        region_name = region_name_arg,
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )

    security_groups = ec2_resource.security_groups

    # Buckets Ahoy?
    for security_group in security_groups.all():
        print(security_group.group_id)
        print("ingress:\n========")
        pretty.pprint(security_group.ip_permissions)
        print("egress:\n=======")
        pretty.pprint(security_group.ip_permissions_egress)


def main():
    if len(sys.argv) == 3:
        regions = sys.argv[2].split()
    else:
        regions = ['us-east-2', 'us-east-1', 'us-west-1', 'us-west-2']

    if len(sys.argv) >= 2:
        print("\nAccount: " + sys.argv[1])
        for region in regions:
            get_security_groups(sys.argv[1], region_name_arg = region)
    else:
        print("Usage: listSecurityGroups <account> [<region>] (default \"us-east-2 us-east-1 us-west-1 us-west-2\")")


if __name__ == "__main__":
    main()
