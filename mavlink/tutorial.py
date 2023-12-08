import time

from pymavlink import mavutil

# Start the connection
the_connection = mavutil.mavlink_connection('udpin:localhost:14551')

# Wait for the first heartbeat
# We also set the system id of remote system for the link
the_connection.wait_heartbeat()
print(f"Heartbeart from system (system {the_connection.target_system} component {the_connection.target_component}) ")
north = 5
east = 5
down = -5
# the_connection.mav.command_int_send()
the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, the_connection.target_system,
                                                                                      the_connection.target_component,
                                                                                      mavutil.mavlink.MAV_FRAME_LOCAL_NED,
                                                                                      int(0b010111111000),
                                                                                      north,
                                                                                      east,
                                                                                      down,
                                                                                      0, 0, 0, 0, 0, 0, 1.57, 0.5))

while 1:
    msg = the_connection.recv_match(
        type='LOCAL_POSITION_NED', blocking=True)
    print(msg)

# the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, the_connection.target_system,
#                         the_connection.target_component, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, int(0b110111111000), int(-35.3629849 * 10 ** 7), int(149.1649185 * 10 ** 7), 10, 0, 0, 0, 0, 0, 0, 1.57, 0.5))


# the_connection.mav.command_int_send(the_connection.target_system, the_connection.target_component,
#                                     mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
#                                     mavutil.mavlink.SET_POSITION_TARGET_LOCAL_NED,  # command
#                                     0, 0,  # current, autocontinue
#                                     0b0000111111111000,  # type_mask (only positions enabled)
#                                     0,0,0,
#                                     north, east, down
#                                     # x, y, z positions (or North, East, Down in the MAV_FRAME_BODY_NED frame
#                                     )
# the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
#                                      mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
#
# msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
# print(msg)
#
# the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
#                                      mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 10)
#
# time.sleep(3)
#
# msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
# print(msg)
