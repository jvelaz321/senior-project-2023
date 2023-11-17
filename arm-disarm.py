import time
import sys
from pymavlink import mavutil

def setMode(mode, master):
    # Check if mode is available
    if mode not in master.mode_mapping():
        print('Unknown mode : {}'.format(mode))
        print('Try:', list(master.mode_mapping().keys()))
        sys.exit(1)

    # Get mode ID
    mode_id = master.mode_mapping()[mode]
    # Set new mode
    # master.mav.command_long_send(
    #    master.target_system, master.target_component,
    #    mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
    #    0, mode_id, 0, 0, 0, 0, 0) or:
    # master.set_mode(mode_id) or:
    master.mav.set_mode_send(
        master.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id)

    while True:
        # Wait for ACK command
        ack_msg = master.recv_match(type='COMMAND_ACK', blocking=True)
        ack_msg = ack_msg.to_dict()

        # Check if command in the same in `set_mode`
        if ack_msg['command'] != mavutil.mavlink.MAVLINK_MSG_ID_SET_MODE:
            continue

        # Print the ACK result !
        print(mavutil.mavlink.enums['MAV_RESULT'][ack_msg['result']].description)
        break


# Create the connection
#  Companion is already configured to allow script connections under the port 9000
# Note: The connection is done with 'udpout' and not 'udpin'.
#  You can check in http:192.168.1.2:2770/mavproxy that the communication made for 9000
#  uses a 'udp' (server) and not 'udpout' (client).
# master = mavutil.mavlink_connection('udpout:0.0.0.0:9000')
the_connection = mavutil.mavlink_connection('/dev/ttyTHS1', baud=921600)

# Wait for the first heartbeat
# We also set the system id of remote system for the link
the_connection.wait_heartbeat()
print(f"Heartbeart from system (system {the_connection.target_system} component {the_connection.target_component}) ")

# Switch to guided mode
mode = 'GUIDED'
setMode(mode, the_connection)

# Arm
the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)

# Sleep for a couple of seconds
print("Pause 🙊")
time.sleep(2)
print("Resume 😈")

# Disarm
the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)
