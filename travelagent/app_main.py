import streamlit as st 
from speechbrain.pretrained import HIFIGAN, Tacotron2, FastSpeech2 
import google.generativeai as palm 
import os 
from time import sleep 

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

def text_to_speech(palm_response):
    hifi_gan, tacotron2 = get_model()
    output_, _, _ = tacotron2.encode_text(palm_response)
    # Running Vocoder (spectrogram-to-waveform)
    waveforms = hifi_gan.decode_batch(output_)
    return waveforms 

def os_tts(palm_response):
    return os.system(f"say {palm_response}")

def play_audio(tts_response, gan = False, **kwargs):
    audio_ = tts_response.numpy()[0] if gan else tts_response 
    return st.audio(audio_, **kwargs)


def main():
    configure_palm()
    audio_res = text_to_speech(prompt_palm(get_text()))
    sample_rate = st.slider("Sample Rate", min_value = 16000, max_value = 40000, value = 22050, step = 20)
    return play_audio(audio_res, sample_rate = sample_rate, gan=True)

if __name__=="__main__":
    main() 




