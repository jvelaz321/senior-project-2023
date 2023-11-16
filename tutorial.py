from pymavlink import mavutil

# Start the connection
the_connection = mavutil.mavlink_connection('udpin:localhost:14551')

# Wait for the first heartbeat
the_connection.wait_heartbeat()
print(f"Heartbeart from system (system {the_connection.target_system} component {the_connection.target_component}) ")

the_connection.mav.command