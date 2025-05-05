# Content Delivery Server
A Python web server that delivers content within a directory.

# Supported devices
This webserver *technically* supports any OS as long as it can run Python and Gunicorn; however, the shell scripts are
designed with Linux users in mind. I'm a Linux user myself and I don't have the time or resources to design the shell
scripts for operating systems outside of GNU/Linux.

# How to use
*Written with Linux in mind*

***Note:** the [main.py](ContentDeliveryServer/main.py) file contains code to run the development Flask server. **DO NOT
USE RUN IT DIRECTLY.** Flask is **NOT** intended for production. Use Gunicorn instead. In order to discourage Flask 
usage, there will not be any way to configure the Flask webserver without hard-coding.*

## Dependencies
The dependencies can be found in the requirements.txt file.

## Installation
1. Clone this repository with `git clone https://gitlab.lettsn.org/Lett/contentdeliveryserver#`
2. CD into the root directory
3. Run `chmod +x run_server.sh`
4. Run `./run_server.sh [port]`, where `[port]` is the port you want to use.
5. A Gunicorn webserver using all threads of your CPU should start.

## Automatic startup
Keep in mind that the webserver won't automatically start on system boot. You will need to set up a systemd service.
Example of a systemd service:
```ini
[Unit]
Description=Content Delivery Server
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=on-failure
RestartSec=1
User=lett
ExecStart=/home/lett/PycharmProjects/ContentDeliveryServer/run_server.sh 7010

[Install]
WantedBy=multi-user.target
```

## Automatic updates
When you run the webserver via the `run_server.sh` script, an auto-updater will start that will pull from the repository
every hour. Keep in mind that it won't actually download anything unless there are any changes to download.


# Configuration
## Overview
The WSGI itself can be configured via a `.ini` file. If you setup the `CDS_CONFIG_ROOT`, then it will use the 
configuration in that given folder. However, if you leave it blank, then it will default to the `cds_config` folder in
the root directory of the cloned repository.

Below is the template that all configuration files follow:
```
[category]
name = value
```

## Configurations
### access
| Name                | Description                                      | Type   | Default |
|---------------------|--------------------------------------------------|--------|---------|
| allow_folder_access | Whether folders can be transversed.              | bool   | false   |
| hidden_files        | Whether files can be hidden with `.[file_name]`. | bool   | true    |

<details><summary>Example of access category</summary>

```ini
[access]
allow_folder_access = true
hidden_files = true
```

</details>
