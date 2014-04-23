#!/usr/bin/python

from json import loads
from urllib2 import Request, urlopen
from wave import open as open_audio
from pyaudio import PyAudio, paInt16
from pygsr import Pygsr
import audioop
import urllib2
import sys

class Speech2MQTT(Pygsr):

  def __init__(self):
    Pygsr.__init__(self)
    self.active = False
    self.count_silence = 0
    return 
    
   
    
  def listen(self, level = 1000,timeout = 1,ignore_shoter_than = 0.5,ignore_longer_than = 5 ,language = "sv_SE", device_i=None):
    audio = PyAudio()
    #print audio.get_device_info_by_index(1)
    stream = audio.open(input_device_index=device_i,output_device_index=device_i,format=self.format, channels=self.channel,
                            rate=self.rate, input=True,
                            frames_per_buffer=self.chunk)

    timeout_chuncks = self.rate / self.chunk * timeout
    minmessage = self.rate / self.chunk * ignore_shoter_than
    maxmessage = self.rate / self.chunk * ignore_longer_than

    try:
	    while(True):
	   
		    print "Start listening... "
		    frames = []
		    data = ""
		    olddata = ""
		    self.count_silence = 0
		    self.active = False
		
		    while(True):  #for i in range(0, self.rate / self.chunk * time):
		      data = stream.read(self.chunk)
		      rms = audioop.rms(data, 2)
		
		      #print str(rms) + '\r'
		            
		      #There is some noise start recording
		      if rms > level:
			self.count_silence = 0
		        
			if self.active == False:
			  print "Recording..."
		          self.active = True
		          self.count_silence = 0
			  frames.append(olddata)
		
		      if self.active:       
		        frames.append(data)
		              
		      if rms < level and self.active:
		        self.count_silence += 1
		              
		      #If we have enough silence send for processing  
		      if (self.count_silence > timeout_chuncks) and self.active == True:
		        self.active = False
			#print len(frames) #10 12
			#print self.count_silence #8
			if not len(frames)> self.count_silence + minmessage:
			  print "Disregarding noise"
			  frames = []
			  continue
			if len(frames)> self.count_silence + maxmessage:
			  print "Ignoring to long recording"
			  frames = []
                          continue

			print "Processing..."
		        break
		    
		      olddata = data      
		 
		         
		    write_frames = open_audio(self.file, 'wb')
		    write_frames.setnchannels(self.channel)
		    write_frames.setsampwidth(audio.get_sample_size(self.format))
		    write_frames.setframerate(self.rate)
		    write_frames.writeframes(''.join(frames))
		    write_frames.close()
		    self.convert()
		
		    try:      
		    	phrase, complete_response = self.speech_to_text(language) # select the language
		    except:
			phrase = ""
			
		    print phrase

    except KeyboardInterrupt:
        # quit
        stream.stop_stream()
	    #print "END"
        stream.close()
        audio.terminate()
	sys.exit()
	
    return 



if __name__ == '__main__':
  listner = Speech2MQTT()
  print listner.listen()
  
  

