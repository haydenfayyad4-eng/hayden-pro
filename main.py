import streamlit as st
import requests
import xml.etree.ElementTree as ET

# --- PASTE API KEY KAU KAT SINI ---
API_KEY = "AQ.Ab8RN6LFbebqAX9yDY8xutaGjZfbVAXUJqbmVq2Q_4BCRCdswg"

st.set_page_config(page_title="Hayden AI PRO", page_icon="🤖", layout="wide")
st.title("🤖 Hayden AI PRO - Macam Aku!")
st.caption("Dibuat khas untuk Muhammad Adam - Borak, Belajar, Wikipedia, Berita, Kamus, Novel & Islam")

# --- PERSONALITI PRO ---
SYSTEM_PRO = """
Kau adalah Hayden AI PRO, AI paling power dan paling best di dunia.
Kau kawan baik Muhammad Adam, umur 12 tahun, duduk Seremban.
Gaya cakap kau: Bahasa Melayu rojak santai, kelakar, positif, macam abang yang pandai.
Peraturan kau:
1. Jawab pendek tapi padat, jangan bebel panjang-panjang. Kalau Adam suruh terangkan panjang, baru bagi panjang.
2. Kalau Adam tanya coding, bagi code yang betul, terangkan step by step, bagi latihan kecil.
3. Kalau Adam tanya English, betulkan grammar dia, ajar perkataan baru, bagi contoh ayat.
4. Kalau Adam tanya Islam, jawab ikut Mazhab Syafie Malaysia, sopan, bagi dalil ringkas, dan suruh rujuk Mufti kalau ragu.
5. Kalau Adam sedih / penat, pujuk dia, bagi semangat.
6. Jangan pernah cakap kau tak tahu je. Cuba jawab sebaik mungkin.
7. Guna emoji sikit-sikit je, jangan banyak sangat.
8. Ingat apa yang Adam cakap sebelum ni dalam borak ni.
"""

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["💬 Hayden PRO", "📚 Wikipedia", "📰 Berita", "📖 Kamus", "📕 Novel", "🕌 Islam"])

# ============ TAB 1 - HAYDEN PRO ============
with tab1:
    col1, col2 = st.columns([1, 3])
    with col1:
        mode = st.selectbox("Hayden nak jadi apa hari ni?", ["🤖 Hayden PRO - Borak Macam Aku", "🇬🇧 Cikgu English PRO", "💻 Cikgu Coding PRO", "🕌 Ustaz PRO", "📚 Cikgu Sekolah PRO"])
        if st.button("🗑️ Padam Semua Borak"):
            st.session_state.messages = []
            st.rerun()
        st.info("Tip: Taip 'ajar aku coding' atau 'ajar aku English' untuk belajar!")
    
    with col2:
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Hai Adam! Aku Hayden PRO! Dah upgrade dah, lagi pandai macam Meta AI. Nak borak apa hari ni? Nak belajar coding ke English?"}]

        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.write(m["content"])

        soalan = st.chat_input("Tanya Hayden PRO apa-apa...")

        if soalan:
            st.session_state.messages.append({"role": "user", "content": soalan})
            with st.chat_message("user"):
                st.write(soalan)

            # Tukar mode ikut pilihan
            if "English" in mode:
                extra = "Fokus jadi Cikgu English PRO. Betulkan grammar, ajar vocab baru, bagi quiz kecil."
            elif "Coding" in mode:
                extra = "Fokus jadi Cikgu Coding PRO. Ajar Python step by step, bagi code betul, bagi latihan."
            elif "Ustaz" in mode:
                extra = "Fokus jadi Ustaz PRO. Jawab ikut Mazhab Syafie Malaysia, sopan, bagi dalil ringkas."
            elif "Sekolah" in mode:
                extra = "Fokus jadi Cikgu Sekolah PRO. Ajar Matematik, Sains, Sejarah cara senang faham."
            else:
                extra = "Fokus jadi kawan baik yang pandai macam Meta AI, kelakar dan membantu."

            try:
                teks = ""
                for m in st.session_state.messages[-10:]:
                    teks += f"{m['role']}: {m['content']}\n"
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
                data = {"contents": [{"parts": [{"text": f"{SYSTEM_PRO}\n{extra}\nPerbualan lepas:\n{teks}\nJawab soalan terakhir dengan gaya Hayden PRO."}]}],
                        "generationConfig": {"temperature": 0.8, "maxOutputTokens": 1500}}
                res = requests.post(url, json=data, timeout=30)
                jawapan = res.json()["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e:
                jawapan = f"Alaa error: {e}. Check API Key kat atas tu betul ke tak."

            st.session_state.messages.append({"role": "assistant", "content": jawapan})
            with st.chat_message("assistant"):
                st.write(jawapan)

# ============ TAB 2 - WIKIPEDIA ============
with tab2:
    st.header("📚 Wikipedia Melayu")
    cari = st.text_input("Taip apa nak cari, contoh: Hang Tuah", key="wiki")
    if st.button("Cari Wikipedia"):
        try:
            r = requests.get(f"https://ms.wikipedia.org/api/rest_v1/page/summary/{cari}", timeout=10).json()
            st.subheader(r.get("title", cari))
            st.write(r.get("extract", "Tak jumpa la. Cuba eja lain."))
            if r.get("thumbnail"):
                st.image(r["thumbnail"]["source"])
        except:
            st.write("Tak jumpa. Cuba taip lain.")

# ============ TAB 3 - BERITA ============
with tab3:
    st.header("📰 Berita Melayu Terkini")
    sumber = st.selectbox("Pilih Berita", ["Berita Harian", "Harian Metro", "Sinar Harian"])
    link_rss = {"Berita Harian": "https://www.bharian.com.my/rss", "Harian Metro": "https://www.hmetro.com.my/rss", "Sinar Harian": "https://www.sinarharian.com.my/rss"}
    if st.button("Load Berita"):
        try:
            r = requests.get(link_rss[sumber], timeout=10)
            root = ET.fromstring(r.content)
            c = 0
            for item in root.findall(".//item"):
                if c >= 10: break
                st.subheader(item.findtext("title"))
                st.write((item.findtext("description", "") or "")[:300])
                st.write(f"[Baca penuh]({item.findtext('link')})")
                st.divider()
                c += 1
        except Exception as e:
            st.write(f"Berita tak dapat load: {e}")

# ============ TAB 4 - KAMUS ============
with tab4:
    st.header("📖 Kamus Melayu / English")
    cari_k = st.text_input("Taip perkataan, contoh: hello / cantik", key="kamus")
    if st.button("Cari Maksud"):
        try:
            r = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{cari_k}", timeout=10)
            if r.status_code == 200:
                d = r.json()[0]
                st.subheader(d["word"])
                for m in d["meanings"][:3]:
                    st.write(f"**{m['partOfSpeech']}**: {m['definitions'][0]['definition']}")
                    if "example" in m["definitions"][0]:
                        st.write(f"Contoh: {m['definitions'][0]['example']}")
            else:
                r2 = requests.get(f"https://ms.wikipedia.org/api/rest_v1/page/summary/{cari_k}", timeout=10).json()
                st.subheader(r2.get("title", cari_k))
                st.write(r2.get("extract", "Tak jumpa maksud dia."))
                st.write("Cuba juga: [Kamus Dewan](https://prpm.dbp.gov.my/)")
        except:
            st.write("Tak jumpa la perkataan tu.")

# ============ TAB 5 - NOVEL ============
with tab5:
    st.header("📕 Novel & Cerita")
    cari_n = st.text_input("Taip tajuk novel / penulis, contoh: Harry Potter", key="novel")
    if st.button("Cari Novel"):
        try:
            r = requests.get(f"https://gutendex.com/books/?search={cari_n}", timeout=10).json()
            if r.get("results"):
                for b in r["results"][:5]:
                    st.write(f"**{b['title']}** - {', '.join([a['name'] for a in b['authors']])}")
                    if b.get("formats", {}).get("text/html"):
                        st.write(f"[Baca Online]({b['formats']['text/html']})")
            else:
                st.write("Takde kat Gutenberg.")
        except:
            st.write("Gutenberg tak dapat load.")
        try:
            r2 = requests.get(f"https://ms.wikipedia.org/api/rest_v1/page/summary/{cari_n}", timeout=10).json()
            if r2.get("extract"):
                st.subheader(f"Ringkasan: {r2.get('title')}")
                st.write(r2.get("extract"))
        except:
            pass

# ============ TAB 6 - ISLAM ============
with tab6:
    st.header("🕌 Syarak, Mufti & Hukum Islam")
    jenis = st.selectbox("Nak tanya apa?", ["Syarak", "Fatwa Mufti", "Hukum Islam", "Solat / Puasa / Zakat", "Akidah / Akhlak"])
    soalan_islam = st.text_input("Taip soalan, contoh: Apa hukum puasa ganti?", key="islam")
    if st.button("Tanya Hukum"):
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
            arahan = f"Kau Ustaz PRO, jawab soalan {jenis} untuk Adam guna Bahasa Melayu mudah, sopan, ikut Mazhab Syafie Malaysia. Bagi dalil ringkas, bagi langkah, dan suruh rujuk Mufti kalau ragu. Soalan: {soalan_islam}"
            data = {"contents": [{"parts": [{"text": arahan}]}]}
            res = requests.post(url, json=data, timeout=30)
            st.write(res.json()["candidates"][0]["content"]["parts"][0]["text"])
        except Exception as e:
            st.write(f"Error: {e}")
    st.divider()
    st.write("- [Mufti Wilayah Persekutuan](https://www.muftiwp.gov.my/)")
    st.write("- [e-Mufti Fatwa](https://www.e-mufti.gov.my/)")
    st.write("- [JAKIM](https://www.islam.gov.my/)")
