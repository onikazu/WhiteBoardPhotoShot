# WhiteboardPhotoShot
This python program was made in order to take a note of the meeting on a whiteboard with a voice order.

# Dependency
python3

# Setup
You have to download some softwares which are described below.
  paho.maqtt
  slacker
  configparser
  picamera
  
Also, the certificate obtained from beebotte (CACERT) is required.
https://beebotte.com/certs/mqtt.beebotte.com.pem

1. Link your Google account with Google home.
2. Make an beebotte account.
3. Make a channel. For example, 
  channel name = photoshot
  channel description = photoshot
  resource = action
  resource description = action
4. Take a note about your beebotte channel token.
5. Make an IFTTT account and link it with the Google account which links with Google home.
6. Make an applet which post a order to a raspberrypi via beebotte. 
  This
    1. Decide how to make an order, such as "take photo."
    2. Decide how the Google home reply. For instance, "take photo."
    3. Choose the language which you use.
  That
    1. Put a URL as below.
      https://api.beebotte.com/v1/data/publish/[channel name]/[resource]?token=[beebotte channel token]
    2. Choose method "POST."
    3. Choose Content Type "application/json."
    4. Write your key items in Body, such as "photo."
7. Make sure the key items is post from webhoock to beebotte.
  1. Go to account setting → access management in beebnotte and make note about your secret key.
  2. Go to console and put your secret key in the top blank, and put both the channel name and the resources in the section of subscribe.
  3. Push "subscribe", and then you will get "success" in the log.
  4. Say your voice order to Google home. If the key items is post successfully, you can see it in the message box.
8. Obtain your slack token from https://api.slack.com/custom-integrations/legacy-tokens.
9. Downloads photo.py and config.def.ini from code.
10. Make config.ini to enter your settings such as beebotte token, beebotte secret key, topic (channel name/resource), slack token, and slack channel name (use config.def.ini as a format). 
11. Rename config.def.ini to config.ini.
11. The program should be set up successfully. Say your order to Google home to try the program. If it works successfully, the slack channel will recieve the whiteboard photoshot which the raspberrypi camera took.

オートスタートについて

WhiteboardPhotoShotのオートスタートにはautostartファイルを利用している。
/home/pi/.config/lxsession/LXDE-pi/にあるautostartを以下のように編集する。

<img width="569" alt="2018-08-07 13 16 31" src="https://user-images.githubusercontent.com/40164219/43754223-a6e9a542-9a44-11e8-8277-1d1973c58135.png">

以上はphoto.py（ラズパイ専用モジュール）を動かす場合で、usbphoto.pyを動かす場合は@bash /home/~を

@python2 /home/pi/WhiteboardPhotoShot/usbphoto.py

に変える（その下の4行はラズパイのスリープ防止）。




# Usage
1. Make a voice order to Google home. For example, say "Okay, Google. Take Photo."
2. Your order is recieved by raspberrypi soon, and it takes a photo of whiteboard.  
3.The photo is sent to the slack channel which you specify and deleted from raspberrypi.

# Licence

# Authors

# Reference
https://qiita.com/msquare33/items/9f0312585bb4707c686b
https://fabcross.jp/category/make/sorepi/20170907_automatic_photography.html  
https://ai-coordinator.jp/surveillance-camera-slack  
https://tonari-it.com/python-splitext-listdir/

