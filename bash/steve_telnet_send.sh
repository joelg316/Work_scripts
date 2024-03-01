#!/bin/bash
{ 
    sleep 5; 
    echo 'ehlo';
    sleep 3;
    echo 'MAIL FROM:<joe@nocom.com>';
    sleep 3; 
    echo 'RCPT TO: <stevene@texquad.com>';
    sleep 3;
    echo 'DATA';
    sleep 3;
    echo -e 'To:stevene@texquad.com\nMIME-Version: 1.0 (mime-construct 1.9)\nContent-Type: application/exe\nContent-Transfer-Encoding: base64\n\n';
    echo 'Test email to show off to Joel';
    echo '.';
} | telnet $mta 25