#!/usr/bin/python

from json import loads
from urllib2 import Request, urlopen
from wave import open as open_audio
from pyaudio import PyAudio, paInt16
from pygsr import Pygsr
import audioop
import urllib2


class Speech2MQTT(Pygsr):

  def __init__(self):
    Pygsr.__init__(self)
    self.active = False
    self.count_silence = 0
    return 
    
    
  def listen(self, level = 1000,timeout = 1,language = "sv_SE", device_i=None):
    while(True):
      print self.listen_once(level,timeout,language, device_i)
    
    print "Next loop!"
  
    return 
    
  def listen(self, level = 1000,timeout = 1,language = "sv_SE",loop=1, device_i=None):
    audio = PyAudio()
    #print audio.get_device_info_by_index(1)
    stream = audio.open(input_device_index=device_i,output_device_index=device_i,format=self.format, channels=self.channel,
                            rate=self.rate, input=True,
                            frames_per_buffer=self.chunk)

   
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
      if self.count_silence > (self.rate / self.chunk * timeout):
        self.active = False
	print "Processing..."
        break;
    
      olddata = data      
 
    stream.stop_stream()
    #print "END"
    stream.close()
    audio.terminate()
         
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
#    except IndexError:
#	try:
# 	  phrase, complete_response = self.speech_to_text(language)
#	except:
#	  phrase = ""

    #print phrase

#    stream.stop_stream()
    #print "END"
#    stream.close()
#    audio.terminate()

    return phrase



if __name__ == '__main__':
  listner = Speech2MQTT()
  print listner.listen()
  
  

