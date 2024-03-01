
$Folders = @()
$Folders += (Get-ChildItem -Path "C:\Users\joelg\Documents\Cases\*\*\*" -Directory | Select-Object FullName)

# I tried including tar files with the below line but it seems to break the command:
# $Folders += (Get-ChildItem -Path "C:\Users\joelg\Documents\Cases\*\*\*" -Directory -Include *.tar | Select-Object FullName)

#-Force -ErrorAction SilentlyContinue
Write-Host $Folders


foreach ($path in $Folders){
    $path = [string]$path.FullName
    echo $path
    #Can also use Write-Output
    #Remove-Item -Path $path -Recurse -Force 
	# -Confirm:$false
    # https://stackoverflow.com/questions/38141528/cannot-remove-item-the-directory-is-not-empty
    Get-ChildItem $path -Recurse | Remove-Item -Force
}


<#for ($i =0; $i -lt $Folders.Count; $i++) {
    $path = $Folders[$i]
    echo $path
    Remove-Item -Path "$path" -Confirm
}#>

<#
# From https://stackoverflow.com/questions/40000691/loop-over-array

$dates = @("23-06-2016","24-06-2016","27-06-2016")

for ($i = 0; $i -lt $dates.Count ; $i++) {
    $find = $dates[$i]
    $rep = $dates[$i+1]
    echo $find
    echo $rep
}
#>
