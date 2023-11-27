#!/usr/bin/env python3

import asyncio

import mavsdk.action_pb2
from mavsdk import System


async def run():
    drone = System()  # Start the mav server
    await drone.connect(system_address="udp://:14550")  # Connect to the drone

    status_text_task = asyncio.ensure_future(print_status_text(drone))

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    # Set mode to guided


    print("-- Arming")
    await drone.action.arm()

    print("-- Taking off")
    # await drone.action.takeoff()

    # await asyncio.sleep(10)

    print("-- Circle ")
    await drone.action.do_orbit(1.0, 2.0, mavsdk.action_pb2.ORBIT_YAW_BEHAVIOR_HOLD_FRONT_TANGENT_TO_CIRCLE, None, None, None)

    await asyncio.sleep(10)

    print("-- Landing")
    await drone.action.land()

    status_text_task.cancel()


async def print_status_text(drone):
    try:
        async for status_text in drone.telemetry.status_text():
            print(f"Status: {status_text.type}: {status_text.text}")
    except asyncio.CancelledError:
        return


if __name__ == "__main__":
    # Run the asyncio loop
    print("Lesss gooo")
    asyncio.run(run())
