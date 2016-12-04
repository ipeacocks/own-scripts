"""
This script uses Digital Ocean (https://www.digitalocean.com/)
api python wrapper and can snapshot VM. At first it turns off
VM then makes snapshot. VM will be turned on automatically after snapshot.
Script can be put into cron with logginning into any file:

@monthly  python do_snapshot.py  &>>  /var/log/do_snapshot.log
"""

import digitalocean
import time

api_key = "your_api_key_from digitalocean"
manager = digitalocean.Manager(token=api_key)
# current_time = time.strftime("%Y-%m-%d %H:%M:%S")
id = 1248252  # VM id, can be found in your admin panel


def vm_object(id):
    my_droplet = manager.get_droplet(id)
    return my_droplet


def power_off(droplet):
    droplet.power_off()
    print '%s - turning off %s...' % (get_ctime(), droplet.name)


def get_status(id):
    my_droplet = manager.get_droplet(id)
    return my_droplet.status


def get_snapshot(droplet):
    droplet.take_snapshot('VM_through_api')
    print ('%s - snapshoting of %s is in progress...'
           % (get_ctime(), droplet.name))


def get_ctime():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    return current_time

my_droplet = vm_object(id)
vm_status = get_status(id)

while vm_status == 'active':
    # print 'I am %s' % vm_status
    power_off(my_droplet)
    time.sleep(8)
    vm_status = get_status(id)
else:
    get_snapshot(my_droplet)

while vm_status == 'off':
    time.sleep(30)
    # print 'I am still snapshoting of %s' % my_droplet.name
    vm_status = get_status(id)
else:
    print ("%s - snapshot of %s is ready with name 'VM_through_api'. "
           "Check it on https://cloud.digitalocean.com/images."
           % (get_ctime(), my_droplet.name))
