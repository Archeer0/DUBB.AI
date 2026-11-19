# Prueba de IndexTTS 2.5: python tts_indextts.py referencia.wav salida.wav "Texto en castellano" [ref_emocion.wav]
import sys, time, os, functools, torchaudio
# El backend sox de torchaudio se rompe con la libsox de Arch: guardar con soundfile
torchaudio.save = functools.partial(torchaudio.save, backend="soundfile")
from indextts.infer_v2_5 import IndexTTS2

ref, out, text = sys.argv[1], sys.argv[2], sys.argv[3]
emo = sys.argv[4] if len(sys.argv) > 4 else None
m = os.path.join(os.environ["DUBB_ROOT"], "modelos/indextts-2.5")
t = time.time()
tts = IndexTTS2(cfg_path=f"{m}/config.yaml", model_dir=m)  # elige solo: gráfica del Mac (MPS) si la hay, si no CPU
print(f"Carga del modelo: {time.time() - t:.0f} s")
t = time.time()
tts.infer(spk_audio_prompt=ref, text=text, output_path=out, lang="es", emo_audio_prompt=emo)
print(f"Generación: {time.time() - t:.0f} s -> {out}")
