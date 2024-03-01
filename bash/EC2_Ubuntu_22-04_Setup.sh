#!/bin/bash
# EC2 Ubuntu 22.04 setup script

# Log all output to file
# https://serverfault.com/questions/103501/how-can-i-fully-log-all-bash-scripts-actions
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>~/EC2_Ubuntu_Setup.log 2>&1
# Everything below will go to the file 'EC2_Ubuntu_Setup.log':

# get default interface name
ifname=`ip route | awk '{ print $5 }' | head -1`

# Update default interface DNS server
# https://repost.aws/knowledge-center/ec2-static-dns-ubuntu-debian
# https://ioflood.com/blog/bash-multiline-string/
cat << EOF | sudo tee /etc/netplan/99-custom-dns.yaml
network:
  version: 2
  ethernets:
    $ifname:
      nameservers:
        addresses: [10.0.0.132]
      dhcp4-overrides:
        use-dns: false
        use-domains: false
EOF

# Generate new DNS config
sudo netplan generate

# Set time zone to Central time
sudo timedatectl set-timezone US/Central

# reboot server to apply network changes
# (could also do 'sudo netplan apply' instead but this ensures changes will persist)
# Userdata script only runs on initial launch by default:
# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html
reboot now

