import boto3
import re
import datetime

ec = boto3.client('ec2')
iam = boto3.client('iam')

"""
This function looks at *all* snapshots that have a "DeleteOn" tag containing
the current day formatted as YYYY-MM-DD. This function should be run at least
daily.
"""

# def lambda_handler(event, context):
def main():
    account_ids = list()
    try:
        """
        You can replace this try/except by filling in `account_ids` yourself.
        Get your account ID with:
        > import boto3
        > iam = boto3.client('iam')
        > print(iam.get_user()['User']['Arn'].split(':')[4])
        """
        account_ids.append(iam.get_user()['User']['Arn'].split(':')[4])
    except Exception as e:
        # use the exception message to get the account ID the function executes under
        account_ids.append(re.search(r'(arn:aws:sts::)([0-9]+)', str(e)).groups()[1])


    delete_on = datetime.date.today().strftime('%Y-%m-%d')
    filters = [
        {'Name': 'tag-key', 'Values': ['DeleteOn']},
        {'Name': 'tag-value', 'Values': [delete_on]},
    ]
    snapshots = ec.describe_snapshots(OwnerIds=account_ids, Filters=filters)['Snapshots']
    print(snapshots)

    if snapshots:
        pass
    else:
        print('Nothing to remove')
        exit(0)

    for snap in snapshots:
        print("Deleting snapshot {}".format(snap['SnapshotId']))
        ec.delete_snapshot(SnapshotId=snap['SnapshotId'])


if __name__ == "__main__":
    main()
