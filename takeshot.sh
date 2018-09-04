#!/bin/sh
#./takeshot <outfile.jpeg>

case "$1" in
*\.jpeg)
	fswebcam -r 3624x2448 -p MJPEG --no-banner $1 -v -S 40 -F 3
	;;
*)
	echo "output filename Not a .jpeg suffix"
	;;
esac
