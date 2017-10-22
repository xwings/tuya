#!/bin/bash

LOCATION=$1
DATE=$2
TIME=$3

SMBDIR=""
CHATID=""
BOTAPI=""


echo "Start: $LOCATION/$DATE/$TIME.jpg" >> /data/scripts/telegram.log
cd $SMBDIR

WAIT=0
while [ ! -f $LOCATION/$DATE/$TIME.jpg ] ;
do
	sleep 10
	WAIT=$(( $WAIT + 1 ))

	if [ "$WAIT" -gt 10 ]; then
		echo "TIMEOUT: $LOCATION/$DATE/$TIME.jpg" >> /data/scripts/telegram.log
		exit 0;
	fi
done


if [ -f $LOCATION/$DATE/$TIME.jpg ]; then
	curl -s -X POST "https://api.telegram.org/$BOTAPI/sendPhoto" \
	-F caption="$DATE $TIME $(vcgencmd measure_temp)" -F disable_notification="1" -F chat_id=$CHATID -F photo="@$LOCATION/$DATE/$TIME.jpg"

	if [ $? == 0 ]; then
		echo "Uploaded: $LOCATION/$DATE/$TIME.jpg" >> /data/scripts/telegram.log
  	else
    		echo "Error: $LOCATION/$DATE/$TIME.jpg" >> /data/scripts/telegram.log
  	fi
fi
