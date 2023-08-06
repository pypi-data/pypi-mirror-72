$LogDir="c:\render\logs\"

function WriteLog
{
    Param ([string]$LogString)
    $DateTime = "[{0:MM/dd/yy} {0:HH:mm:ss}]" -f (Get-Date)
    $LogMessage = "$Datetime $LogString"
    Add-content "$LogDir\client-render.log" -value $LogMessage
	Write-Output $LogMessage
}

New-Item -ItemType directory -Path $LogDir -Force

WriteLog "Retriving user data..."
$URL="http://169.254.169.254/latest/user-data"
$WebClient = new-object system.net.webclient
$UserData = $WebClient.DownloadString($URL) | ConvertFrom-Json

WriteLog "Activating environment..."
Start-Process -FilePath "c:\venv\3dsmax\Scripts\activate.bat" -Wait -NoNewWindow

$WatchDelay = $UserData.watch_delay
WriteLog "Watching changes after each $WatchDelay seconds..."
Start-Process -FilePath "python" -ArgumentList "-m render.watch Corona --delay=$WatchDelay" -NoNewWindow -RedirectStandardOutput "${LogDir}\watch-out.log" -RedirectStandardError "${LogDir}\watch-err.log"

$HeartbeatInterval=$UserData.heartbeat_interval
$Hostname=$UserData.hostname
WriteLog "Starting worker $Hostname..."
Start-Process -FilePath "celery" -ArgumentList "-A render.celery worker -Q rendering --pool=solo --loglevel debug --hostname=$Hostname --without-gossip --without-mingle --heartbeat-interval=$HeartbeatInterval --logfile=$LogDir/celery.log" -Wait -NoNewWindow

