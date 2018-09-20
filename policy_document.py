#!/usr/local/bin/python3

import boto3
import json
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--role", help="Name of the iam role")
parser.add_argument("-p", "--policy", help="Name of the policy")
parser.add_argument("-v", "--version", help="Version of the policy")
parser.add_argument("--inline", help="To get a inline policy")
parser.add_argument("--custom", help="To get a custom policy")
parser.add_argument("-P", "--path", help="policy path")

args = parser.parse_args()

if args.inline:
    client = boto3.client('iam')
    role_name = args.role
    policy_name = args.policy
    file_name = policy_name + ".json"
    iam_policy = client.get_role_policy(
        RoleName = role_name,
        PolicyName = policy_name
    )

    iam_json = iam_policy.get("PolicyDocument", "none")

    with open(file_name, "w") as json_file:
        json.dump(iam_json, json_file, indent=4)
elif args.custom:
    iam = boto3.client('iam')
    account_id = boto3.client('sts').get_caller_identity()['Account']
    policy_name = args.policy
    policy_path = args.path
    version_id = args.version
    file_name = policy_name + ".json"
    iam_policy = iam.get_policy_version(
        PolicyArn= "arn:aws:iam::" + account_id + ":" + policy_path + "/" + policy_name,
        VersionId= version_id
    )
    iam_json = iam_policy.get("PolicyVersion", "none")
    iam_document = iam_json.get("Document", "none")


    with open(file_name, "w") as json_file:
        json.dump(iam_document, json_file, indent=4)
else:
    print ("no policy selected to extract")
