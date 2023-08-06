import boto3
import time
import datetime
import click
from datetime import datetime

@click.command()
@click.option('--db_instance', default='DBInstanceIdentifier for snapshot.', show_default=True, help='Database instance')
@click.option('--s3_bucket', default='The Amazon S3 bucket that the snapshot is exported to.', show_default=True)
@click.option('--kms_key', default='The ID of the AWS KMS key that is used to encrypt the snapshot when its exported to Amazon S3. The KMS key ID is the Amazon Resource Name (ARN).', show_default=True )
@click.option('--iam_role_arn', default='The name of the IAM role that is used to write to Amazon S3 when exporting a snapshot.', show_default=True)

def main(db_instance,s3_bucket,kms_key, iam_role_arn):
    client = boto3.client('rds')

    snapshot_time = datetime.now().strftime("snap-%Y-%m-%d-%H-%M")
# create snapshot for rds
    def create_snapshot():

        snapshot_name = "{0}-{1}".format(db_instance,snapshot_time)
        snap_run = client.create_db_snapshot(
            DBSnapshotIdentifier=snapshot_name,
            DBInstanceIdentifier=db_instance
        )
        time.sleep(3)  # wait few seconds before status request
        current_status = None
        while True:
            current_status =  client.describe_db_snapshots(DBSnapshotIdentifier=snapshot_name)['DBSnapshots'][0]['Status']
            current_progress = client.describe_db_snapshots(DBSnapshotIdentifier=snapshot_name)['DBSnapshots'][0]['PercentProgress']
            if current_status == 'available':
                snapshot_success = True
                print("DB snapshot %s is ready" % snapshot_name)
                break
            if  current_status == 'failed':
                print("DB snapshot filed, exit")
                exit()
            else:
                time.sleep(5)
                print(str(datetime.now()))
                print("DB snapshot %s in progress,  progress:%s, status: %s " % (snapshot_name, current_progress, current_status))
            # return current_status
        return snapshot_name
# encrypting rds snapshot
    def encrypt_snapshot():
        source_snapshot_name = create_snapshot()
        encrypted_snapshot_name = 'encrypted-' + str(source_snapshot_name)
        encrypt_run = client.copy_db_snapshot(
            SourceDBSnapshotIdentifier=source_snapshot_name,
            TargetDBSnapshotIdentifier=encrypted_snapshot_name,
            KmsKeyId= kms_key,
        )
        time.sleep(3)  # wait few seconds before status request
        print("Encrypting snapshot")
        current_status = None
        while True:
            current_status = client.describe_db_snapshots(DBSnapshotIdentifier=encrypted_snapshot_name)['DBSnapshots'][0]['Status']
            current_progress = client.describe_db_snapshots(DBSnapshotIdentifier=encrypted_snapshot_name)['DBSnapshots'][0]['PercentProgress']
            encrypted_snapshot_arn = client.describe_db_snapshots(DBSnapshotIdentifier=encrypted_snapshot_name)['DBSnapshots'][0]['DBSnapshotArn']
            if current_status == 'available':
                snapshot_success = True
                print("DB snapshot %s is ready" % encrypted_snapshot_name)
                print(str(encrypted_snapshot_arn))
                # delete source snapshot if encrypting process finished successfully
                def delete_source_snapshot():
                    print("Delete source snapshot:%s" %(source_snapshot_name) )
                    delete_snapshot = client.delete_db_snapshot(DBSnapshotIdentifier=source_snapshot_name)
                delete_source_snapshot()
                break
            if  current_status == 'failed':
                print("DB snapshot failed, exit")
                exit()
            else:
                time.sleep(5)
                print(str(datetime.now()))
                print("DB snapshot %s in progress,status:%s, progress:%s " % (encrypted_snapshot_name, current_status, current_progress))
        return encrypted_snapshot_arn
    
# copy encrypted snapshot to s3 bucket
    def copy_snapshot_to_s3():
        export_task_id = db_instance + str(snapshot_time)
        snapshot_arn = encrypt_snapshot()
        copy_snapshot = client.start_export_task(
        ExportTaskIdentifier=export_task_id,
        SourceArn=snapshot_arn,
        S3BucketName=s3_bucket,
        IamRoleArn=iam_role_arn,
        KmsKeyId=kms_key
    )
        time.sleep(3)  # wait few seconds before status request
        print("Moving snapshot to s3")
        current_status = None
        while True:
            current_status = client.describe_export_tasks(ExportTaskIdentifier=export_task_id)['ExportTasks'][0]['Status']
            current_progress = client.describe_export_tasks(ExportTaskIdentifier=export_task_id)['ExportTasks'][0]['PercentProgress']
            if current_status == 'COMPLETE':
                snapshot_success = True
                print("DB snapshot %s export to s3  is done" % export_task_id)
                break
            if current_status == 'FAILED':
                print("DB snapshot export failed, exit")
                exit()
            else:
                time.sleep(5)
                print(str(datetime.now()))
                print("DB snapshot  in progress,status:%s, progress:%s " % (current_status, current_progress))

    copy_snapshot_to_s3()
main()