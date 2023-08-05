# tlnetcard_python [![Build Status](https://travis-ci.com/EGuthrieWasTaken/tlnetcard_python.svg?token=LUrGqUz1JQxq9JLRjGmk&branch=master)](https://travis-ci.com/EGuthrieWasTaken/tlnetcard_python) ![PyPI](https://img.shields.io/pypi/v/tlnetcard-python) ![PyPI - License](https://img.shields.io/pypi/l/tlnetcard-python) ![PyPI - Status](https://img.shields.io/pypi/status/tlnetcard-python)

Welcome to tlnetcard_python! tlnetcard_python is a Python 3 API for the TLNET Supervisor web interface which is used with Tripp Lite's [TLNETCARD](https://www.tripplite.com/support/TLNETCARD), and aims to provide similar functionality in a scriptable format. This API makes frequent use of the [requests](https://github.com/psf/requests) module, and I recommend it for use in any projects which involve making HTML requests in Python. A second thank you goes to the people behind the [selenium](https://github.com/SeleniumHQ/selenium) and [PySNMP](https://github.com/etingof/pysnmp) modules respectively, of which this API makes intermittent use.

## Installation [![Downloads](https://pepy.tech/badge/tlnetcard-python)](https://pepy.tech/project/tlnetcard-python) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tlnetcard-python) ![PyPI - Format](https://img.shields.io/pypi/format/tlnetcard-python)

This package is installed using pip. If you do not have pip installed on your system, you can install it by downloading [get-pip.py](https://pip.pypa.io/en/stable/installing/) and running that python file (Windows/MacOS/Linux/BSD), or you can run the following command in terminal (Linux/BSD):

```bash
sudo apt install python3-pip
```

If you're using brew for MacOS, you can install pip (along with the rest of Python 3) using brew:

```bash
brew install python3
```

**Note: The creator of this software does not recommend the installation of python or pip using brew, and instead recommends that pip be installed using [get-pip.py](https://pip.pypa.io/en/stable/installing/), or that Python 3.5+ be installed using the installation candidates found on [python.org](https://www.python.org/downloads/), which include pip by default.**

### Using Pip to install from PyPi

Fetching this repository from PyPi is the recommended way to install this package. From your terminal, run the following command:

```bash
pip3 install tlnetcard-python
```

And that's it! Now you can go right ahead to the quick-start guide!

### Installing from Source

Installing this package from source is the only way to guarantee you're getting the latest, bleeding-edge code. If you're installing from source, I assume you already know the risks (stability is not guaranteed, stability is *not* guaranteed, etc.). Assuming you have git installed, installation from source can be accomplished easily (MacOS/Linux/BSD):

```bash
git clone https://github.com/EGuthrieWasTaken/tlnetcard_python.git
cd tlnetcard_python/
pip3 install .
```

If, for whatever reason, you have your heart set on not installing git on your system (who installs from source but won't use git?), you can also install by [downloading the zip file](https://github.com/EGuthrieWasTaken/tlnetcard_python/archive/master.zip) for this project, unzipping it, and starting a terminal/cmd session in the unzipped directory. Then, run the following command (Windows/MacOS/Linux/BSD):

```bash
pip3 install .
```

Of course, there is no need to use pip to install. In lieu of ```pip3 install .``` for either of the above methods, you could substitute ```python3 setup.py install```.  
And that's it! Now you can go right ahead to the quick-start guide!

## Quick-Start Guide

After installation, you can get started with using the module immediately! You will first need to create a login object to initiate an authenticated session with TLNET Supervisor, and then you may run any other commands you wish, but understand that every action object must be initialized with the login session. An example is below:

```python
import tlnetcard_python

# Creating authenticated session.
card = tlnetcard_python.Login("admin", "password", "10.0.0.100")

# Do whatever configuration is needed here.
batch_config = tlnetcard_python.system.administration.BatchConfiguration(card)
batch_config.upload_system_configuration("/home/sampleUser/sys_config.txt")

# Closing session.
card.logout()
```

Note that this process could be placed into a loop to configure multiple systems. Additionally, using the [set_host()](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python#set_hosthost-passwd) method allows for the same login object to be used with multiple hosts. The password will still need to be provided for each host change unless the ```save_passwd``` flag was set to ```True``` when the object was initialized. See example below:

```python
from tlnetcard_python import Login
from tlnetcard_python.system.administration import BatchConfiguration
hosts = ['10.0.0.100', '10.0.0.101', '10.0.0.103', ...]

card = Login("admin", "password", save_passwd=True)
for host in hosts:
    card.set_host(host)
    batch_config = BatchConfiguration(card)
    batch_config.upload_system_configuration("/home/sampleUser/sys_config.txt")
card.logout()
```

**Note: the creator(s) of this software will not be liable for any unintended results from using any tlnetcard_python software, including lost or stolen passwords. Please use options such as ```save_passwd``` with caution. For complete information regarding liability, see the [License](https://github.com/EGuthrieWasTaken/tlnetcard_python/blob/master/LICENSE).**  

## Documentation

Documentation for this project can be found in the GitHub Repository. Each folder has it's own documentation for the class files it contains. The documentation tree is below:  

* [tlnetcard_python](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python)
  * [Monitor](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/monitor)
    * [Information](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/monitor/information)
      * [UPS Properties](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/monitor/information/ups_properties)
      * [Battery Parameters](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/monitor/information/battery_parameters)
      * [In/Out Parameters](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/monitor/information/in_out_parameters)
      * [Identification](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/monitor/information/identification)
      * [Status Indication](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/monitor/information/status_indication)
      * [Shutdown Agent](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/monitor/information/shutdown_agent)
    * [History](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/monitor/history)
      * [Event Log](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/monitor/history/event_log)
      * [Data Log](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/monitor/history/data_log)
      * [Configure](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/monitor/history/configure)
    * [Environment](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/monitor/environment)
      * [Information](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/monitor/environment/information)
      * [Configuration](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/monitor/environment/configuration)
    * [About](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/monitor/about)
      * [Information](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/monitor/about/information)
  * [Device](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/device)
    * [Management](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/device/management)
      * [Reaction](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/device/management/reaction)
      * [Configure](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/device/management/configure)
      * [Control](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/device/management/control)
      * [Weekly Schedule](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/device/management/weekly_schedule)
      * [Specific Schedule](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/device/management/specific_schedule)
      * [Event Level](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/device/management/event_level)
  * [System](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/system)
    * [Administration](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/system/administration)
      * [User Manager](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/system/administration/user_manager)
      * [TCP/IP](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/system/administration/tcp_ip)
      * [Web](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/system/administration/web)
      * [Console](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/system/administration/console)
      * [FTP](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/system/administration/ftp)
      * [Time Server](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/system/administration/time_server)
      * [Syslog](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/system/administration/syslog)
      * [Batch Configuration](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/system/administration/batch_configuration)
      * [Upgrade](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/system/administration/upgrade)
    * [Notification](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/system/notification)
      * [SNMP Access](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/system/notification/snmp_access)
      * [SNMPv3 USM](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/system/notification/snmpv3_usm)
      * [SNMP Trap](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/system/notification/snmp_trap)
      * [Mail Server](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/system/notification/mail_server)
      * [Wake On LAN](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/system/notification/wake_on_lan)
      * [Modbus TCP](https://github.com/EGuthrieWasTaken/tlnetcard_python/tree/master/tlnetcard_python/system/notification/modbus_tcp)
