import whisper
import os
import language_tool_python
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Verberg Tkinter-venster
Tk().withdraw()

# Stap 1: Bestand selecteren via popup
audio_path = askopenfilename(title="Selecteer een audiobestand", filetypes=[("Audio bestanden", "*.wav *.mp3 *.m4a")])
if not audio_path:
    print("Geen bestand geselecteerd. Script gestopt.")
    exit()

# Stap 2: Laad het Whisper-model
model = whisper.load_model("base")

# Stap 3: Transcribeer met segmenten
print(f"Transcriberen van: {audio_path}")
result = model.transcribe(audio_path)

# Stap 4: Genereer segmenten met tijdcodes en afwisselende sprekerlabels
segments = result["segments"]
originele_segmenten = []
for i, segment in enumerate(segments):
    start = segment["start"]
    end = segment["end"]
    text = segment["text"]
    spreker = f"Spreker {i % 2 + 1}"
    originele_segmenten.append(f"[{start:.2f} – {end:.2f}] {spreker}: {text.strip()}")

originele_tekst = "\n\n".join(originele_segmenten)

# Stap 5: Bestandsnamen en output-paden instellen
base_name = os.path.splitext(os.path.basename(audio_path))[0]
base_dir = os.path.dirname(audio_path)

output_origineel = os.path.join(base_dir, f"{base_name}_origineel.txt")
output_verbeterd = os.path.join(base_dir, f"{base_name}_verbeterd.txt")

# Stap 6: Sla originele versie op
with open(output_origineel, "w", encoding="utf-8") as f:
    f.write(originele_tekst)
print(f"Originele transcriptie met tijdcodes opgeslagen als: {output_origineel}")

# Stap 7: Grammaticale/spellingcorrectie uitvoeren
tool = language_tool_python.LanguageTool('nl')
print("Voer grammaticale/spellingscontrole uit...")
verbeterde_tekst = tool.correct(originele_tekst)

# Stap 8: Sla verbeterde versie op
with open(output_verbeterd, "w", encoding="utf-8") as f:
    f.write(verbeterde_tekst)
print(f"Verbeterde transcriptie opgeslagen als: {output_verbeterd}")
