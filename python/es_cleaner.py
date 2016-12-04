"""
This script uses Elasticsearch API for cleaning big indices.
He finds all indecies and removes biggest one (bigger than normal_size value)
if disk space is used for more than 85%. Free disk space is counted by df
bash command.
"""

import elasticsearch
import subprocess
import operator
import syslog
import time


# Creating dictionary with name of indices as key and size as value
def dic_indices_func(client):
    es_request = client.indices.stats(metric='store')['indices']
    all_indices = es_request.keys()
    dic_indices = {}

    for index in all_indices:
        size_in_bytes = (es_request[index]['primaries']
                         ['store']['size_in_bytes'])
        dic_indices[index] = size_in_bytes

    return dic_indices


# Checking free space
def disk_space(path):
    df = subprocess.Popen(["df", path], stdout=subprocess.PIPE)
    output = df.communicate()[0]
    device, size, used, available, percent, mountpoint = \
        output.split("\n")[1].split()

    percent = int(percent[:-1])
    return percent


# main code
def main():
    client = elasticsearch.Elasticsearch()
    dic_indices = dic_indices_func(client)
    disk_space_percent = disk_space('/data')
    # We are not going to remove indices which size are less than 2gb
    # This is 2GB in bytes
    normal_size_index = 2147483648

    while disk_space_percent > 85 and dic_indices:
        max_size_index = max(dic_indices.iteritems(),
                             key=operator.itemgetter(1))[0]

        if dic_indices[max_size_index] > normal_size_index:
            client.indices.delete(index=max_size_index)
            time.sleep(4)
            disk_space_percent = disk_space('/data')
            syslog.syslog(syslog.LOG_INFO, "index {} was removed for "
                          "cleaning disk space".format(max_size_index))
            '''
            Debugging
            print "-" * 20
            print max_size_index, dic_indices[max_size_index]
            print disk_space_percent
            '''

        del dic_indices[max_size_index]


if __name__ == "__main__":
    main()
