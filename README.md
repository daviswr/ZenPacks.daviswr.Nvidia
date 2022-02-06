# ZenPacks.daviswr.Nvidia

ZenPack to monitor Nvidia GPUs on Linux

## Requirements
* Nvidia proprietary drivers for Linux. nouveau is not supported
* An account on the monitored host, which can
  * Log in via SSH with a key
  * Execute the `nvidia-smi` utility
* [ZenPackLib](https://help.zenoss.com/in/zenpack-catalog/open-source/zenpacklib)

## Usage
I'm not going to make any assumptions about your device class organization, so it's up to you to configure the `daviswr.cmd.Nvidia` modeler on the appropriate class or device.

## Special Thanks
* [JRansomed](https://github.com/JRansomed)
