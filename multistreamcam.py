import picamera
from pynput.keyboard import Key, Listener
#from multiprocessing import Process
import subprocess
import sys, os
import io
import time
import datetime
#from moviepy.editor import VideoFileClip
def write_from_buf(splits):
    #print("writing from buf")
    stream.copy_to('%s/highlight%d.h264'%(directory,splits))
    
    """with io.open('highlight%d.h264'%(splits),'wb') as output:
        for frame in stream.frames:
            print("iteration")
            if frame.frame_type==picamera.PiVideoFrameType.sps_header:
                stream.seek(frame.position)
                break
            while True:
                buf=stream.read1()
                if not buf:
                    break
                output.write(buf)
    stream.seek(0)
    stream.truncate()
    """
def on_press(key):
        global splits
        global recording
        global recorded
        global game_files
	print('{0} pressed'.format(key))
	try: hit=key.char
	except: hit=key.name
	if (hit=='esc' ) or (key==Key.esc):
		camera.stop_recording()
		camera.stop_preview()
		for x in range(splits):
                    print(x)
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
		
	if  hit=='n':
	#	print("YAY!")
		splits+=1
		highlight(splits)
                #camera.split_recording('part%d.h264' %splits)
                #p=Process(target=highlight,args=(splits,))
                #p.start()
	if hit=='r':
            if(recording==False):
                game_files+=1
                camera.start_recording('%s/game%d.h264'%(directory, game_files),splitter_port=2,resize=(640,480))
                recording=True
                recorded=True
            else:
                camera.stop_recording(splitter_port=2)
                recording=False
	
                
def highlight(splits):
        global stream
	print("highlight recording")
	camera.split_recording('%s/useless.h264'%directory) #dumps the very few frames lost while the circular buffer is dumped into a file, shouldn't be longer than a few seconds of lost footage if anything.
	write_from_buf(splits)
	
	camera.split_recording(stream)
	print("resuming highlight recording")
	#home=os.path.expanduser("~")
        #ffmpeg='/usr/bin/ffmpeg'
        #argument=[ffmpeg,'-y','-sseof','-3','-t','3','-i', 'part%d.h264'%(splits-1),'highlight%d.h264'%(splits)]
	#highlightcreate=subprocess.Popen(argument)
	"""outcall=str("MP4Box -add part%d.h264 part%d.mp4" %(splits-1,splits-1))
	subprocess.call(outcall,shell=True) """
	#clip=VideoFileClip("part%d.mjpeg" %(splits-1))
	""".subclip(0,-30)"""
	#c=clip.duration
	#print(c)
	#clip.write_videofile("highlight%d.h264" %splits,fps=25)
        
	

with picamera.PiCamera() as camera:
    recording=False
    recorded=False
    game_files=0
    splits=0
    directory=os.path.join(datetime.datetime.now().strftime("%y-%m-%d-%H-%M"))
    print(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    camera.resolution=(1024,768)
    
    camera.framerate=30
    stream=picamera.PiCameraCircularIO(camera, seconds=30)
    camera.start_recording(stream,format='h264')
        
    camera.start_preview()
	
    with Listener(on_press=on_press) as listener:
        listener.join()
