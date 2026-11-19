# Varias tomas por frase con IndexTTS 2.5: python tts_tomas.py referencia.wav N carpeta_salida "frase1" ["frase2" ...]
import sys, time, os, functools, torchaudio
# El backend sox de torchaudio se rompe con la libsox de Arch: guardar con soundfile
torchaudio.save = functools.partial(torchaudio.save, backend="soundfile")
from indextts.infer_v2_5 import IndexTTS2

ref, n, outdir, texts = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4:]
os.makedirs(outdir, exist_ok=True)
m = os.path.join(os.environ["DUBB_ROOT"], "modelos/indextts-2.5")
tts = IndexTTS2(cfg_path=f"{m}/config.yaml", model_dir=m)  # elige solo: gráfica del Mac (MPS) si la hay, si no CPU
for f, text in enumerate(texts, 1):
    for i in range(1, n + 1):
        t = time.time()
        out = f"{outdir}/frase{f}_toma{i}.wav"
        tts.infer(spk_audio_prompt=ref, text=text, output_path=out, lang="es")
        print(f"{time.time() - t:.0f} s -> {out}", flush=True)
