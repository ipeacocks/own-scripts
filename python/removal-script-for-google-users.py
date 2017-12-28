'''
This script is for removing users from Google Admin panel 
which were supended more then 30 days ago.
But before this script will upload all data as archive to sysadmin account.

For using this script just edit your email accounts and passwords in it.

This script uses GAM https://github.com/jay0lee/GAM. So previously it should
be installed and configured correct.
'''

import os
import shutil
import csv
import smtplib

from datetime import datetime, date

import tarfile
import os


def list_all_users():
    users_list = "python gam.py print users lastlogintime suspended"
    users_list = os.popen(users_list).read()

    correct_list = [row for row in csv.reader(users_list.splitlines(), delimiter=',')]
    correct_list = correct_list[1:-1]
    
    return correct_list


def list_suspended_users(correct_list):
    suspended_list = []

    for user in correct_list:
        last_login_date = user[1][:10]
        if user[2] == 'True':
            if last_login_date == "Never":
                print "{} - {}".format(last_login_date, user[0])
                suspended_list.append(user[0])
            else:
                delta = date.today() - datetime.strptime(last_login_date, '%Y-%m-%d').date()
                if delta.days >= 30:
                    suspended_list.append(user[0])
    return suspended_list


def unblock_user(suspended_list):
    unblock_command = "python gam.py update user {} suspended off".format(user)
    os.popen(unblock_command).read()


def block_user(user):
    unblock_command = "python gam.py update user {} suspended on".format(user)
    os.popen(unblock_command).read()


def delete_user(user):
    delete_command = "python gam.py delete user {}".format(user)
    os.popen(delete_command).read()


def normilize_filelist(user):
    filelist_command = "python gam.py user {} show filelist id filesize".format(user)
    filelist = os.popen(filelist_command).read()

    correct_filelist = [row for row in csv.reader(filelist.splitlines(), delimiter=',')]
    correct_filelist = correct_filelist[1:-1]

    return correct_filelist


def ids(correct_filelist):

    id_filelist = []

    for file in correct_filelist:
        id_filelist.append(file[3])

    return id_filelist


def download_files_from_drive(user, id_filelist):
    for id in id_filelist:
        print "Downloading file with id {}".format(id)
        download_command = "python gam.py user {0} get drivefile id {1} \
                            targetfolder /tmp/test_dir/{0}".format(user, id)
        os.popen(download_command).read()


def upload_file_to_drive(user, output_filename):
    print "Uploading {}".format(output_filename)
    upload_command = "python gam.py user sysadmin@gmail.com add drivefile \
                      localfile {}".format(output_filename)
    os.popen(upload_command).read()


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def user_archive_size(output_filename):
    print "{} bytes is archive size".format(os.path.getsize(output_filename))
    return os.path.getsize(output_filename)


# 32212254720 bytes - 30 GB
def free_admin_size(admin_filelist):

    used_size = 0

    # print admin_filelist
    for file in admin_filelist:
        if file[1] != "":
            used_size = used_size + int(file[1])

    free_space = 32212254720 - used_size
    print "{} is free admin space".format(free_space)
    return free_space


def sent_mail():

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    sender = "Autoremove tool"
    to = "Me"
    subject = "Smth wrong with sysadmin space"
    receivers = ["admin@gmail.com"]

    headers = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, to, subject)
    body = ("Hello,\n\n"
            "Cant move data for suspended users: not enough space on sysadmin@gmail.com.\n"
            "Please check logs.\n\n"
            "Bye."
            )
    msg = headers + body

    mailserver = smtplib.SMTP(smtp_server, smtp_port)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(admin_mailbox, admin_mailbox_pw)
    mailserver.sendmail(admin_mailbox, receivers, msg)
    mailserver.close()


admin_mailbox = "sysadmin@gmail.com"
admin_mailbox_pw = "my_password"

correct_list = list_all_users()
suspended_list = list_suspended_users(correct_list)

if suspended_list:
    # ---- free space for admin user sysadmin@gmail.com
    admin_filelist = normilize_filelist(admin_mailbox)
    free_space = free_admin_size(admin_filelist)
    # ----
    archive_size = 0

    print suspended_list

    if free_space > 0:
        for user in suspended_list:

            # we cant count disk space in blocked/suspended users
            unblock_user(user)
            
            free_space -= archive_size
            print "This is free space on sysadmin mailbox: {} bytes".format(free_space)

            correct_filelist = normilize_filelist(user)
            id_filelist = ids(correct_filelist)

            root_dir = os.path.join("/tmp/test_dir", user)

            if os.path.exists(root_dir):
                shutil.rmtree(root_dir)
            os.makedirs(root_dir)

            output_filename = "/tmp/test_dir/{}{}".format(user, ".tgz")

            download_files_from_drive(user, id_filelist)
            make_tarfile(output_filename, root_dir)
            archive_size = user_archive_size(output_filename)

            if free_space > archive_size:
                upload_file_to_drive(admin_mailbox, output_filename)
                delete_user(user)
                shutil.rmtree(root_dir)
            else:
                sent_mail()
                block_user(user)
    else:
        sent_mail()
else:
    print "Nothing to backup. There are no suspended users."
