#!/usr/bin/env python

import os
import sys
import rosbag
import datetime
import matplotlib.pyplot as plt
import time
from PIL import Image

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

# TOPICS = [
#     '/msd/vehicle_reporter/vehicle_status'
# ]

# TOPICS = [
#     '/perception/fusion/od'
# ]

# TOPICS = [
#     '/perception/lidar/od'
# ]

# TOPICS = [
#     '/msd/endpoint/control_command'
# ]#throttle brake and steering

# TOPICS = [
#     '/vehicle/dbw_status'
# ]

# TOPICS = [
#     '/mla/sensor/imu'
# ]

TOPICS = [
    '/perception/radar/result_front'
]


class ros_reader():
    def __init__(self):
        print("start")


    def read_perception_msgs(self, input_bag_path):

        tl = []
        msg_x_position = []
        msg_x_speed = []
        id = []

        inbag = rosbag.Bag(input_bag_path, 'r')
        # print(inbag.get_type_and_topic_info())
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


            if int(t_ms) >= 0 and int(t_ms) < 500 and ms_larger == False:
                ms_larger = True
                # continue
            elif int(t_ms) >= 500 and ms_larger == True:
                ms_larger = False

            else:
                continue

            # if topic == "/perception/fusion/od":
            #     draw_perception = True
            for i in range(len(msg.perception_fusion_objects.perception_fusion_objects_data)):
                # if i==0:
                #     temp_mag = []
                #write the files below
                # f.writelines("id is:{}\n".format(msg.perception_fusion_objects.perception_fusion_objects_data[i].track_id))
                # f.write("x:{}\ny:{}\n".format(msg.perception_fusion_objects.perception_fusion_objects_data[i].relative_position.x, msg.perception_fusion_objects.perception_fusion_objects_data[i].relative_position.y))
                # f.write("x_velocity:{}\ny_velocity:{}\n".format(msg.perception_fusion_objects.perception_fusion_objects_data[i].relative_velocity.x, msg.perception_fusion_objects.perception_fusion_objects_data[i].relative_velocity.y))
                if abs(msg.perception_fusion_objects.perception_fusion_objects_data[i].relative_position.y) < 1 and msg.perception_fusion_objects.perception_fusion_objects_data[i].relative_position.x > 0:
                    # print(msg.perception_fusion_objects.perception_fusion_objects_data[i].track_id)
                    # if len(tl) > 0:#skip the objs at the same time 
                    #     if tl[-1] == tM+tS+str(t_ms):
                    #         break
                    # print(msg.perception_fusion_objects.perception_fusion_objects_data[i].relative_position.y)
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
            # fwritelines(str(msg))
            # f.close()
        # if draw_perception == True:
        plt.title("the front car's longitudinal position changing with time\nstart time is 47:00")
        plt.plot(tl, msg_x_position, marker="*", color = "b", label = "the front car's longitudinal position/m")

        plt.annotate("took over", xy = ("59:0", 17.0), xytext = ("59:0",30.0), arrowprops = dict(facecolor='black', shrink=0.01))
        plt.legend()
        figsize = 9, 9
        # figure, ax = plt.subplots(figsize=figsize)
        font2 = {'family' : 'Times New Roman',
        'weight' : 'normal',
        'size' : 30,
        }
        plt.tick_params(axis='both',which='major',rotation = 45, labelsize=6)
        # labels = ax.get_xticklabels() + ax.get_yticklabels()
        # print labels
        # [label.set_fontname('Times New Roman') for label in labels]
        plt.xlabel('time')
        plt.ylabel('longitudinal position')
        for a, b, c in zip(tl, msg_x_position, id):
            # plt.text(a, b, round(b,1), ha='center', va='bottom', fontsize=16)
            plt.text(a, b+2, c, ha='center', va='bottom', fontsize=6, color = "r")
        plt.savefig("/home/allen/Desktop/01-software/code/position/test_position.png", dpi=300)
        plt.show()
        plt.title("the front car's longitudinal speed changing with time\nstart time is 47:00")
        plt.plot(tl, msg_x_speed, marker="*", color = "b", label = "the front car's longitudinal speed/m/s")
        plt.annotate("took over", xy = ("59:0", -6), xytext = ("59:0",-5), arrowprops = dict(facecolor='black', shrink=0.01))
        plt.legend()
        plt.tick_params(axis='both',which='major',rotation = 45, labelsize=6)
        plt.xlabel('time')
        plt.ylabel('longitudinal speed')
        for a, b, c in zip(tl, msg_x_speed, id):
            # plt.text(a, b, round(b,1), ha='center', va='bottom', fontsize=16)
            plt.text(a, b+0.1, c, ha='center', va='bottom', fontsize=6, color = "r")
        plt.savefig("/home/allen/Desktop/01-software/code/position/test_speed.png", dpi=300)
        plt.show()
        p1 = Image.open("/home/allen/Desktop/01-software/code/position/test_position.png")
        p2 = Image.open("/home/allen/Desktop/01-software/code/position/test_speed.png")
        result = Image.new(p1.mode, (1920, 1440*2))
        result.paste(p1, box=(0,0))
        result.paste(p2, box=(0,1440))
        result.save("/home/allen/Desktop/01-software/code/position/combined.png")


    def check_topic(self, input_bag_path):
        inbag = rosbag.Bag(input_bag_path, 'r')
        print(inbag.get_type_and_topic_info())
        accz2=[]
        tl2 = []
        tl1 = []
        accz1 = []
        ms_larger = False
        for topic, msg, t in inbag.read_messages(topics=TOPICS):
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
            # print(t3)
            # t4 = getdate2(t)
            # filename=os.path.join(os.getcwd(),'position',str(t3)+":"+str(t_ms)+'.txt')
            # print(filename)


            if int(t_ms) >= 0 and int(t_ms) < 500 and ms_larger == False:
                ms_larger = True
                # continue
            elif int(t_ms) >= 500 and ms_larger == True:
                ms_larger = False

            else:
                continue

            if topic == "/mla/sensor/imu":
                if len(accz2) == 0:
                    accz2.append(msg.info.imu_data_basic.accz)
                    tl2.append(self.getdate2(t))
                elif len(accz2) ==1:
                    if accz2[0] < msg.info.imu_data_basic.accz:
                        accz2.append(msg.info.imu_data_basic.accz)
                        tl2.append(self.getdate2(t))
                    else:
                        accz2.insert(0, msg.info.imu_data_basic.accz)
                        tl2.insert(0, self.getdate2(t))
                else:#pick the smallest and biggest one
                    if accz2[0] > msg.info.imu_data_basic.accz:#smaller
                        accz2.pop(0)
                        tl2.pop(0)
                        accz2.insert(0,msg.info.imu_data_basic.accz)
                        tl2.insert(0, self.getdate2(t))
                    elif accz2[1] < msg.info.imu_data_basic.accz:#bigger
                        accz2.pop()
                        tl2.pop()
                        accz2.append(msg.info.imu_data_basic.accz)
                        tl2.append(self.getdate2(t))

                tl1.append(tS+":"+tms)
                accz1.append(round(msg.info.imu_data_basic.accz, 2))

        print(accz2[1] - accz2[0])
        print(tl2)
        print("good")

        plt.title("imu status on z axis: m/s2")
        plt.plot(tl1, accz1, marker="*", color = "b", label = "ims status: m/s2")

        # plt.annotate("took over", xy = ("59:0", 17.0), xytext = ("59:0",30.0), arrowprops = dict(facecolor='black', shrink=0.01))
        plt.legend()
        figsize = 9, 9
        # figure, ax = plt.subplots(figsize=figsize)
        font2 = {'family' : 'Times New Roman',
        'weight' : 'normal',
        'size' : 30,
        }
        plt.tick_params(axis='both',which='major',rotation = 45, labelsize=6)
        # labels = ax.get_xticklabels() + ax.get_yticklabels()
        # print labels
        # [label.set_fontname('Times New Roman') for label in labels]
        plt.xlabel('time')
        plt.ylabel('imu z axis status')
        for a, b, c in zip(tl1, accz1, accz1):
            # plt.text(a, b, round(b,1), ha='center', va='bottom', fontsize=16)
            plt.text(a, b+0.015, c, ha='center', va='bottom', fontsize=6, color = "r")
        plt.savefig("/home/allen/Desktop/01-software/code/position/test_imu.png", dpi=300)
        plt.show()

            # print(topic)

            # print(msg.info.imu_data_basic.accz)
            # tl.append(str(t))
            # accz.append(msg.info.imu_data_basic.accz)
            # t1=int(str(t))/1000000000
            # # t1=int(str(t))/1000000
            # t2=datetime.datetime.fromtimestamp(t1)
            
            # tM = t2.strftime('%M')
            # tS = t2.strftime('%S')

            # if int(tS) < 47:
            #     print("skip")
            #     continue
            # if int(tS) >= 52:
            #     break


            # if msg.status == False:#autonoumous status
            #     tt = self.getdate2(t)
            #     print(tt)
            # print('------' * 10)
        # plt.plot(tl, accz, marker="*", color = "b", label = "imu status")
        # plt.tick_params(axis='both',which='major',labelsize=5)

        # plt.xlabel('time')

        # plt.ylabel('imu z axis acc')
        # plt.show()

    def getdate2(self, t="1598506228000"):
        '''时间戳转换为时间'''

        t1=int(str(t))/1000000000
            # t1=int(str(t))/1000000
        t2=datetime.datetime.fromtimestamp(t1)
        t3=t2.strftime('%Y-%m-%d-%H:%M:%S')
        t_ms = int((int(str(t)) - int(t1)*10**9)/10**6)
        tms = str(t_ms)
        t3 = t3 + ":" + tms
        
        return t3



if __name__ == '__main__':
    sys.argv.append("/media/allen/MyPassport/02-data/momenta-bag/20210311-083521.bag")
    if len(sys.argv) != 2:
        print('usage: {} <input_bag>'.format(sys.argv[0]))
        exit(-1)

    if not os.access(sys.argv[1], os.R_OK):
        print('file "{}" cannot be read'.format(sys.argv[1]))
        exit(-1)

    reader = ros_reader()
    # reader.read_perception_msgs(sys.argv[1])
    reader.check_topic(sys.argv[1])

    # print_recorder_msgs(sys.argv[1])
    print("good")