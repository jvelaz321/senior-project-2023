#!/usr/bin/env python3

"""
Caveat when attempting to run the examples in non-gps environments:

`drone.offboard.stop()` will return a `COMMAND_DENIED` result because it
requires a mode switch to HOLD, something that is currently not supported in a
non-gps environment.
"""

import asyncio

from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)

# Position coordinates
position_data = [[0.0, 0.0, 0.0], [-0.00100903, -0.0015942, 0.00235286], [-0.0010074, -0.00158939, 0.00333386],
                 [-0.0009995400000000002, -0.0015749700000000002, 0.00431479],
                 [-0.0009825999999999997, -0.0015498299999999994, 0.0052955499999999996],
                 [-0.0009524399999999997, -0.00151177, 0.006275959999999999],
                 [-0.0009070800000000002, -0.0014604200000000005, 0.007255750000000002],
                 [-0.0008433500000000005, -0.0013959899999999997, 0.008234660000000001],
                 [-0.0007604700000000001, -0.0013184400000000006, 0.00921238],
                 [-0.0006604100000000002, -0.0012311800000000001, 0.010131149999999998],
                 [-0.0005363599999999996, -0.0011302399999999994, 0.011105629999999998],
                 [-0.0003994900000000006, -0.0010261200000000002, 0.011963870000000001],
                 [-0.0002480899999999994, -0.0009139299999999986, 0.012804220000000005],
                 [-7.278999999999966e-05, -0.0007849300000000031, 0.01377312],
                 [0.00010761999999999924, -0.0006545299999999969, 0.014691469999999998],
                 [0.00029642000000000036, -0.0005210300000000022, 0.015598340000000002],
                 [0.0004971899999999998, -0.00037972999999999826, 0.016563930000000004],
                 [0.0006839000000000003, -0.0002514300000000004, 0.017357999999999985],
                 [0.0008881499999999999, -0.00011567999999999995, 0.018323630000000007],
                 [0.00106996, 2.999999999808711e-08, 0.019116880000000003],
                 [0.00126011, 0.0001160200000000014, 0.020085169999999986],
                 [0.0014364200000000003, 0.00021805000000000088, 0.021055550000000006],
                 [0.0015957599999999999, 0.00030092999999999787, 0.022028360000000025],
                 [0.00173458812, 0.00036029599999999953, 0.023003479999999965],
                 [0.00185209188, 0.00039097400000000226, 0.023970760000000035],
                 [0.0019455400000000004, 0.0003894499999999995, 0.024949489999999963],
                 [0.0020104499999999996, 0.00035311000000000023, 0.025929140000000017],
                 [0.0020436199999999995, 0.00028034999999999866, 0.026908500000000002],
                 [0.0020441, 0.00016856000000000163, 0.02785726999999999],
                 [0.002010620000000001, 1.8749999999997935e-05, 0.028761829999999988],
                 [0.0019383199999999986, -0.00018083999999999809, 0.029731300000000016],
                 [0.0018343400000000003, -0.0004064299999999993, 0.030550599999999983],
                 [0.0016890399999999993, -0.0006777100000000015, 0.03139404000000001],
                 [0.0014973799999999995, -0.001000789999999998, 0.032289360000000045],
                 [0.001272910000000002, -0.0013509100000000003, 0.03309812999999995],
                 [0.0010173599999999984, -0.0017229200000000028, 0.033816640000000064],
                 [0.000685810000000002, -0.002179579999999997, 0.034712429999999905],
                 [0.00033783000000000077, -0.0026328500000000025, 0.03543230000000008],
                 [-3.227000000000091e-05, -0.003092519999999998, 0.036038860000000006],
                 [-0.00043711000000000097, -0.00357416, 0.036595839999999935],
                 [-0.0008260799999999999, -0.004019189999999999, 0.03693495000000002],
                 [-0.0012922499999999983, -0.0045305100000000015, 0.03737394999999999],
                 [-0.0017362500000000017, -0.004998530000000001, 0.03761345999999999]]


async def run():
    """ Does Offboard control using position NED coordinates. """

    drone = System()
    await drone.connect(system_address="udp://:14551")

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

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed \
                with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    # Iterate through each of the points in the coordinates
    for coord in position_data:
        print(f"-- Go {coord[0]}m North, {coord[1]}m East, {coord[2]}m Down \
                within local coordinate system")
        await drone.offboard.set_position_ned(
            PositionNedYaw({coord[0]}, {coord[1]}, {coord[2]}, 0.0)) # TODO: Change the yaw to the most optimal angle.

    # Pause
    await asyncio.sleep(10)

    # Turn off offboard control
    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed \
                with error code: {error._result.result}")


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())
