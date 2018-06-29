# Idea of https://serverlesscode.com/post/lambda-schedule-ebs-snapshot-backups/

import boto3

ec = boto3.client('ec2')

def lambda_handler(event, context):
    backup_ebs_disks = ec.describe_volumes(
        Filters=[{'Name': 'tag-key', 'Values': ['backup', 'Backup']},]
        ).get('Volumes', [])

    if backup_ebs_disks:
        pass
    else:
        print('You have no tagged disks for backuping')
        exit(0)

    for disk in backup_ebs_disks:
        volume_id = disk['VolumeId']
        instance_id = disk['Attachments'][0]['InstanceId']
        ec.create_snapshot(VolumeId=volume_id)
        print("Made snapshot for {} on instance {}".format(volume_id, instance_id))
