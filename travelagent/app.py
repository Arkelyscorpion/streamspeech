import google.generativeai as palm
import os 
from shiny import ui, render, App, reactive 
from shinyswatch import theme_picker_ui, theme_picker_server 

# TODO: UI styling, better error handling to show some form of notification to the user 
app_ui = ui.page_fluid(
    theme_picker_ui(), 
    ui.layout_sidebar(
    ui.sidebar(

    ui.input_text_area("user_prompt", "", placeholder="Type here", autoresize = True),
    ui.input_action_button("ok_go", "Run"), 


    ), 

    ui.output_text_verbatim("text_response")

    )
            
    )


def server(input, output,session):
    theme_picker_server()
    try: 
        # TODO: Disable this welcome message from the API
        # TODO: Restrict the range of topics supported 
        palm.configure(api_key = os.environ["google_key"])
    except KeyError:
        raise KeyError("This app requires an API Key named 'google_key' in your environment. Get one at https://developers.generativeai.google/tutorials/setup")
    res = reactive.Value("Welcome to our chat bot, friend. Have fun")
    @reactive.Effect 
    @reactive.event(input.ok_go)
    def _():
        res.set(input.user_prompt())

    @output 
    @render.text
    async def text_response():
        with ui.Progress(min = 1, max = 20) as p:
            p.set(message="Thinking", detail="This may take a while, please wait")
            response = palm.generate_text(prompt = res())
            out = response.result
        return out 
app = App(app_ui, server)