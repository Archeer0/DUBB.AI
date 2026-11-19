# IndexTTS 2.5 mezclando la voz del actor con una referencia castellana en distintas proporciones:
# python tts_mezcla.py referencia.wav ref_castellana.wav carpeta_salida "frase" 0.3 0.5 0.7
import sys, time, os, functools, torchaudio
# El backend sox de torchaudio se rompe con la libsox de Arch: guardar con soundfile
torchaudio.save = functools.partial(torchaudio.save, backend="soundfile")
from indextts.infer_v2_5 import IndexTTS2

ref, emo, outdir, text, alphas = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:]
os.makedirs(outdir, exist_ok=True)
m = os.path.join(os.environ["DUBB_ROOT"], "modelos/indextts-2.5")
tts = IndexTTS2(cfg_path=f"{m}/config.yaml", model_dir=m)  # elige solo: gráfica del Mac (MPS) si la hay, si no CPU
for i, a in enumerate(alphas, 1):
    t = time.time()
    out = f"{outdir}/mezcla_{a}_toma{i}.wav"
    tts.infer(spk_audio_prompt=ref, text=text, output_path=out, lang="es", emo_audio_prompt=emo, emo_alpha=float(a))
    print(f"{time.time() - t:.0f} s -> {out}", flush=True)
