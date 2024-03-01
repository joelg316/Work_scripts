#!/bin/bash

insert_settings() {
  echo -e "# Audit log\n\$ModLoad imfile\n\$InputFileName /var/log/audit/audit.log\n\$InputFileTag tag_audit_log:\n\$InputFileStateFile audit_log\n\$InputFileSeverity info\n\$InputFileFacility local6\n\$InputRunFileMonitor\n\nlocal6.* @@[$1] ### Add rsyslog server IP here." >> /etc/rsyslog.conf
  service rsyslog restart
  echo "Success"
}

if ! grep -q "# Audit" /etc/rsyslog.conf; then
  cp -a /etc/rsyslog.conf /etc/rsyslog.conf.bak
  echo "" >> /etc/rsyslog.conf # Append blank line but only if inserting settings for first time
  insert_settings $1
  echo "Changes made:"
  diff /etc/rsyslog.{conf.bak,conf}
else 
  while true; do
    read -p "Audit log settings already present, overwrite? " yn
    case $yn in
        [Yy]* )  sed -i.bak2 '/# Audit/,$d' /etc/rsyslog.conf # delete previous settings
	  insert_settings $1
	  echo "Changes made:"
	  diff /etc/rsyslog.{conf.bak2,conf}    
	  break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
  done
fi
