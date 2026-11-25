from google import genai
import streamlit as st

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
from pengetahuan import SUMBER_BELAJAR
# lepas tu bagi Hayden baca sumber tu sebelum jawab
