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

$Hostname=$UserData.hostname
$HeartbeatInterval=$UserData.heartbeat_interval

WriteLog "Activating environment..."
Start-Process -FilePath "c:\venv\3dsmax\Scripts\activate.bat" -Wait -NoNewWindow

$ScreenshotDelay = $UserData.screenshots_delay
WriteLog "Making screenshots every $ScreenshotDelay seconds..."
Start-Process -FilePath "python" -ArgumentList "-m render.screen $ScreenshotDelay" -NoNewWindow -RedirectStandardOutput "${LogDir}\screens-out.log" -RedirectStandardError "${LogDir}\screens-err.log"

$SyncDelay = $UserData.sync_delay
WriteLog "Sync files every $SyncDelay seconds..."
Start-Process -FilePath "python" -ArgumentList "-m render.sync Corona" -NoNewWindow -RedirectStandardOutput "${LogDir}\sync-out.log" -RedirectStandardError "${LogDir}\sync-err.log"

WriteLog "Starting worker $Hostname..."
Start-Process -FilePath "celery" -ArgumentList "-A render.celery worker -Q rendering --pool=solo --loglevel debug --hostname=$Hostname --without-gossip --without-mingle --heartbeat-interval=$HeartbeatInterval --logfile=$LogDir/celery.log" -Wait -NoNewWindow

