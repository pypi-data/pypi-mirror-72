@ECHO OFF
:: This batch file is started rendering.
TITLE Rendering window
celery -A render.celery worker -Q rendering --pool=solo --loglevel info --hostname=render-node@%%h --without-gossip --without-mingle --heartbeat-interval=30