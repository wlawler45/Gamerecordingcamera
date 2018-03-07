import picamera
from pynput.keyboard import Key, Listener
import subprocess
import sys, os
import io
import time
import datetime


#Function that copies stream to file
def write_from_buf(splits):
    #print("writing from buf")
    stream.copy_to('%s/highlight%d.h264'%(directory,splits))
    
#Function to catch key presses and perform functions
def on_press(key):
	#state and counter variables given initial values in main and then altered in this function
        global splits
	global game_files
        global recording
	global recorded
        
	print('{0} pressed'.format(key))
	try: hit=key.char
	except: hit=key.name
	#if ESC key is hit, stop recordings and for each highlight file in recordings convert file to MP4 file and then convert game file to MP4 if it exists then return 
	if (hit=='esc' ) or (key==Key.esc):
		camera.stop_recording()
		camera.stop_preview()
		for x in range(splits):
                    
                    mp4command=['MP4Box','-add','%s/highlight%d.h264'%(directory,x+1), '%s/highlight%d.mp4'%(directory,x+1)]
                    subprocess.call(mp4command)
                    time.sleep(5)
		if(recorded):
                    if(recording): camera.stop_recording(splitter_port=2)
                    for x in range(game_files):
                    
                        mp4command=['MP4Box','-add','%s/game%d.h264'%(directory,x+1), '%s/game%d.mp4'%(directory,x+1)]
                        subprocess.call(mp4command)
                        time.sleep(5)
                return False
	
	#if n key is hit create a new highlight of number splits
	if  hit=='n':
	#	print("YAY!")
		splits+=1
		highlight(splits)
                
	#if r key is hit starts new full game recording at lower resolution if not already recording, cancels full game recording if recording
	if hit=='r':
            if(recording==False):
                game_files+=1
                camera.start_recording('%s/game%d.h264'%(directory, game_files),splitter_port=2,resize=(640,480))
                recording=True
                recorded=True
            else:
                camera.stop_recording(splitter_port=2)
                recording=False
	
#Highlight function, dumps 30 second memory of high quality footage in circular buffer to a file then resumes circular buffer capture                
def highlight(splits):
	print("highlight recording")
	camera.split_recording('%s/useless.h264'%directory) #dumps the very few frames lost while the circular buffer is dumped into a file, shouldn't be longer than a few seconds of lost footage if anything.
	write_from_buf(splits)
	
	camera.split_recording(stream)
	print("resuming highlight recording")
	
        
	
#Start of "Main" function

with picamera.PiCamera() as camera:
	#global variable definitions
    recording=False
    recorded=False
    game_files=0
    splits=0
	global stream
	#directory to save files according to date and time the program is run
    directory=os.path.join(datetime.datetime.now().strftime("%y-%m-%d-%H-%M"))
    print(directory)
	
	#create directory
    if not os.path.exists(directory):
        os.makedirs(directory)
	
    #Set camera parameters and open camera stream and simultaneous circular stream
    camera.resolution=(1024,768)
    camera.framerate=30
    stream=picamera.PiCameraCircularIO(camera, seconds=30)
    camera.start_recording(stream,format='h264')
    camera.start_preview()
	#creates listener event to detect key presses and take commands
    with Listener(on_press=on_press) as listener:
        listener.join()
