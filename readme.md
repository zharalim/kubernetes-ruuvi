# RuuviTag on Kubernetes

A system for gathering measurements from RuuviTag (https://ruuvi.com/) via bluetooth, saving them to InfluxDB and showing them on Grafana. All running on one node Kubernetes cluster on Raspberry Pi 3 B+.

This is not a production ready system: RBAC is not used, grafana and influxdb passwords are not managed, all Ansible automation is not idempotent etc..

The Ansible automation:
1. Setups ssh keys and disables password access
1. Installs Kubernetes with kubeadm
1. Builds the `ruuvi` docker image and starts up the services.

Why was this done:
- To learn more about kubernetes. GKE was too easy ;)
- To use RuuviTag for something fun

## Steps for running the system

Prepare your controller machine (tested on [WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10)):
1. Install Ansible (2.7)
1. Run `ansible-galaxy install -r requirements.yml`
1. When running on windows WSL run `export ANSIBLE_CONFIG=./ansible.cfg` to use the config file regardless of the file permissions.

Set up the raspberry pi:
1. Download raspbian lite image and flash the sd card
1. Create empty file `ssh` to the boot partition of the SD card to enable ssh
1. Boot up the rasberry pi
1. Create Ansible inventory for your environment.
    - See `inventories/inventory-template` dir for example
    - Create ssh key and configure the needed variables to the group vars
    - Save the inventory to `inventories/inventory` folder or change `ansible.cfg` to match your dir
1. Run ansible `ansible-playbook install.yml -k`. *For the first run* you'll need to use `-k` and give the raspbian's default password `raspberry` when asked.
1. Connect to grafana http://host_ip:30000/

## TODO list

- ruuvi container hangs sometimes
- Add another node to the cluster
- Use StatefulSet for influxDB
- Try local persistent volume for influxDB
- Use USB storage for persistent volume support
- Use helm
    - InfluxDB and Grafana charts. InfluxDB didn't work straight out of the box because of missing arm images.
    - Create chart for the ruuvi deployment