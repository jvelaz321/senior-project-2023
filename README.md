# AI Drone Racing

We used MAVSDK and PYMAVLINK to control our drone.

## Development
- Setup your [environment](https://ardupilot.org/dev/docs/setting-up-sitl-on-linux.html)
- Start SITL
```shell
cd ~/ardupilot/ArduCopter
sim_vehicle.py --console --map --out=127.0.0.1:14551```
```
- Connect GCS to UDP://:14550
- The scripts will use **UDP://:14551**
