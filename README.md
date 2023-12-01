# AI Drone Racing

We used MAVSDK and PYMAVLINK to control our drone.

## Development
- Setup your [environment](https://ardupilot.org/dev/docs/setting-up-sitl-on-linux.html)
- Start SITL
```shell
cd ~/ardupilot/ArduCopter
sim_vehicle.py --console --map --out=127.0.0.1:14551
```
- Connect GCS to UDP://:14550
- The scripts will use **UDP://:14551**
### Adding an Optical Flow sensor

A virtual optical flow sensor can be added enabling a RangeFinder (see “Adding a Rangefinder” above) and then setting these parameters:
```
param set SIM_FLOW_ENABLE 1
param set FLOW_TYPE 10
```




### Disable GPS
Inside of MAVPROXY run the following to disable arming checks
```shell
arm safetyoff
arm uncheck all
arm throttle
```

## Gazebo
First install some necessary tools:
```shell
sudo apt-get update
sudo apt-get install lsb-release wget gnupg
```

Then install Gazebo Garden:
```shell
sudo wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
sudo apt-get update
sudo apt-get install gz-garden
```

#### Gazebo Plugin install


Install additional dependencies
```shell
sudo apt update
sudo apt install libgz-sim7-dev rapidjson-dev
```

Create a workspace folder and clone the repository
```shell
mkdir -p gz_ws/src && cd gz_ws/src
git clone https://github.com/ArduPilot/ardupilot_gazebo
```

Build the plugin
```shell
cd ardupilot_gazebo
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo
make -j4
```

Export env vars
```shell
echo 'export GZ_SIM_SYSTEM_PLUGIN_PATH=$HOME/gz_ws/src/ardupilot_gazebo/build:${GZ_SIM_SYSTEM_PLUGIN_PATH}' >> ~/.bashrc
echo 'export GZ_SIM_RESOURCE_PATH=$HOME/gz_ws/src/ardupilot_gazebo/models:$HOME/gz_ws/src/ardupilot_gazebo/worlds:${GZ_SIM_RESOURCE_PATH}' >> ~/.bashrc
```

Test
```shell
sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON --map --console
```
