import time

from pymavlink import mavutil

# Start the connection
the_connection = mavutil.mavlink_connection('udpin:localhost:14550')

# Wait for the first heartbeat
# We also set the system id of remote system for the link
the_connection.wait_heartbeat()
print(f"Heartbeart from system (system {the_connection.target_system} component {the_connection.target_component}) ")

the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)

the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 10)

time.sleep(3)

msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)
