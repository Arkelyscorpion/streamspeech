import os 
from pathlib import Path 
if __name__=="__main__":
    file_path = Path(__file__).parent 
    app_path = Path(f"{file_path}/app_main.py")
    os.system(f"streamlit run {app_path}")

     
