$LOG_DIR="c:\render\logs\"
$CurrentLog=$LOG_DIR + "client-render.log"

function WriteLog
{
    Param ([string]$LogString)
    $DateTime = "[{0:MM/dd/yy} {0:HH:mm:ss}]" -f (Get-Date)
    $LogMessage = "$Datetime $LogString"
    Add-content $CurrentLog -value $LogMessage
	Write-Output $LogMessage
}

New-Item -ItemType directory -Path $LOG_DIR -Force

WriteLog "Retriving user data..."
$URL="http://169.254.169.254/latest/user-data"
$WebClient = new-object system.net.webclient
$UserData = $WebClient.DownloadString($URL) | ConvertFrom-Json

$Hostname=$UserData.hostname
$HeartbeatInterval=$UserData.heartbeat_interval

WriteLog "Activating environment..."
Start-Process -FilePath "c:\venv\3dsmax\Scripts\activate.bat" -Wait -NoNewWindow

WriteLog "Making screenshots every 5 minutes..."
Start-Process -FilePath "python" -ArgumentList "-m render.screen 60" -NoNewWindow -RedirectStandardOutput "${LOG_DIR}\screens-out.log" -RedirectStandardError "${LOG_DIR}\screens-err.log"

#echo %DATE% %TIME% Sync files every 1 minutes...
#::start /B python -m render.sync 1

WriteLog "Starting worker $Hostname..."
Start-Process -FilePath "celery" -ArgumentList "-A render.celery worker -Q rendering --pool=solo --loglevel debug --hostname=$Hostname --without-gossip --without-mingle --heartbeat-interval=$HeartbeatInterval --logfile=$LOG_DIR/celery.log" -Wait -NoNewWindow

