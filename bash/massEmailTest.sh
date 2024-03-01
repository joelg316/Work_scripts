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

function sendEmail {
    MyHost=`hostname`

    MailHost=127.0.0.1
    MailPort=25

    # These values are defined in function call at bottom of script
    FromAddr=$1
    
    ToAddr=$2

    Subject=$3

    Message=$4

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
}

# for each domain in input file, send a test email from test@{domain}.com
while read domain; do sendEmail test@$domain $1 'Test' 'Test message'; done < domains.txt

# call sendEmail and pass the arguments entered by the user, or use these default values
#sendEmail ${1:-'test@test.com'} ${2:-'joel@joeltest.org'} ${3:-'Test'} ${4:-'Test message'}
