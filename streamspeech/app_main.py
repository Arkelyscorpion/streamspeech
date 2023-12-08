import os
import google.generativeai as palm
import numpy as np
import streamlit as st
from joblib import Parallel, delayed
from speechbrain.pretrained import HIFIGAN, FastSpeech2, Tacotron2


class StreamSpeech:
    def __init__(self):
        try:
            self.api_key = os.environ["google_key"]
            palm.configure(api_key = self.api_key)
        except KeyError:
            raise KeyError("This app requires an API Key named 'google_key' in your environment. Get one at https://developers.generativeai.google/tutorials/setup")

    def _get_model(self):
        hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-ljspeech", savedir="tmpdir_vocoder")
        tacotron2 = Tacotron2.from_hparams(source="speechbrain/tts-tacotron2-ljspeech", savedir="tmpdir_tts")
        return hifi_gan, tacotron2
    
    def _get_text(self):
        return st.text_area(label="StreamSpeech", value="Ask me something")
    
    def _get_waveform(self,res):
        hifi_gan, tacotron2 = self._get_model()
        mel_output, mel_length, alignment = tacotron2.encode_text(res)
        return hifi_gan.decode_batch(mel_output).squeeze(1)

    def _merge_audio(self,audio_list):
        return np.column_stack(audio_list) 
    
    def _prompt_palm(self, user_text):
        res = palm.generate_text(prompt= user_text).result
        return res.split("\n")


    def _process_audio(self,res):
        audios = Parallel(n_jobs = 4, backend="threading")(delayed(self._get_waveform)(x) for x in res if x)
        return self._merge_audio(audios)
    
    def _get_response(self):
        return self._process_audio(self._prompt_palm(self.get_text()))
    
    def _play_audio(self, tts_response,  **kwargs):
        audio_ = tts_response  
        return st.audio(audio_, **kwargs)

    
    def run_app(self):
        st.set_page_config(page_title="streamspeech", page_icon=f":brain:")
        with st.spinner("Processing your input, please wait...."):
            audio_res = self._process_audio(self._prompt_palm(self._get_text()))
        sample_rate = st.slider("Sample Rate", min_value = 16000, max_value = 40000, value = 22050, step = 20)
        return self._play_audio(audio_res, sample_rate = sample_rate)

def main():
    return StreamSpeech().run_app()


if __name__ == "__main__":
    main()

    











