#!/bin/sh

function checkStatus {
  expect=250
  if [ $# -eq 3 ] ; then
    expect="${3}"
  fi
  if [ $1 -ne $expect ] ; then
    echo "Error: ${2}"
    exit
  fi
}

MyHost=`hostname`

MailHost=127.0.0.1
MailPort=25

FromAddr=test@test.com

ToAddr=joelg@joelg.com

Subject=Test

Message="Test email with URLs: http://wrs71.winshipway.com https://google.com"

exec 3<>/dev/tcp/${MailHost}/${MailPort}

read -u 3 sts line
checkStatus "${sts}" "${line}" 220

echo "HELO ${MyHost}" >&3

read -u 3 sts line
checkStatus "$sts" "$line"

echo "MAIL FROM: ${FromAddr}" >&3

read -u 3 sts line
checkStatus "$sts" "$line"

echo "RCPT TO: ${ToAddr}" >&3

read -u 3 sts line
checkStatus "$sts" "$line"

echo "DATA" >&3

read -u 3 sts line
checkStatus "$sts" "$line" 354

echo "Subject: ${Subject}" >&3
echo "${Message}" >&3
echo "." >&3

read -u 3 sts line
checkStatus "$sts" "$line"
