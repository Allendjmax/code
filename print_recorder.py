#!/usr/bin/env python

import os
import sys
import rosbag
import datetime
import matplotlib.pyplot as plt
import time

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

# TOPICS = [
#     '/msd/vehicle_reporter/vehicle_status'
# ]

TOPICS = [
    '/perception/fusion/od'
]


def print_recorder_msgs(input_bag_path):

    tl = []
    msg_x_position = []
    msg_x_speed = []
    id = []
    
    inbag = rosbag.Bag(input_bag_path, 'r')
    print(inbag.get_type_and_topic_info())
    ms_larger = False
    if not os.path.exists('position'):
        os.makedirs('position')
    for topic, msg, t in inbag.read_messages(topics=TOPICS):
        # print(msg)
        # print('------' * 10)
        t1=int(str(t))/1000000000
        # t1=int(str(t))/1000000
        t2=datetime.datetime.fromtimestamp(t1)
        t3=t2.strftime('%Y-%m-%d-%H:%M:%S')
        t4 = t2.strftime('%M%S')
        tM = t2.strftime('%M')
        tS = t2.strftime('%S')
        t_ms = int((int(str(t)) - int(t1)*10**9)/10**6)

        if int(tM) >= 34 or int(tS) < 47:
            continue

        #choose 33m47s00ms as start point
        tM = str(int(tM) - 33)
        # tS = str(int(tS) - 47)
        tms = str(int(t_ms/100))

        # t2=time.gmtime(t1)
        print(t3)
        # t4 = getdate2(t)
        filename=os.path.join(os.getcwd(),'position',str(t3)+":"+str(t_ms)+'.txt')
        print(filename)
        

        if int(t_ms) > 0 and int(t_ms) < 500 and ms_larger == False:
            ms_larger = True
            # continue
        elif int(t_ms) >= 500 and ms_larger == True:
            ms_larger = False

        else:
            continue


        for i in range(len(msg.perception_fusion_objects.perception_fusion_objects_data)):
            # if i==0:
            #     temp_mag = []

            #write the files below
            # f.writelines("id is:{}\n".format(msg.perception_fusion_objects.perception_fusion_objects_data[i].track_id))
            # f.write("x:{}\ny:{}\n".format(msg.perception_fusion_objects.perception_fusion_objects_data[i].relative_position.x, msg.perception_fusion_objects.perception_fusion_objects_data[i].relative_position.y))
            # f.write("x_velocity:{}\ny_velocity:{}\n".format(msg.perception_fusion_objects.perception_fusion_objects_data[i].relative_velocity.x, msg.perception_fusion_objects.perception_fusion_objects_data[i].relative_velocity.y))
            if abs(msg.perception_fusion_objects.perception_fusion_objects_data[i].relative_position.y) < 1 and msg.perception_fusion_objects.perception_fusion_objects_data[i].relative_position.x > 0:
                print(msg.perception_fusion_objects.perception_fusion_objects_data[i].track_id)
                # if len(tl) > 0:#skip the objs at the same time 
                #     if tl[-1] == tM+tS+str(t_ms):
                #         break

                
                print(msg.perception_fusion_objects.perception_fusion_objects_data[i].relative_position.y)
                print("found")

                tl.append(tS+":"+tms)
                msg_x_speed.append(msg.perception_fusion_objects.perception_fusion_objects_data[i].relative_velocity.x)
                id.append(msg.perception_fusion_objects.perception_fusion_objects_data[i].track_id)
                msg_x_position.append(msg.perception_fusion_objects.perception_fusion_objects_data[i].relative_position.x)
                if len(tl) > 1:
                    if tl[-2] == tS+":"+tms:
                        tl.pop()
                        id.pop()
                        if msg_x_position[-1] < msg_x_position[-2]:#pick the closer one's position and speed
                            msg_x_position.pop(-2)
                            msg_x_speed.pop(-2)
                        else:
                            msg_x_position.pop(-1)
                            msg_x_speed.pop(-1)
                    # if msg.perception_fusion_objects.perception_fusion_objects_data[i].relative_position.x < msg.perception_fusion_objects.perception_fusion_objects_data[i-1].relative_position.x:
                        # msg_x_position.pop()
                        # msg_x_position.append(msg.perception_fusion_objects.perception_fusion_objects_data[i].relative_position.x)

                
        
        # f.writelines(str(msg))
        # f.close()

    
    plt.title("the front car's longitudinal position changing with time\nstart time is 47:00")
    plt.plot(tl, msg_x_position, marker="*", color = "b", label = "the front car's longitudinal position/m")
    plt.legend()

    font2 = {'family' : 'Times New Roman',
    'weight' : 'normal',
    'size' : 30,
    }
    plt.tick_params(labelsize=8)

    plt.xlabel('time')

    plt.ylabel('longitudinal position')

    for a, b, c in zip(tl, msg_x_position, id):
        # plt.text(a, b, round(b,1), ha='center', va='bottom', fontsize=16)
        plt.text(a, b, c, ha='center', va='bottom', fontsize=10, color = "r")
    
    plt.savefig("/home/allen/Desktop/01-software/code/position/test.png", dpi=300)
    plt.show()

    plt.title("the front car's longitudinal speed changing with time\nstart time is 47:00")
    plt.plot(tl, msg_x_speed, marker="*", color = "b", label = "the front car's longitudinal speed/m/s")
    plt.legend()

    plt.xlabel('time')

    plt.ylabel('longitudinal speed')

    for a, b, c in zip(tl, msg_x_speed, id):
        # plt.text(a, b, round(b,1), ha='center', va='bottom', fontsize=16)
        plt.text(a, b, c, ha='center', va='bottom', fontsize=16, color = "r")
    
    plt.savefig("/home/allen/Desktop/01-software/code/position/test_speed.png")
    plt.show()

def getdate2(t="1598506228000"):
    '''时间戳转换为时间'''

    t1 = float(str(t))/1000
    # print(timeStamp)
    t2 = time.localtime(t1)
    # print(timeArray)
    t3 = time.strftime("%Y-%m-%d %H:%M:%S", t2)
    # print(otherStyleTime)
    return t3



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