import boto3
import collections
import datetime

ec = boto3.client('ec2')


# def lambda_handler(event, context):
def main():
    backup_ebs_disks = ec.describe_volumes(
        Filters=[{'Name': 'tag-key', 'Values': ['backup', 'Backup']},]
        ).get('Volumes', [])

    if backup_ebs_disks:
        pass
    else:
        print('You have no tagged disks for backuping')
        exit(0)

    to_tag = collections.defaultdict(list)

    for disk in backup_ebs_disks:
        try:
            retention_days = [
                int(t.get('Value')) for t in disk['Tags']
                if t['Key'] == 'Retention'][0]
        # set in case when no Retention tag on EBS volume
        except IndexError:
            retention_days = 7

        volume_id = disk['VolumeId']
        instance_id = disk['Attachments'][0]['InstanceId']

        # take the snapshot, and save it in a list with others in the same
        # retention time category
        snap = ec.create_snapshot(VolumeId=volume_id)
        to_tag[retention_days].append(snap['SnapshotId'])
        print(to_tag)
        print("Made snapshot for {} on instance {}".format(volume_id, instance_id))


    for retention_days in to_tag.keys():
        # get the date X days in the future
        delete_date = datetime.date.today() + datetime.timedelta(days=retention_days)
        # format the date as YYYY-MM-DD
        delete_fmt = delete_date.strftime('%Y-%m-%d')
        print("Will delete {} snapshots on {}".format(len(to_tag[retention_days]), delete_fmt))
        ec.create_tags(
            Resources=to_tag[retention_days],
            Tags=[
                {'Key': 'DeleteOn', 'Value': delete_fmt},
            ]
        )

if __name__ == "__main__":
    main()
