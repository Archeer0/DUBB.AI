# Análisis técnico y plan de desarrollo — AI Movie Dubbing Studio

## Contexto
`product.md` pide un análisis técnico antes de escribir código: qué tecnologías existen, qué se puede reutilizar, licencias, calidad, hardware y limitaciones reales, más un plan por fases verificables. Este documento es ese análisis.

Al aprobarlo:
- Lo guardo en el proyecto como `docs/analisis-tecnico.md`.
- Empiezo por la **Fase 0** (pruebas cortas para decidir motores), descrita al final.

Las licencias "no comerciales" (NC) **no son un problema**, porque el uso es personal y privado. Aun así, las indico.

---

## 1. Conclusión rápida

| Etapa | Recomendación inicial | Alternativa a probar |
|---|---|---|
| Separar voces / música / efectos | **BS/Mel-RoFormer** (vía `audio-separator`) para aislar la voz | **Bandit v2** (separa diálogo, música y efectos por separado) |
| Transcripción con tiempos | **WhisperX** (faster-whisper large-v3 + alineación por palabra) | — |
| Quién habla cada vez | **pyannote Community-1** | NVIDIA Sortformer (limitado a 4 personas, descartado como principal) |
| Traducción | **LLM local con llama.cpp**: Qwen3-30B-A3B o similar | Qwen3-14B, Mistral Small |
| Voz en castellano clonada | **A decidir en la Fase 0** entre IndexTTS 2.5, Chatterbox Multilingual y Qwen3-TTS | + conversión de voz (Seed-VC / OpenVoice) |
| Ajuste de tiempos | Duración controlada **en el propio modelo de voz** y, como apoyo, estiramiento suave con Rubber Band | — |
| Mezcla y exportación | **FFmpeg** | — |
| Interfaz (Fase 7) | **PySide6** (ventanas nativas en Linux y macOS) | — |

**El mayor riesgo del proyecto es la voz.** Conseguir castellano de España con la voz de un actor que habla inglés no está resuelto "de serie" por ningún modelo. Por eso propongo probarlo antes de construir nada más (Fase 0).

---

## 2. Análisis por etapa

### A. Separación de audio
- **Demucs (Meta):** referencia clásica, licencia MIT, pero **ya no se mantiene** y está pensado para música (voz / batería / bajo / resto), no para cine.
- **RoFormer (BS / Mel-Band):** son los mejores modelos actuales para **aislar la voz**. Se usan con la librería `audio-separator` (MIT). Separa en dos partes: voz y "todo lo demás". Para doblar nos basta, porque lo que queremos es quitar la voz y conservar el resto entero.
- **Bandit v2:** diseñado **específicamente para cine**: separa diálogo, música y efectos. Código Apache-2.0, pesos CC BY-SA. Inconvenientes: entrenado con datos limpios y modernos, y hay quejas de que algunos programas no cargan bien sus pesos.
- **MVSEP-CDX23:** modelo de concurso de 2023 para cine (MIT). Más antiguo.
- **Particularidad del cine clásico:** audio mono, ruido y siseo. Ningún modelo está entrenado con este tipo de audio. Hay que **probarlo con un fragmento real**. Por suerte, separar voz de fondo suele resistir bien el ruido.

**Decisión:** RoFormer como opción principal para quitar la voz. Bandit v2 como alternativa, a comparar en la Fase 2.

### B. Transcripción
- **WhisperX:** transcribe con Whisper large-v3 (muy robusto con audio viejo), alinea cada palabra con precisión y se integra con pyannote. Licencia BSD. Es la opción estándar, sin rival claro para inglés.
- **Subtítulos en inglés, si los hay:** sirven para corregir palabras dudosas. Son un extra opcional.

### C. Quién habla en cada momento (diarización)
- **pyannote Community-1:** abierto (MIT + CC-BY-4.0) y sin límite de personajes. Además da una "huella vocal" de cada personaje, útil para mantener `VOICE_001` constante en toda la película. La descarga requiere una cuenta gratuita en Hugging Face (la web donde se publican los modelos).
- **Sortformer (NVIDIA):** limitado a 4 personas. No sirve para películas.
- **Limitación real:** con voces que se pisan, ruido o muchos personajes secundarios, **habrá errores**. Por eso es clave la corrección manual que pide el proyecto.

### D. Traducción
- No hace falta un modelo especializado: inglés → español es de los pares mejor cubiertos. Un modelo de lenguaje general con buenas instrucciones lo hace bien y, sobre todo, **entiende el contexto**, que es lo que pide el proyecto.
- **llama.cpp:** el programa que ejecuta estos modelos en local. Es muy eficiente en CPU y además **puede usar tu gráfica AMD mediante Vulkan** (otra vía de acceso a la gráfica que sí funciona con la tuya), sin depender de ROCm.
- **Modelo candidato: Qwen3-30B-A3B** (Apache-2.0). Es grande, pero en cada palabra solo trabaja una parte pequeña, así que en CPU va rápido. Ocupa unos 18 GB, y tienes 30 GB de RAM.
- **Cómo se traduce:**
  - Por escenas, pasando el contexto anterior y una ficha de cada personaje (registro, forma de hablar).
  - Se pide **castellano peninsular** y una duración aproximada en sílabas.
  - Si una frase no cabe en el tiempo, se pide una versión alternativa más corta o más larga, como indica `product.md`.

### E. Voz clonada en castellano (la etapa crítica)

**El problema:** al clonar en español una voz que solo tenemos hablando inglés, los modelos tienden a:
1. Arrastrar **acento inglés**.
2. Hablar con **acento latinoamericano**. Está documentado en Qwen3-TTS, y la mayoría de los datos de entrenamiento en español son latinos.

Candidatos:

| Modelo | Español | Puntos fuertes | Licencia |
|---|---|---|---|
| **IndexTTS 2.5** (Bilibili) | Sí (añadido en 2.5) | **Separa voz y emoción** (referencia de identidad + referencia emocional, justo lo que pide el proyecto) y **controla la duración exacta** | Propia, a revisar |
| **Chatterbox Multilingual** (Resemble AI) | Sí, 23 idiomas | MIT, control de intensidad emocional, buena calidad | MIT |
| **Qwen3-TTS** (Alibaba) | Sí | Clona con 3 s de audio, buena calidad | Apache-2.0 |
| OmniVoice (k2-fsa) | Sí (600+ idiomas) | Fija la duración en segundos | Pesos NC |
| XTTS-v2 | Sí | Maduro, pero de 2023 y por debajo de los anteriores | CPML (NC) |
| F5-TTS | Solo con versiones comunitarias | Buena clonación | NC |

**Plan B, si el acento falla:** generar en dos pasos.
1. Se genera la frase con una voz castellana neutra y buena entonación.
2. Un **conversor de voz** (Seed-VC, GPL-3; u OpenVoice, MIT) cambia el timbre por el del actor.

Así el acento sale castellano y el timbre, del actor. Es más lento y puede perder algo de naturalidad.

**Muestras de referencia:** el audio de cine clásico es ruidoso. Para cada personaje se elegirán automáticamente los fragmentos más limpios de voz aislada, con posibilidad de elegirlos a mano.

### F. Sincronización
- **Primera opción:** que el modelo de voz genere ya la duración correcta. IndexTTS 2.5 y OmniVoice lo permiten.
- **Segunda:** pedir otra traducción más corta o más larga.
- **Última:** estirar o comprimir ligeramente con **Rubber Band**, que cambia la velocidad sin cambiar el tono. Límite aproximado de ±10–15 % para que no suene artificial.

### G. Mezcla y exportación
- **FFmpeg** hace todo:
  - Mezcla el fondo original con los diálogos nuevos.
  - Ajusta el volumen según el estándar de cine (nivel de sonoridad normalizado).
  - Evita la saturación.
  - Mete la nueva pista en MKV/MP4 sin tocar el vídeo (`-c:v copy`).
- **Opcional:** bajar ligeramente el fondo mientras habla alguien, para tapar restos de la voz inglesa que la separación no haya quitado.

### H. Interfaz (Fase 7)
- **PySide6:** ventanas nativas en Linux y macOS, licencia LGPL. Permite una lista de frases, reproducir cada una y editarla.
- Hasta la Fase 7 se trabaja desde la terminal.
- Playwright no aplica, salvo que la interfaz acabe siendo web.

---

## 3. Proyectos existentes: ¿reutilizar o no?

| Proyecto | Qué hace | Veredicto |
|---|---|---|
| pyVideoTrans (GPL-3, ~18K estrellas) | Doblaje completo con F5-TTS / CosyVoice | Buena **referencia de ideas**. Demasiado grande y genérico para nuestro caso |
| SoniTranslate, Python-Autodub, KrillinAI, OmniVoice Studio | Flujos de doblaje parecidos | Referencia. Ninguno se centra en calidad, cine clásico o castellano |
| TTS-Audio-Suite (ComfyUI) | Reúne muchos modelos de voz | Útil para **probar modelos** en la Fase 0 |

**Decisión:** no partir de un proyecto existente, sino **reutilizar sus librerías** (WhisperX, pyannote, audio-separator, llama.cpp, el modelo de voz elegido) dentro de nuestra arquitectura de etapas independientes. Es más simple (Ponytail) y nos da control sobre la calidad.

---

## 4. Hardware: qué esperar en tu equipo

- **Gráfica (Vega integrada):**
  - **Vulkan** (con llama.cpp para traducir): debería funcionar sin trucos.
  - **PyTorch** (que usan separación, transcripción y voz): solo con el truco de hacer pasar la gráfica por otro modelo, y sin garantías. Lo comprobaremos en la Fase 0.
- **Tiempo estimado** para 90 minutos de película, solo CPU. Son estimaciones gruesas:
  - Separación: 1–2 h.
  - Transcripción + diarización: 1–2 h.
  - Traducción: 1–2 h.
  - **Generación de voz: la parte más lenta**, de varias horas a más de un día según el modelo. El resultado se guarda frase a frase y se reanuda donde se quedó.
- **En total:** entre una y tres noches. Es aceptable según `product.md`.
- **Disco:** cada película ocupará unos 5–15 GB de archivos intermedios, más los modelos (unos 30–40 GB en total).
- **macOS:** todos los candidatos funcionan en Mac con chip Apple. Algunos, como Qwen3-TTS, tienen versión optimizada (MLX).

---

## 5. Limitaciones reales (para que no haya sorpresas)

1. **El acento castellano** con voz clonada es el punto más débil del estado del arte. Puede requerir el plan B.
2. **El audio antiguo y ruidoso** empeora la separación, la identificación de personajes y la calidad de la voz clonada.
3. **Voces solapadas**, gritos y susurros: la identificación de quién habla fallará a veces. Habrá que corregir a mano.
4. **Restos de la voz inglesa:** la separación nunca es perfecta. Puede oírse un leve rastro de la voz original en el fondo.
5. **Emociones extremas** (llanto, risa, gritos): los modelos las reproducen peor que el habla normal.
6. **Velocidad:** con solo CPU, el proceso será lento. Lo compensan la reanudación y la caché.

---

## 6. Plan de desarrollo

**Fase 0 — Pruebas de decisión (NUEVA, antes de la Fase 1).** Sin construir la app, solo pruebas sueltas:
1. Crear el entorno aislado con `uv` (gestor de Python que instala un Python 3.12 propio sin tocar el del sistema). Comprobar si la gráfica acelera con PyTorch (truco ROCm) y con Vulkan.
2. Coger **un fragmento de 1–2 minutos de una película clásica tuya** con dos o más personajes. Separar la voz y clonar 3–4 frases en castellano con IndexTTS 2.5, Chatterbox Multilingual y Qwen3-TTS, más el plan B si hace falta.
3. Te paso los audios, **eliges de oído** y fijamos el motor de voz.

Te pediré aprobación antes de cada descarga pesada (los modelos ocupan varios GB).

**Fases 1–8:** tal como están en `product.md`. Cada etapa es un script independiente que lee y escribe en la carpeta del proyecto de cada película:
```
proyecto_pelicula/
  01_analisis.json      02_fondo.wav  02_voces.wav
  03_transcripcion.json 03_personajes.json
  04_traduccion.json    05_frases/VOICE_001_0001.wav …
  06_dialogos.wav       06_mezcla.wav
  salida/ (mkv, mp4, wav, srt)
```
Si el archivo de una etapa ya existe y está completo, esa etapa se salta. Así funcionan la caché y la reanudación.

## Verificación
- **Fase 0:** termina cuando eliges un motor de voz escuchando las muestras y sabemos si tu gráfica sirve.
- **Cada fase siguiente:** se prueba con el mismo fragmento de película. Al final, con una secuencia larga y los 7 criterios de `product.md`.

## Lo que necesito de ti para la Fase 0
- Un fragmento de película clásica: ruta a un archivo MKV/MP4 con varios personajes.
- Visto bueno para descargar los modelos de prueba (unos 15–20 GB en total).

## Fuentes
- [IndexTTS 2.5 (Hugging Face)](https://huggingface.co/indexteam/indextts-2.5) · [Informe técnico 2.5](https://arxiv.org/html/2601.03888v3) · [IndexTTS2 (artículo)](https://arxiv.org/abs/2506.21619v2)
- [Comparativa IndexTTS2 / Chatterbox / Qwen3-TTS](https://filmora.wondershare.com/answers/indextts2-vs-chatterbox-vs-qwen3-tts-voice-cloning.html) · [Qwen3-TTS y acentos](https://ocdevel.com/blog/20260302-qwen-tts-voice-cloning) · [Voces españolas para Qwen3-TTS](https://github.com/alblez/qwen3-tts-spanish-voices)
- [OmniVoice](https://huggingface.co/k2-fsa/OmniVoice) · [Seed-VC](https://arxiv.org/abs/2411.09943v1) · [TTS-Audio-Suite](https://github.com/diodiogod/TTS-Audio-Suite)
- [Bandit v2 (multilingüe)](https://arxiv.org/abs/2407.07275v2) · [Bandit v2 en MVSEP](https://mvsep.com/algorithms/45) · [MVSEP-CDX23](https://github.com/ZFTurbo/MVSEP-CDX23-Cinematic-Sound-Demixing) · [Problema al cargar Bandit](https://github.com/ZFTurbo/Music-Source-Separation-Training/issues/41)
- [pyannote vs NeMo](https://www.pyannote.ai/blog/pyannote-vs.-nvidia-nemo-diarization-accuracy-setup-and-production-readiness) · [Benchmarks de diarización](https://soniqo.audio/benchmarks/diarization)
- [pyVideoTrans](https://cdn.jsdelivr.net/gh/jianchang512/pyvideotrans@main/README.md) · [Doblaje local con IA](https://localaimaster.com/blog/local-ai-video-dubbing)
- [LLMs locales para traducir](https://insiderllm.com/guides/best-local-llms-translation/) · [ROCm vs Vulkan en AMD](https://glukhov.org/llm-hosting/comparisons/amd-rocm-vs-vulkan-llm-hosting/) · [ROCm en gráficas no soportadas](https://localaimaster.com/blog/rocm-unsupported-gpu-hsa-override)
