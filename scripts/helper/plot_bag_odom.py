#!/usr/bin/python
import yaml
import rosbag
import matplotlib.pyplot as plt
import sys
import numpy as np

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

if (len(sys.argv) == 2) and (sys.argv[1] == '--help'):
   print "Usage: plot_bag file_name> <\"use_ground_truth\"> <start_time> <end_time> "
   print "  plot_bag 2015-01-15-10-13-41.bag  0 10.4 20.5"
   print "    set use_ground_truth = 0 for not, 1 for use"
   sys.exit(1)


file_name = 'log.bag'
if (len(sys.argv) > 1):
	file_name = sys.argv[1]

use_ground_truth = False
if (len(sys.argv) > 2):
  if (sys.argv[1] != "0"):
    use_ground_truth = True

start_time = 0
end_time   = 999999999999.9

if (len(sys.argv) > 3):
	start_time = float(sys.argv[3])

if (len(sys.argv) > 4):
	end_time = float(sys.argv[4])


print "Read bag file ..."
bag = rosbag.Bag(file_name, 'r')

print "Get topic info..."
info_dict = yaml.load(bag._get_yaml_info())
print(info_dict['topics'])

print "Get list ..."
topic_list = []
cmd_msgs = 0
state_msgs = 0

base_node='/create_node/'
odom_msgs                 = []
ground_truth_msgs         = []
ground_truth_euler_msgs   = []
odom_euler_msgs           = []
cmd_vel_msgs           = []
time_odom = []
x_odom = []
y_odom = []
z_odom = []
theta_odom_time = []
theta_odom = []
time_gnd = []
x_gnd = []
y_gnd = []
z_gnd = []
theta_gnd_time = []
theta_gnd = []
time_cmd = []
vx_cmd = []
wz_cmd = []

for topic_info in info_dict['topics']:
        topic = topic_info['topic']
        topic_list.append(topic)
        if (topic == base_node+'odom'):
                odom_msgs = topic_info['messages']
        if (topic == base_node+'ground_truth'):
                ground_truth_msgs = topic_info['messages']
        if (topic == '/robot_odometry/euler'):
                odom_euler_msgs = topic_info['messages']
        if (topic == '/robot_ground_truth/euler'):
                ground_truth_euler_msgs = topic_info['messages']

        if (topic == base_node+'cmd_vel'):
            cmd_vel_msgs = topic_info['messages']


print topic_list

print "Message counts:"
print "  odom msgs        ="+str(  odom_msgs 	)
print "  ground_truth msgs="+str(  ground_truth_msgs 	)
print "  odom euler msgs  ="+str(  odom_euler_msgs 	)
print "  ground_truth euler="+str(  ground_truth_euler_msgs 	)
print "  cmd vel msgs      ="+str(  cmd_vel_msgs 	)

print "Process messages ..."
time_base = -1;
jnt = 16


print "  Process odometry data ..."
if (odom_msgs):
    time_odom = [0 for x in xrange(odom_msgs)]
    x_odom = [0 for x in xrange(odom_msgs)]
    y_odom = [0 for x in xrange(odom_msgs)]
    z_odom = [0 for x in xrange(odom_msgs)]
    pt = 0
    for topic, msg, t0 in bag.read_messages(topics=base_node+'odom'):
            if (time_base < 0):
                time_base = msg.header.stamp.to_sec()
            time_odom[pt] = (msg.header.stamp.to_sec() - time_base)
            x_odom[pt]    = msg.pose.pose.position.x
            y_odom[pt]    = msg.pose.pose.position.y
            z_odom[pt]    = msg.pose.pose.position.z

            pt = pt + 1

    end_time = min(end_time, max(time_odom))
    print "Set end time ="+str(end_time)

if (odom_euler_msgs):
    theta_odom_time = [0 for x in xrange(odom_euler_msgs)]
    theta_odom = [0 for x in xrange(odom_euler_msgs)]
    # odom euler
    pt = 0
    for topic, msg, t0 in bag.read_messages(topics='/robot_odometry/euler'):
            theta_odom_time[pt] = (msg.header.stamp.to_sec() - time_base)
            theta_odom[pt]      = msg.vector.z

            pt = pt + 1


if (ground_truth_msgs):
    time_gnd = [0 for x in xrange(ground_truth_msgs)]
    x_gnd = [0 for x in xrange(ground_truth_msgs)]
    y_gnd = [0 for x in xrange(ground_truth_msgs)]
    z_gnd = [0 for x in xrange(ground_truth_msgs)]
    # ground truth
    pt = 0
    for topic, msg, t0 in bag.read_messages(topics=base_node+'ground_truth'):
            time_gnd[pt] = (msg.header.stamp.to_sec() - time_base)
            x_gnd[pt]    = msg.pose.pose.position.x
            y_gnd[pt]    = msg.pose.pose.position.y
            z_gnd[pt]    = msg.pose.pose.position.z

            pt = pt + 1

if (ground_truth_euler_msgs):
    theta_gnd_time = [0 for x in xrange(ground_truth_euler_msgs)]
    theta_gnd = [0 for x in xrange(ground_truth_euler_msgs)]
    # ground truth euler
    pt = 0
    for topic, msg, t0 in bag.read_messages(topics='/robot_ground_truth/euler'):
            theta_gnd_time[pt] = (msg.header.stamp.to_sec() - time_base)
            theta_gnd[pt]      = msg.vector.z

            pt = pt + 1

if (cmd_vel_msgs):
    time_cmd = [0 for x in xrange(cmd_vel_msgs)]
    vx_cmd = [0 for x in xrange(cmd_vel_msgs)]
    wz_cmd = [0 for x in xrange(cmd_vel_msgs)]
    # cmd vel
    pt = 0
    for topic, msg, t0 in bag.read_messages(topics=base_node+'cmd_vel'):
            time_cmd[pt] = (msg.header.stamp.to_sec() - time_base)
            vx_cmd[pt]      = msg.twist.linear.x
            wz_cmd[pt]      = msg.twist.angular.z

            pt = pt + 1


print "Close bag!"
bag.close()



   

if (odom_msgs):# and ground_truth_msgs):
#    print "  Plot odometry vs. ground truth ..."
#    fig_odom = plt.figure()
#    ax_odom = fig_odom.add_subplot(111, aspect='equal')
#    ax_odom.plot(x_gnd,y_gnd,'r', x_odom,y_odom,'b')
#    ax_odom.axis([min([min(x_odom), min(x_gnd)])-0.2, max([max(x_odom), max(x_gnd)])+0.2,
#                      min([min(y_odom), min(y_gnd)])-0.2, max([max(y_odom), max(y_gnd)])+0.2 ])
#    ax_odom.set_ylabel('x')
#    ax_odom.set_xlabel('y')
#    ax_odom.legend(['ground truth','odometry'])
#    fig_odom.suptitle("Path")
#elif (odom_msgs ):
    print "  Plot odometry  ..."
    fig_odom = plt.figure()
    ax_odom = fig_odom.add_subplot(111, aspect='equal')
    ax_odom.plot(x_odom,y_odom,'g')
    ax_odom.axis([min(x_odom)-0.2, max(x_odom)+0.2,
                  min(y_odom)-0.2, max(y_odom)+0.2 ])
    ax_odom.set_ylabel('x')
    ax_odom.set_xlabel('y')
    ax_odom.legend(['odometry'])
    fig_odom.suptitle("Path")

if (ground_truth_msgs):
    print "  Plot odom frame in ground truth  ..."
    fig_gnd = plt.figure()
    ax_gnd = fig_gnd.add_subplot(111, aspect='equal')
    ax_gnd.plot(x_gnd,y_gnd,'g')
    ax_gnd.axis([min(x_gnd)-0.2, max(x_gnd)+0.2,
                 min(y_gnd)-0.2, max(y_gnd)+0.2 ])
    ax_gnd.set_ylabel('x')
    ax_gnd.set_xlabel('y')
    ax_gnd.legend(['ground truth (simulation)'])
    fig_gnd.suptitle("Displacement")

if (cmd_vel_msgs):
    print "  Plot commands ..."
    fig_cmd = plt.figure()
    ax_cmd = fig_cmd.add_subplot(211)
    ax_cmd.plot(time_cmd,vx_cmd,'r')
    ax_cmd.axis([min(time_cmd), max(time_cmd),
                 min(vx_cmd)-0.005, max(vx_cmd)+0.005 ])
    ax_cmd.set_ylabel('m/s')
    ax_cmd.set_xlabel('time')
    ax_cmd.legend(['vx_cmd (m/s)'])
    ax_cmd = fig_cmd.add_subplot(212)
    ax_cmd.plot(time_cmd,wz_cmd,'b')
    ax_cmd.axis([min(time_cmd), max(time_cmd),
                  min(wz_cmd)-0.005, max(wz_cmd)+0.005 ])
    ax_cmd.set_ylabel('rad/s')
    ax_cmd.set_xlabel('time')
    ax_cmd.legend(['wz_cmd (m/s)'])
    fig_cmd.suptitle("Commands")


print "Show plot..."
plt.show()



