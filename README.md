# aws_federated_list_securitygroups

Usage: listSecurityGroups <account> [<region>] (default \"us-east-2 us-east-1 us-west-1 us-west-2\")

List security groups from a federated account

This script will list security groups for a federated account using STS tokens

To use, you need to:
1. Add a policy that includes ec2:describesecuritygroups to the target account (the account being monitored).
2. Create a role for cross-account access, designating the originating account (the account that will monitor the target account)
3. Attach the policy to the role.
4. Create a group/role/policy in the originating account that allows it to assume the role.
5. Create a CLI only user and add it to the group.
6. Set up your configuration to authenticate as that user (see boto3) and run the script.
