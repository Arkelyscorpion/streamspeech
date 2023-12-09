import streamlit as st 
from speechbrain.pretrained import HIFIGAN, Tacotron2 
import google.generativeai as palm 
import os 
import numpy as np 
from joblib import Parallel, delayed 

class StreamSpeech:
    def __init__(self):
        self.hifi_gan, self.tacotron2 = self.get_model()

    def get_model(self):
        hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-ljspeech", savedir="tmpdir_vocoder")
        tacotron2 = Tacotron2.from_hparams(source="speechbrain/tts-tacotron2-ljspeech", savedir="tmpdir_tts")
        return hifi_gan, tacotron2
    
    def configure_palm(self):
        try:
            palm.configure(api_key = os.environ["google_key"])
        except KeyError:
            raise KeyError("This app requires an API Key named 'google_key' in your environment. Get one at https://developers.generativeai.google/tutorials/setup")
        
    def get_text(self):
        return st.text_area(label="User Text", value="Ask me something")
    
    def prompt_palm(self,user_prompt):
        response = palm.generate_text(prompt= user_prompt).result
        return response
    
    def text_to_speech(self,palm_response):
        output_, _, _ = self.tacotron2.encode_text(palm_response)
        waveforms = self.hifi_gan.decode_batch(output_)
        return waveforms 
    
    def get_audio_waveform(self,res):
        audios = []
        for response in res:
            if response == "" or not response:
                continue
            mel_output, mel_length, alignment = self.tacotron2.encode_text(response)
            waveforms = self.hifi_gan.decode_batch(mel_output)
            audios.append(waveforms.squeeze(1))
        return audios
    
    def get_waveform(self,res):
        mel_output, mel_length, alignment = self.tacotron2.encode_text(res)
        return self.hifi_gan.decode_batch(mel_output).squeeze(1)
    
    def merge_audio(self,audio_list):
        return np.column_stack(audio_list)
    
    def process_audio(self,res):
        audios = Parallel(n_jobs = 4, backend="threading")(delayed(self.get_waveform)(x) for x in res if x)
        return self.merge_audio(audios)
    
    def os_tts(self,palm_response):
        return os.system(f"say {palm_response}")
    
    def play_audio(self,tts_response,**kwargs):
        audio_ = tts_response  
        return st.audio(audio_, **kwargs)


Processor = StreamSpeech()

st.set_page_config(page_title="streamspeech", page_icon=f":brain:")
Processor.configure_palm()
with st.spinner("Processing your input, please wait...."):
    audio_res = Processor.process_audio(Processor.prompt_palm(Processor.get_text()).split("\n"))
sample_rate = st.slider("Sample Rate", min_value = 16000, max_value = 40000, value = 22050, step = 20)

Processor.play_audio(audio_res, sample_rate = sample_rate)






