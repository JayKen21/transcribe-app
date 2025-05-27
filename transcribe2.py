import streamlit as st
import whisper
import tempfile
import os
import requests

st.set_page_config(page_title="Transcriptie & Tekstcorrectie App", layout="wide")
st.title("🎙️ Transcriptie & Tekstcorrectie App")

# Functie voor grammaticale correctie via LanguageTool API
def check_with_languagetool_api(text):
    response = requests.post(
        "https://api.languagetoolplus.com/v2/check",
        data={
            "text": text,
            "language": "nl",
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    result = response.json()
    corrected_text = text
    for match in reversed(result["matches"]):
        offset = match["offset"]
        length = match["length"]
        replacement = match["replacements"][0]["value"] if match["replacements"] else ""
        corrected_text = corrected_text[:offset] + replacement + corrected_text[offset+length:]
    return corrected_text

# Upload audio
uploaded_file = st.file_uploader("📂 Upload een audiobestand (.wav, .mp3, .m4a)", type=["wav", "mp3", "m4a"])

if uploaded_file is not None:
    # Tijdelijk opslaan
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as temp_audio:
        temp_audio.write(uploaded_file.read())
        audio_path = temp_audio.name

    st.info("⏳ Transcriptie bezig...")

    # Whisper transcribe
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)

    # Segmenten met tijdcodes en 'Spreker'-labels
    segments = result["segments"]
    originele_segmenten = []
    for i, segment in enumerate(segments):
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]
        spreker = f"Spreker {i % 2 + 1}"
        originele_segmenten.append(f"[{start:.2f} – {end:.2f}] {spreker}: {text.strip()}")

    originele_tekst = "\n\n".join(originele_segmenten)

    st.subheader("📄 Ruwe transcriptie met tijdcodes")
    st.text_area("Origineel (ruw)", originele_tekst, height=300)

    # Verbeteren via LanguageTool API
    st.info("🧠 Voer grammaticale/spellingscontrole uit...")
    verbeterde_tekst = check_with_languagetool_api(originele_tekst)

    st.subheader("✅ Verbeterde transcriptie")
    st.text_area("Verbeterd", verbeterde_tekst, height=300)

    # Downloadknoppen
    st.download_button("💾 Download originele transcriptie", originele_tekst, file_name="transcriptie_origineel.txt")
    st.download_button("💾 Download verbeterde versie", verbeterde_tekst, file_name="transcriptie_verbeterd.txt")

    # Opruimen tijdelijk audiobestand
    os.remove(audio_path)
