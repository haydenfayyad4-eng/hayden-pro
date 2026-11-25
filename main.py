import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Hayden AI", page_icon="🤖")
st.title("🤖 Hayden AI PRO - Macam Aku!")
st.write("Dibuat khas untuk Muhammad Adam - Taip je apa-apa, aku layan!")

# API Key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

if "chat" not in st.session_state:
    st.session_state.chat = []

# Papar chat lama
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.write(msg["text"])

# Kotak taip - SATU JE, TAKDE TAB DAH
prompt = st.chat_input("Taip apa-apa... contoh: sang kancil, berita hari ni, apa tu fotosintesis")

if prompt:
    st.session_state.chat.append({"role": "user", "text": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Fikir jap..."):
            # Suruh AI auto tukar topik sendiri
            full_prompt = f"""Kau adalah Hayden, kawan borak Muhammad Adam.
            Kau cakap macam budak Melayu, santai, kelakar sikit.
            Kalau user tanya pasal tokoh, sejarah, haiwan, benda - bagi jawapan gaya Wikipedia Melayu yang senang faham.
            Kalau user tanya berita - bagi ringkasan berita.
            Kalau user tanya maksud perkataan - bagi maksud Kamus.
            Kalau user nak borak biasa - borak je macam kawan.
            Jangan suruh user pilih topik. Terus jawab.
            Soalan user: {prompt}"""
            
            res = model.generate_content(full_prompt)
            st.write(res.text)
            st.session_state.chat.append({"role": "assistant", "text": res.text})
