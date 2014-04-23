#!/usr/bin/python


from pygsr import Pygsr
import audioop

class Speech2MQTT(Pygsr):

  def __init__(self):
    Pygsr.__init__(self)
    self.active = False
    return 
    
    
  def listen(self, level, device_i=None):
        audio = PyAudio()
        print audio.get_device_info_by_index(1)
        stream = audio.open(input_device_index=device_i,output_device_index=device_i,format=self.format, channels=self.channel,
                            rate=self.rate, input=True,
                            frames_per_buffer=self.chunk)
        print "REC: "
        frames = []
        while(True):  #for i in range(0, self.rate / self.chunk * time):
            data = stream.read(self.chunk)
            rms = audioop.rms(data, 2)
            
            #There is some noise start recording
            if rms > level and self.active == False:
                self.active = True
                
            if       
            frames.append(data)
        stream.stop_stream()
        print "END"
        stream.close()
        audio.terminate()
        write_frames = open_audio(self.file, 'wb')
        write_frames.setnchannels(self.channel)
        write_frames.setsampwidth(audio.get_sample_size(self.format))
        write_frames.setframerate(self.rate)
        write_frames.writeframes(''.join(frames))
        write_frames.close()
        self.convert()
