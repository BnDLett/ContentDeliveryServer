# Content Delivery Server
A Python web server that delivers content within a directory.

# Supported devices
This webserver *technically* supports any OS as long as it can run Python and Gunicorn; however, the shell scripts are
designed with Linux users in mind. I'm a Linux user myself and I don't have the time or resources to design this for a
Windows system. *However, contributions that allows for Windows compatibility is allowed and encouraged.*

# How to use
*Written with Linux in mind*
## Installation
1. Clone this repository with `git clone https://gitlab.lettsn.org/Lett/contentdeliveryserver#`
2. CD into the root directory
3. Run `chmod +x run_server.sh`
4. Run `./run_server.sh`
5. A Gunicorn webserver using all threads of your CPU should start.

## Automatic startup
Keep in mind that the webserver won't automatically start on system boot. You will need to set up a systemd script.
Additionally, the `run_server.sh` script isn't designed with flexibility in mind. You *could* run it anywhere, but don't
expect customizability. 

## Automatic updates
When you run the webserver via the `run_server.sh` script, an auto-updater will start that will pull from the repository
every 12 hours. Keep in mind that it won't actually download anything unless there are any changes to download.
