# Prueba de Qwen3-TTS: python tts_qwen.py ref1.wav salida1.wav "texto1" [ref2.wav salida2.wav "texto2" ...]
# La transcripción de cada referencia se lee de ref.txt (mismo nombre, extensión .txt)
import sys, time, torch, soundfile as sf
from qwen_tts import Qwen3TTSModel

t = time.time()
tts = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-Base", device_map="cpu", dtype=torch.float32)
print(f"Carga del modelo: {time.time() - t:.0f} s")
args = sys.argv[1:]
for ref, out, text in zip(args[0::3], args[1::3], args[2::3]):
    t = time.time()
    wavs, sr = tts.generate_voice_clone(text=text, language="Spanish", ref_audio=ref,
                                        ref_text=open(ref.rsplit(".", 1)[0] + ".txt").read())
    sf.write(out, wavs[0], sr)
    print(f"Generación: {time.time() - t:.0f} s -> {out}")
