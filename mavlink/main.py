import time
import asyncio
from pymavlink import mavutil

async def set_position_ned(vehicle, north, east, down, yaw):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms
        0,       # target system
        0,       # target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
        0b0000111111111000,  # type_mask (ignore all except position)
        north,   # x
        east,    # y
        down,    # z
        0,       # vx
        0,       # vy
        0,       # vz
        0,       # afx
        0,       # afy
        0,       # afz
        yaw,     # yaw
        0        # yaw_rate
    )
    vehicle.send_mavlink(msg)
    await asyncio.sleep(2)

async def run():
    vehicle = mavutil.mavlink_connection('udp:127.0.0.1:14550')

    print("-- Arming")
    vehicle.mav.command_long_send(
        vehicle.target_system, vehicle.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0,
        1, 0, 0, 0, 0, 0, 0
    )

    print("-- Setting initial setpoint")
    await set_position_ned(vehicle, 0.0, 0.0, 0.0, 0.0)

    print("-- Starting offboard")
    vehicle.mav.set_mode_send(
        vehicle.target_system, mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mavutil.mavlink.MAV_MODE_OFFBOARD, 0
    )
    while not vehicle.wait_heartbeat().custom_mode:
        pass

    initial = [-0.10090299999999999, -0.15942, -0.235286]
    print(f"-- Go {initial[0]}m North, {initial[1]}m East, {initial[2]}m Down \
                    within local coordinate system")
    await set_position_ned(vehicle, initial[0], initial[1], initial[2], 45.0)

    # Iterate through each of the points in the coordinates
    for coord in position_data:
        print(f"-- Go {coord[0]}m North, {coord[1]}m East, {coord[2]}m Down \
                within local coordinate system")
        await set_position_ned(vehicle, coord[0], coord[1], coord[2], 0.0)

    # Turn off offboard control
    print("-- Stopping offboard")
    vehicle.mav.set_mode_send(
        vehicle.target_system, mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mavutil.mavlink.MAV_MODE_STABILIZE, 0
    )
    while vehicle.wait_heartbeat().custom_mode != 0:
        pass

if __name__ == "__main__":
    asyncio.run(run())
