#!/usr/bin/env python

import os
import sys
import rosbag

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

# TOPICS = [
#     '/msd/planning/plan'
# ]

TOPICS = [
    '/perception/fusion/od'
]


def print_recorder_msgs(input_bag_path):
    inbag = rosbag.Bag(input_bag_path, 'r')
    print(inbag.get_type_and_topic_info())
    for topic, msg, t in inbag.read_messages(topics=TOPICS):
        print(msg)
        print('------' * 10)
        # break


if __name__ == '__main__':
    sys.argv.append("/media/allen/MyPassport/02-data/momenta-bag/20210311-083521.bag")
    if len(sys.argv) != 2:
        print('usage: {} <input_bag>'.format(sys.argv[0]))
        exit(-1)

    if not os.access(sys.argv[1], os.R_OK):
        print('file "{}" cannot be read'.format(sys.argv[1]))
        exit(-1)

    print_recorder_msgs(sys.argv[1])
    print("good")

