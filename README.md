# RaspberrySplit
Software for Raspberry Split screen. Controller and guide coming soon.

# Get it running (TEMPORARY)
Step 1: Flash 2016-11-08-pitft-35r.img to the SD card

Step 2: Boot the Pi.

Step 3: Plug in any keyboard.

Step 4: Click on the Raspberry at the top left, then Accessories, then Terminal. Move the window so you can see the window buttons, then maximize it to see the entire terminal.

Step 5: Connect to the Net using the Pi 3's WiFi system or through any other preferred method.

Step 6: Type "sudo raspi-config", then go to Internationalization, then Change Keyboard Layout, then choose your country's keyboard layout. Then select Finish.

Step 7: Type "cd ~ && git clone https://github.com/Raspberry-Split/RaspberrySplit.git && cd RaspberrySplit && sudo chmod -R +x ."

Step 8: Type "sudo apt-get update && sudo apt-get install python-dev && sudo apt-get install bluetooth libbluetooth-dev && sudo pip install pybluez && sudo pip install python-uinput"

Step 9: Go through the prompts, installing all of the libraries.

Step 10: "sudo nano /etc/modules", add uinput to end, CTRL+O, ENTER, CTRL+X

Step 11: "sudo nano /etc/systemd/system/dbus-org.bluez.service", add a space and then "-C" after bluetoothd, save and exit nano as usual. "sudo reboot".

Step 12: Reopen Terminal as usual.

Step 13: Type "sudo raspi-config", then go to Boot Options, then Console. Then select Finish. Then press escape, as you would not like to shut down.

Step 14: "cd RaspberrySplit", then "sudo cp cmdline.txt /boot/cmdline.txt && sudo cp config.txt /boot/config.txt && sudo cp rc.local /etc/rc.local"

Step 15: "sudo reboot". Unplug the keyboard and Internet cable if needed.
