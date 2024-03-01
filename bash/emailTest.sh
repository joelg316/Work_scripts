#!/bin/bash

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

MailHost=joeltest.relay.tmes.trendmicro.com
MailPort=25

FromAddr=test@joeltest.org

ToAddr=joel@joeltest.org
#ToAddr=joel@joeltest.org

headers="Received: from adc-mailrelay1.trendmicro.com (unknown [84.71.84.71])
	by inpre01.tmes.trendmicro.com (Trend Micro Email Security) with ESMTPS id 9FF71100008D3
	for <joel@joeltest.org>; Mon,  5 Feb 2024 07:31:37 +0000 (UTC)
Received: from adc-mailrelay1.trendmicro.com (unknown [127.0.0.1])
	by DDEI (Postfix) with ESMTP id 7B40116A211D;
	Mon,  5 Feb 2024 07:31:34 +0000 (UTC)
Received: from adc-orig.trendmicro.com (unknown [83.70.83.70])
	by adc-mailrelay1.trendmicro.com (Trend Micro Email Security) with ESMTPS id 9FF71100008D2
	for <joel@joeltest.org>; Mon,  5 Feb 2024 07:31:33 +0000 (UTC)"

subject="Test"

message="Test email with suspicious IP in received header"
#message="Test email with URLs: http://wrs71.winshipway.com https://google.com"

#exec 3<>'telnet ${MailHost} ${MailPort}'
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

echo "${headers}" >&3
echo "Subject: ${subject}" >&3
echo "${message}" >&3
echo "." >&3

read -u 3 sts line
checkStatus "$sts" "$line"
