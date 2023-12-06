import streamlit as st 
from speechbrain.pretrained import HIFIGAN, Tacotron2, FastSpeech2 
import google.generativeai as palm 
import os 
from time import sleep 
import numpy as np 
from joblib import Parallel, delayed 

def get_model():
    hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-ljspeech", savedir="tmpdir_vocoder")
    tacotron2 = Tacotron2.from_hparams(source="speechbrain/tts-tacotron2-ljspeech", savedir="tmpdir_tts")
    return hifi_gan, tacotron2

def configure_palm():
    try:
        palm.configure(api_key = os.environ["google_key"])
    except KeyError:
        raise KeyError("This app requires an API Key named 'google_key' in your environment. Get one at https://developers.generativeai.google/tutorials/setup")

def get_text():
    return st.text_area(label="User Text", value="Ask me something")

def prompt_palm(user_prompt):
    res = palm.generate_text(prompt= user_prompt).result
    return res 

def text_to_speech(palm_response):
    hifi_gan, tacotron2 = get_model()
    output_, _, _ = tacotron2.encode_text(palm_response)
    waveforms = hifi_gan.decode_batch(output_)
    return waveforms 

def get_audio_waveform(res):
    audios = []
    for response in res:
        if response == "" or not response:
            continue
        hifi_gan, tacotron2 = get_model()
        mel_output, mel_length, alignment = tacotron2.encode_text(response)
        waveforms = hifi_gan.decode_batch(mel_output)
        audios.append(waveforms.squeeze(1))
    return audios

def get_waveform(res):
    hifi_gan, tacotron2 = get_model()
    mel_output, mel_length, alignment = tacotron2.encode_text(res)
    return hifi_gan.decode_batch(mel_output).squeeze(1)

def merge_audio(audio_list):
    return np.column_stack(audio_list) 

def process_audio(res):
    audios = Parallel(n_jobs = 4, backend="threading")(delayed(get_waveform)(x) for x in res if x)
    return merge_audio(audios)




def os_tts(palm_response):
    return os.system(f"say {palm_response}")

def play_audio(tts_response,  **kwargs):
    audio_ = tts_response  
    return st.audio(audio_, **kwargs)


def main():
    st.set_page_config(page_title="streamspeech", page_icon=f":brain:")
    configure_palm()
    with st.spinner("Processing your input, please wait...."):
        audio_res = process_audio(prompt_palm(get_text()).split("\n"))
    sample_rate = st.slider("Sample Rate", min_value = 16000, max_value = 40000, value = 22050, step = 20)
    return play_audio(audio_res, sample_rate = sample_rate)

if __name__=="__main__":
    main() 




