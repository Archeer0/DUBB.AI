# Prueba de Chatterbox Multilingual: python tts_chatterbox.py ref1.wav salida1.wav "texto1" [ref2.wav salida2.wav "texto2" ...]
import sys, time, soundfile as sf
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

t = time.time()
tts = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
print(f"Carga del modelo: {time.time() - t:.0f} s")
args = sys.argv[1:]
for ref, out, text in zip(args[0::3], args[1::3], args[2::3]):
    t = time.time()
    wav = tts.generate(text, language_id="es", audio_prompt_path=ref)
    sf.write(out, wav.squeeze().numpy(), tts.sr)
    print(f"Generación: {time.time() - t:.0f} s -> {out}")
