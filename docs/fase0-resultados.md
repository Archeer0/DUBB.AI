# Fase 0 — Resultados de las pruebas

Equipo: Ryzen 7 4800U, 30 GB RAM, solo CPU (salvo llama.cpp).
Fragmento: *Asesinato de Calidad* (1991), 7:30–9:30. Personajes: Barbara y George.

## Gráfica
- **PyTorch + ROCm 7.2:** no funciona. La gráfica gfx90c no está soportada y el truco `HSA_OVERRIDE_GFX_VERSION` se cierra con error.
- **llama.cpp + Vulkan:** funciona. Lectura de contexto ×2,8 y escritura ×1,2 respecto a la CPU.

## Separación de voz (30 s de audio)
| Modelo | Tiempo | Resultado |
|---|---|---|
| BS-RoFormer 1297 (2 pasadas) | 325 s (~11× tiempo real) | **Excelente**: fondo sin rastro de voz |
| MDX-Net Voc FT | 58 s | **Falla**: el fondo conserva todo el diálogo (también en estéreo). Descartado y borrado |

Decisión: BS-RoFormer para todo. Película entera ≈ 18–19 h en este PC.
Lección: conservar los canales originales (no convertir a mono).

## Voz clonada en castellano
Referencias: `pruebas/referencias/barbara.wav` (9 s), `george.wav` (11 s).

| Motor | Velocidad | Barbara | George |
|---|---|---|---|
| IndexTTS 2.5 | ~16× tiempo real (carga 15 s) | Natural, algo ronca (justificable), acento sin problemas | Natural, más estridente que el original, **acento latino** |
| Chatterbox Multilingual | ~6–8× tiempo real (carga 11 s) | **Acento latino**, ruido de fondo al final | **Acento latino** |
| Qwen3-TTS 1.7B Base | ~9× tiempo real | Mezcla de acento anglo-latino | Mezcla de acento anglo-latino |

Notas IndexTTS: necesita guardar con `soundfile` (el backend sox de torchaudio se rompe en Arch). Falta la normalización de texto en español (`nemo_text_processing`), que no es imprescindible.

**Chatterbox: descartado.** Acento latino en ambas voces y añade marca de agua inaudible (Perth).

**Plan B (voz castellana + conversión Seed-VC): descartado** por el usuario. El objetivo es la voz del actor original hablando castellano natural, no una voz intermedia retocada.

Nota: la frase de prueba usada para George ("¿Y qué otra cosa iba a hacer allí?…") la dice Barbara en la película. Las próximas pruebas usarán frases propias de George.

### Prueba: IndexTTS con dos referencias (timbre de George + entonación castellana)
Frase de George: "¿Por qué te escribe a ti? ¿Por qué no le escribe directamente a Jesús?"
- **Solo voz de George** (`indextts_george_2_solo.wav`): **preferida**. Mantiene las características de la voz original del actor y sale en **castellano perfecto** (la primera frase de George salió latina con la misma referencia: el acento varía entre generaciones).
- **George + muestra castellana como referencia de emoción** (`indextts_george_2_emo_castellana.wav`): muy buen castellano neutro, pero **deja de ser la voz del actor**. Descartada: la referencia de emoción también arrastra identidad vocal.

### VoicePowered v1 (F5-TTS ajustado a castellano): descartado
- Muy lento: ~65–77× tiempo real (unas 50 h de voz por película).
- El usuario lo descarta tras escucharlo: no merece la pena.

Regla general: **nunca usar el backend sox de torchaudio** (se cierra con error en Arch). Leer y guardar siempre con `soundfile`.

### Prueba: varias tomas con IndexTTS (solo voz de George), 5 tomas por frase
- Frase 1 ("¿Por qué te escribe a ti?…"): **las 5 con acento latino**. La toma original `indextts_george_2_solo.wav` (mismos ajustes) sigue siendo la única en castellano: ~1 de cada 6.
- Frase 2 ("¿Y tú cómo sabes que su marido enseña en Carne?"): acento latino poco evidente, pero presente en casi todas. Mejor: toma 2.
- Conclusión: repetir tomas no basta; el castellano sale por casualidad.

### Prueba: mezcla voz de George + muestra castellana (`emo_alpha`), frase 1
- 0.3 (`mezcla_0.3.wav`): **castellano sin perder la esencia de George**. Prometedora.
- 0.7: castellano muy conseguido, pero se parece menos al actor.
- Repetición con 0.3, 3 tomas por frase: frase 1 **las 3 latinas**; frase 2 solo la toma 2 en castellano. Con 0.3 el castellano sigue saliendo por casualidad (~2 de cada 7).
- 0.5: acento latino, entonación bastante parecida a George.
- **0.7: alternativa aceptable** si no hay nada mejor: más castellano, menos George, pero se acerca bastante.
- Repetición (3 tomas): **0.6** frase 1 → solo la toma 2 en castellano. **0.7** frase 1 → las 3 latinas; frase 2 → las 3 en castellano. Parecido a George prácticamente igual en todas.
- Conclusión provisional: ninguna mezcla garantiza castellano; la frase 1 tiende a latino casi siempre. Pendiente decidir: ajuste fino de IndexTTS con voces de España (necesita GPU alquilada o Mac) u otras vías.
