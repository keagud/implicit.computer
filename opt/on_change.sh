#!/bin/sh


LOG_TAG="on-change-script"


for exec_target in /opt/site/on_change/*;  do
	if [ ! -f "$exec_target" ] || [ ! -x "$exec_target" ]; then
		continue
	fi

	if ! "$exec_target"; then
		logger -t "$LOG_TAG" "FAILED: $exec_target"
	else
		logger -t "$LOG_TAG" "FINISHED: $exec_target"
	fi

done
