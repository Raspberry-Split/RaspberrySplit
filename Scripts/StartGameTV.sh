echo "fb0"
clear
sudo /home/pi/RaspberrySplit/Apps/gpsp/gpsp "$SWITCH_GAME" &
sleep 0.5
now=$(pgrep gpsp)
sudo kill -STOP $now
sleep 0.01
sudo kill -CONT $now