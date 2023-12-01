import google.generativeai as palm
import os 
from pathlib import Path 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import pyttsx3 
from shiny import ui, render, App, reactive 

# Design Spec 
# We need a text field to input user input 
# Need a button to allow text generation 
app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
        ui.input_text("user_prompt", "Ask me something"),
        ui.input_action_button("ok_go", "OK")
        ),
        ui.panel_main(
        ui.output_text("text_response")
    )


    ) 
    
)

def server(input, output,session):
    palm.configure(api_key = os.environ["google_key"])
    res = reactive.Value("Welcome to our chat bot, friend. Have fun")
    @reactive.Effect 
    @reactive.event(input.ok_go)
    def _():
        res.set(input.user_prompt())

    @output 
    @render.text
    def text_response():
        response = palm.generate_text(prompt = res())
        out = response.result.split("\n")
        return out 
app = App(app_ui, server)