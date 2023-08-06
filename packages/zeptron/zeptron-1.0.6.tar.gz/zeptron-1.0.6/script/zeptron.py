# USAGE
# python zeptron.py --i SERVER_IP --p PORT --r True

# import the necessary packages
from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time

def main():
	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--ip", required=True,
		help="ip address of the server to which the client will connect")
	ap.add_argument("-p", "--port", required=True,
		help="port of the server to which the client will connect")
	ap.add_argument("-r", "--raspberry", 
		help="if using Raspberry pi, put True, else do not use")
	args = vars(ap.parse_args())

	# initialize the ImageSender object with the socket address of the
	# server
	sender = imagezmq.ImageSender(connect_to="tcp://{}:{}".format(args["ip"], args["port"]))

	# get the host name, initialize the video stream, and allow the
	# camera sensor to warmup
	device_name = socket.gethostname()

	if (args["raspberry"]): 
		vs = VideoStream(usePiCamera=True).start()
	else:
		vs = VideoStream(src=0).start()

	time.sleep(2.0)
	
	while True:
		# read the frame from the camera and send it to the server
		frame = vs.read()
		sender.send_image(device_name, frame)