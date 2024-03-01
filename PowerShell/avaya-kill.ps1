get-process ccad | %{ $_.closemainwindow() }
$wshell = New-Object -ComObject wscript.shell
$wshell.AppActivate('Agent Desktop Shutdown')
Start-Sleep -s 1
$wshell.SendKeys('~')