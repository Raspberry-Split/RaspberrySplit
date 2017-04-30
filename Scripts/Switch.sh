aplay /home/pi/RaspberrySplit/Sound/Switch.wav &
sleep 0.5
export SWITCH_ED=1
sudo python /home/pi/RaspberrySplit/Main.py $SWITCH_FB $SWITCH_VOL &
if [ "$SWITCH_FB" = "0" ]; then
  ( sleep 1 ; cat /home/pi/RaspberrySplit/Overlay/SwitchFromTV.raw >/dev/fb1 ) &
fi
if [ "$SWITCH_FB" = "1" ]; then
  vcgencmd display_power 0 &
fi
