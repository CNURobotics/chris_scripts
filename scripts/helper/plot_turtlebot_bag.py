#!/usr/bin/python
import yaml
import rosbag
import matplotlib.pyplot as plt
import sys
import numpy as np

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

if (len(sys.argv) == 2) and (sys.argv[1] == '--help'):
   print "Usage: plot_bag file_name <\"use_ground_truth\"> <robot namespace> <start_time> <end_time> "
   print "  plot_bag 2015-01-15-10-13-41.bag  0 10.4 20.5"
   print "  optional arguments must be in order "
   print "    set use_ground_truth = 0 for not, 1 for use (default = 0)"
   print "    set robot namespace to the robot's namespace; default = \"turtlebot\""
   print "    set start time to starting time in seconds (default=0)"
   print "    set end time in seconds (default=final time in bag)"
   sys.exit(1)


file_name = 'log.bag'
if (len(sys.argv) > 1):
	file_name = sys.argv[1]

use_ground_truth = False
if (len(sys.argv) > 2):
  if (sys.argv[2] != "0"):
    use_ground_truth = True

robot_name = "turtlebot"
if (len(sys.argv) > 3):
  robot_name = sys.argv[3]

start_time = 0
end_time   = 999999999999.9

if (len(sys.argv) > 4):
	start_time = float(sys.argv[4])

if (len(sys.argv) > 5):
	end_time = float(sys.argv[5])


print "Read bag file ..."
bag = rosbag.Bag(file_name, 'r')

print "Get topic info..."
info_dict = yaml.load(bag._get_yaml_info())
print(info_dict['topics'])

print "Get list ..."
topic_list = []
cmd_msgs = 0
state_msgs = 0

base_node='/'+robot_name+'/'

odom_msgs                 = []
odom_ground_truth_msgs    = [] # odom frame to world ground truth
base_ground_truth_msgs    = [] # base frame to world ground truth
cmd_vel_msgs              = []
pose_msgs                 = [] # Estimated pose messages

time_odom = []
x_odom = []
y_odom = []
z_odom = []
vx_odom = []
wz_odom = []
time_pose = []
x_pose=[]
y_pose=[]

theta_odom_time = []
theta_odom = []
time_gnd = []
x_gnd = []
y_gnd = []
z_gnd = []
x_odom_gnd = []
y_odom_gnd = []
z_odom_gnd = []
theta_gnd_time = []
theta_gnd = []
time_cmd = []
vx_cmd = []
wz_cmd = []

for topic_info in info_dict['topics']:
        topic = topic_info['topic']
        topic_list.append(topic)
        if (topic == base_node+'mobile_base/odom'):
                odom_msgs = topic_info['messages']
        if (topic == base_node+'mobile_base/ground_truth'):
                base_ground_truth_msgs = topic_info['messages']
        if (topic == base_node+'mobile_base/odom_ground_truth'):
                odom_ground_truth_msgs = topic_info['messages']
        if (topic == base_node+'stamped_cmd_vel_mux/output/cmd_vel_stamped'):
            cmd_vel_msgs = topic_info['messages']
        if (topic == base_node+'estimated_pose'):
            pose_msgs = topic_info['messages']


print topic_list

print "Message counts:"
print "  odom msgs        ="+str(  odom_msgs 	)
print "  odom_ground_truth msgs="+str(  odom_ground_truth_msgs 	)
print "  base_ground_truth msgs="+str(  base_ground_truth_msgs 	)
print "  cmd vel msgs      ="+str(  cmd_vel_msgs 	)
print "  pose msgs      ="+str(  pose_msgs 	)

print "Process messages ..."
time_base = -1;
jnt = 16


print "  Process odometry data ..."
if (odom_msgs):
    time_odom = [0 for x in xrange(odom_msgs)]
    x_odom = [0 for x in xrange(odom_msgs)]
    y_odom = [0 for x in xrange(odom_msgs)]
    z_odom = [0 for x in xrange(odom_msgs)]
    vx_odom = [0 for x in xrange(odom_msgs)]
    wz_odom = [0 for x in xrange(odom_msgs)]
    pt = 0
    for topic, msg, t0 in bag.read_messages(topics=base_node+'mobile_base/odom'):
            if (time_base < 0):
                time_base = msg.header.stamp.to_sec()*1.0
                print "time base=",time_base


            time_odom[pt] = (msg.header.stamp.to_sec() - time_base)
            x_odom[pt]    = msg.pose.pose.position.x
            y_odom[pt]    = msg.pose.pose.position.y
            z_odom[pt]    = msg.pose.pose.position.z
            vx_odom[pt]   = msg.twist.twist.linear.x
            wz_odom[pt]   = msg.twist.twist.angular.z

            pt = pt + 1

    end_time = min(end_time, max(time_odom))
    print "Odom start time ="+str(min(time_odom))
    print "Set end time ="+str(end_time)


if (base_ground_truth_msgs):
    time_gnd = [0 for x in xrange(base_ground_truth_msgs)]
    x_gnd = [0 for x in xrange(base_ground_truth_msgs)]
    y_gnd = [0 for x in xrange(base_ground_truth_msgs)]
    z_gnd = [0 for x in xrange(base_ground_truth_msgs)]
    # ground truth
    pt = 0
    for topic, msg, t0 in bag.read_messages(topics=base_node+'mobile_base/ground_truth'):
            time_gnd[pt] = (msg.header.stamp.to_sec() - time_base)
            x_gnd[pt]    = msg.pose.pose.position.x
            y_gnd[pt]    = msg.pose.pose.position.y
            z_gnd[pt]    = msg.pose.pose.position.z

            pt = pt + 1

if (odom_ground_truth_msgs):
    time_odom_gnd = [0 for x in xrange(odom_ground_truth_msgs)]
    x_odom_gnd = [0 for x in xrange(odom_ground_truth_msgs)]
    y_odom_gnd = [0 for x in xrange(odom_ground_truth_msgs)]
    z_odom_gnd = [0 for x in xrange(odom_ground_truth_msgs)]
    # ground truth
    pt = 0
    for topic, msg, t0 in bag.read_messages(topics=base_node+'mobile_base/odom_ground_truth'):
            time_odom_gnd[pt] = (msg.header.stamp.to_sec() - time_base)
            x_odom_gnd[pt]    = msg.pose.pose.position.x
            y_odom_gnd[pt]    = msg.pose.pose.position.y
            z_odom_gnd[pt]    = msg.pose.pose.position.z

            pt = pt + 1

if (cmd_vel_msgs):
    time_cmd = [0 for x in xrange(cmd_vel_msgs)]
    vx_cmd = [0 for x in xrange(cmd_vel_msgs)]
    wz_cmd = [0 for x in xrange(cmd_vel_msgs)]
    # cmd vel
    pt = 0
    for topic, msg, t0 in bag.read_messages(topics=base_node+'stamped_cmd_vel_mux/output/cmd_vel_stamped'):
            time_cmd[pt] = (msg.header.stamp.to_sec() - time_base)
            vx_cmd[pt]   = msg.twist.linear.x
            wz_cmd[pt]   = msg.twist.angular.z

            pt = pt + 1

    print "Cmd start time ="+str(min(time_cmd))
    print "Cmd end time ="+str(max(time_cmd))

if (pose_msgs):
    time_pose = [0 for x in xrange(pose_msgs)]
    x_pose    = [0 for x in xrange(pose_msgs)]
    y_pose    = [0 for x in xrange(pose_msgs)]
    # estimated pose data
    pt = 0
    for topic, msg, t0 in bag.read_messages(topics=base_node+'estimated_pose'):
            time_pose[pt] = (msg.header.stamp.to_sec() - time_base)
            x_pose[pt]    = msg.pose.pose.position.x
            y_pose[pt]    = msg.pose.pose.position.y

            pt = pt + 1

    print "Pose start time ="+str(min(time_pose))
    print "Pose end time ="+str(max(time_pose))
else:
    x_pose

print "Close bag!"
bag.close()





if (odom_msgs):
    print "  Plot odometry  ..."
    fig_odom = plt.figure()
    ax_odom = fig_odom.add_subplot(111, aspect='equal')
    ax_odom.plot(x_odom,y_odom,'g')
    ax_odom.axis([min(x_odom)-0.2, max(x_odom)+0.2,
                  min(y_odom)-0.2, max(y_odom)+0.2 ])
    ax_odom.set_ylabel('x')
    ax_odom.set_xlabel('y')
    ax_odom.legend(['odometry'])
    fig_odom.suptitle("Odometry Path")

if (base_ground_truth_msgs):
    print "  Plot odom frame in ground truth  ..."
    fig_gnd = plt.figure()
    ax_gnd = fig_gnd.add_subplot(111, aspect='equal')
    ax_gnd.plot(x_gnd,y_gnd,'b')
    ax_gnd.axis([min(x_gnd)-0.2, max(x_gnd)+0.2,
                 min(y_gnd)-0.2, max(y_gnd)+0.2 ])
    ax_gnd.set_ylabel('x')
    ax_gnd.set_xlabel('y')
    ax_gnd.legend(['ground truth (simulation)'])
    fig_gnd.suptitle("Actual Displacement")

if (pose_msgs):
    print "  Plot odometry  ..."
    fig_pose = plt.figure()
    ax_pose = fig_pose.add_subplot(111, aspect='equal')
    ax_pose.plot(x_pose,y_pose,'g')
    ax_pose.axis([min(x_pose)-0.2, max(x_pose)+0.2,
                  min(y_pose)-0.2, max(y_pose)+0.2 ])
    ax_odom.set_ylabel('x')
    ax_odom.set_xlabel('y')
    ax_odom.legend(['pose'])
    fig_pose.suptitle("Mapping-based Localization")


if (odom_msgs and (base_ground_truth_msgs or pose_msgs)):
    print "  Plot odom frame with other estimates  ..."
    fig_gnd = plt.figure()
    ax_gnd = fig_gnd.add_subplot(111, aspect='equal')
    ax_gnd.hold(True)
    ax_gnd.plot(x_odom,y_odom,'g')

    legend_text = ['odometry']

    xmin0= min(x_odom)-0.2
    xmax0= max(x_odom)+0.2
    ymin0= min(y_odom)-0.2
    ymax0= max(y_odom)+0.2
    if (base_ground_truth_msgs):
        ax_gnd.plot(x_gnd,y_gnd,'b:')
        legend_text.append('ground truth (simulation)')
        xmin0= min([min(x_gnd),xmin0])-0.2
        xmax0= max([max(x_gnd),xmin0])+0.2
        ymin0= min([min(y_gnd),ymin0])-0.2
        ymax0= max([max(y_gnd),ymin0])+0.2

    if (pose_msgs):
        ax_gnd.plot(x_pose,y_pose,'r:')
        legend_text.append('mapping')
        xmin0= min([min(x_pose),xmin0])-0.2
        xmax0= max([max(x_pose),xmin0])+0.2
        ymin0= min([min(y_pose),ymin0])-0.2
        ymax0= max([max(y_pose),ymin0])+0.2

    print "[min([min(x_gnd,min(x_odom))])-0.2, max([max(x_gnd,max(x_odom))])+0.2,\
                 min([min(y_gnd,min(y_odom))])-0.2, max([max(y_gnd,max(y_odom))])+0.2]=",\
                 [xmin0, xmax0, ymin0, ymax0]

    ax_gnd.axis([xmin0, xmax0, ymin0, ymax0])
    ax_gnd.set_ylabel('x')
    ax_gnd.set_xlabel('y')
    ax_gnd.legend(legend_text)
    fig_gnd.suptitle("Displacement")

if (odom_ground_truth_msgs):
    print "  Plot odom frame in ground truth  ..."
    fig_odom_gnd = plt.figure()
    ax_gnd = fig_odom_gnd.add_subplot(111, aspect='equal')
    ax_gnd.plot(x_odom_gnd,y_odom_gnd,'r')
    ax_gnd.axis([min(x_odom_gnd)-0.2, max(x_odom_gnd)+0.2,
                 min(y_odom_gnd)-0.2, max(y_odom_gnd)+0.2 ])
    ax_gnd.set_ylabel('x')
    ax_gnd.set_xlabel('y')
    ax_gnd.legend(['ground truth of odom frame to world (simulation)'])
    fig_odom_gnd.suptitle("Odom Frame Displacement")


if (cmd_vel_msgs):
    print "  Plot commands ..."
    tmin0 = min([min(time_cmd),min(time_odom)])-0.2
    tmax0 = max([max(time_cmd),max(time_odom)])+0.2
    vxmin0= min([min(vx_cmd),  min(vx_odom) ] )-0.2
    vxmax0= max([max(vx_cmd),  max(vx_odom) ] )+0.2
    wzmin0= min([min(wz_cmd),  min(wz_odom) ] )-0.2
    wzmax0= max([max(wz_cmd),  max(wz_odom) ] )+0.2

    print "  tmin=",str(tmin0),"  tmax=",str(tmax0)

    fig_cmd = plt.figure()
    ax_cmd = fig_cmd.add_subplot(211)
    ax_cmd.hold(True)
    ax_cmd.plot(time_odom,vx_odom,'r')
    ax_cmd.plot(time_cmd,vx_cmd,'g*')
    ax_cmd.axis([tmin0, tmax0, vxmin0, vxmax0])

    ax_cmd.set_ylabel('m/s')
    ax_cmd.set_xlabel('time')
    ax_cmd.legend(['vx_actual (m/s)', 'vx_cmd (m/s)'])

    ax_cmd = fig_cmd.add_subplot(212)
    ax_cmd.hold(True)
    ax_cmd.plot(time_odom,wz_odom,'r')
    ax_cmd.plot(time_cmd,wz_cmd,'g*')
    ax_cmd.axis([tmin0, tmax0, wzmin0, wzmax0])
    ax_cmd.set_ylabel('rad/s')
    ax_cmd.set_xlabel('time')
    ax_cmd.legend(['wz_actual (rad/s)', 'wz_cmd (rad/s)'])
    fig_cmd.suptitle("Commands")


print "Show plot..."
plt.show()
