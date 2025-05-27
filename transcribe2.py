import streamlit as st
import whisper
import tempfile
import os
import language_tool_python

st.set_page_config(page_title="Audio Transcriptie & Correctie", layout="wide")
st.title("🎙️ Transcriptie & Tekstcorrectie App")

# Upload audio
uploaded_file = st.file_uploader("📂 Upload een audiobestand (.wav, .mp3, .m4a)", type=["wav", "mp3", "m4a"])

if uploaded_file is not None:
    # Sla bestand tijdelijk op
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as temp_audio:
        temp_audio.write(uploaded_file.read())
        audio_path = temp_audio.name

    st.info("⏳ Transcriptie bezig...")
    
    # Whisper model laden en transcriberen
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)

    # Segmenten met tijdcodes en sprekerlabels
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

    # Verbeteren via LanguageTool
    st.info("🧠 Voer grammaticale controle uit...")
    tool = language_tool_python.LanguageTool('nl')
    verbeterde_tekst = tool.correct(originele_tekst)

    st.subheader("✅ Verbeterde transcriptie")
    st.text_area("Verbeterd", verbeterde_tekst, height=300)

    # Downloadknoppen
    st.download_button("💾 Download originele transcriptie", originele_tekst, file_name="transcriptie_origineel.txt")
    st.download_button("💾 Download verbeterde versie", verbeterde_tekst, file_name="transcriptie_verbeterd.txt")

    # Opruimen
    os.remove(audio_path)
