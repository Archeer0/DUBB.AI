# AI Movie Dubbing Studio

## Qué es

Aplicación de escritorio que dobla automáticamente películas y series del inglés al **castellano de España**. Sustituye solo los diálogos y conserva la voz de cada actor original mediante clonación vocal.

El funcionamiento normal **no depende de API comerciales de pago**. Los modelos se ejecutan preferentemente **en local**.

## Para quién

Uso **personal** enfocado a ver en castellano **cine clásico y series antiguas que nunca se doblaron** o que muy difícilmente se encuentran.

El uso es **exclusivamente privado** (visionado en casa). Los resultados no se publican ni se distribuyen.

## Qué problema resuelve

Hay muchas obras clásicas sin doblaje al castellano. Los subtítulos no siempre son una opción cómoda, y los doblajes automáticos actuales suenan artificiales: una sola voz genérica, sin emoción, mal sincronizada y con la música y los efectos dañados.

Esta app busca un doblaje **natural, expresivo y sincronizado**, en el que cada personaje conserva su timbre y personalidad propios.

## Particularidades del contenido

Por ser cine clásico, el audio original suele ser:
- Mono, o con pocos canales.
- Con ruido, siseo y calidad limitada.
- Con diálogos, música y efectos mezclados en una única pista.

La separación de voces y la transcripción deben funcionar bien en estas condiciones.

## Qué incluye

1. **Análisis del vídeo:** pistas de audio, vídeo y subtítulos, idiomas, canales y duración. Selección manual de la pista original si hay varias.
2. **Separación de audio:** diálogos por un lado y música, efectos y ambiente por otro, sin que estos últimos se pierdan.
3. **Transcripción:** texto completo con tiempos precisos, frases, pausas e interlocutores.
   - Si el vídeo trae subtítulos en inglés (incrustados o en .srt), se usan **opcionalmente** para corregir la transcripción.
4. **Personajes:** un identificador persistente por voz (`VOICE_001`, `VOICE_002`…), revisable y corregible a mano. Cada personaje tiene su perfil vocal.
5. **Traducción:** al castellano peninsular, teniendo en cuenta el contexto narrativo, el registro de cada personaje, las expresiones idiomáticas y la duración disponible. Nunca frase a frase de forma aislada.
6. **Clonación y generación de voz:** una voz distinta por personaje, clonada a partir del audio original, que conserva timbre, tono, ritmo y emoción. Cuando sea posible, se usa una referencia para la identidad vocal y otra para la emoción.
7. **Sincronización:** cada frase se ajusta a la duración original sin acelerar de forma poco natural. Se ajustan las pausas y se evitan los solapamientos. Prima la naturalidad sobre la sincronía perfecta.
8. **Mezcla final:** música, efectos y ambiente originales más los nuevos diálogos, con control de volumen y sin saturación. Se mantiene la configuración de canales original.
9. **Exportación:** MKV, MP4, pista de audio WAV, pista de diálogos aislada, subtítulos SRT en castellano y archivos del proyecto.
   - El vídeo **no se recodifica**.
   - Si el formato de vídeo original no cabe en un MP4 sin recodificar, se exporta solo el MKV y se avisa.

### Forma de trabajo de la app

- **Automática por defecto:** se mete la película y se obtiene el doblaje.
- **Control frase a frase disponible:** revisar y editar traducciones, regenerar frases, ajustar tiempos y corregir personajes. Cuanto peor sea el resultado automático, más se usará.
- **Guarda todos los resultados intermedios:** nunca se repite un cálculo ya hecho.
- **Se puede pausar y reanudar:** una película puede procesarse en varias sesiones.

### Añadido opcional (nunca por defecto)

- Un script aparte para **mejorar la calidad de imagen y sonido** del vídeo original. No forma parte del flujo normal.

## Qué NO incluye

- **Otros idiomas:** solo inglés → castellano de España. Ni español latino ni otros pares de idiomas.
- **Modificar la imagen:** ni sincronización labial ni retoques. La imagen original no se toca.
- **Depender de API comerciales de pago** para el funcionamiento normal.
- **Distribución pública:** la app y sus resultados son para uso privado.
- **Windows:** no se contempla.

## Requisitos de calidad

Por orden de prioridad:

1. Calidad de las voces.
2. Naturalidad de la interpretación.
3. Fidelidad a la identidad vocal del actor original.
4. Calidad de la traducción.
5. Sincronización.
6. Conservación de la música y los efectos.

Además:
- **No se sacrifica calidad para ganar velocidad.** Si hace falta, se procesa en varias sesiones.
- **La naturalidad está por encima de la sincronización perfecta.** Si hace falta, se usan traducciones alternativas más cortas o más largas para encajar en el tiempo.
- **Se conserva intacto** todo lo que no sean diálogos: imagen, música y efectos.
- Debe funcionar con **películas completas de varias horas**.

## Plataformas y hardware

- **Sistemas:** Linux (Arch, XFCE, X11) y macOS.
- **Requisito:** debe funcionar **solo con CPU**. Aprovechará la GPU cuando la haya:
  - NVIDIA (CUDA).
  - AMD (ROCm).
  - Mac con chip Apple (Metal/MPS).
- **Equipo de referencia** (el del desarrollador):
  - AMD Ryzen 7 4800U (8 núcleos, 16 hilos).
  - 30 GB de RAM.
  - Gráfica integrada Radeon Vega (gfx90c, 512 MB propios + memoria compartida). La aceleración por ROCm está por verificar.
  - Python 3.14 del sistema. El proyecto usará su propio Python 3.11 o 3.12, aislado.
  - FFmpeg 9.0.2.

## Nota sobre clonación de voz

Se clonan las voces de los actores originales sin autorización expresa de sus titulares. Se acepta **únicamente** porque el uso es privado y los resultados no se publican ni se distribuyen. Si en algún momento se quisiera compartir el resultado, habría que revisar esta decisión.

## Arquitectura

### Módulos

El programa se divide en módulos claramente separados:

1. Interfaz gráfica.
2. Extracción multimedia.
3. Separación de fuentes (voces, música y efectos).
4. Reconocimiento de voz.
5. Diarización: saber quién habla en cada momento.
6. Traducción.
7. Clonación vocal.
8. Sincronización.
9. Mezcla de audio.
10. Exportación.

### Cómo se comunican

- Cada etapa es un **programa independiente** que lee archivos de la carpeta del proyecto y escribe los suyos: audio en WAV y datos en JSON, un formato de texto estructurado.
- **Cambiar de motor de IA** en una etapa solo exige que el nuevo produzca los mismos archivos. El resto del programa no cambia.
- **Caché y reanudación:** si el archivo de salida de una etapa ya existe y está completo, esa etapa se salta. Nunca se repite una operación que terminó bien, y tras una interrupción se continúa desde el último punto guardado.

### Reglas técnicas

- **Modelos:** se descargan una vez y se guardan en una carpeta local.
- **Entornos aislados:** cada modelo tiene su propio entorno de Python cuando sus dependencias choquen con las de otro. Nunca se instala nada en el Python del sistema.
- **Archivos grandes:** se trabaja por fragmentos. Nunca se carga una película entera en memoria.
- **Sin API de pago:** el funcionamiento normal no depende de servicios comerciales de pago.

## Metodología y fases

### Antes de programar: análisis técnico

1. Analizar las tecnologías disponibles.
2. Investigar proyectos open source reutilizables.
3. Comparar modelos, licencias, calidad, requisitos de hardware y compatibilidad con Linux y macOS.
4. Proponer la arquitectura más adecuada y justificar las decisiones.
5. Identificar las limitaciones técnicas reales.
6. Dividir el desarrollo en fases verificables.

Si una tecnología no da resultados satisfactorios, se investigan alternativas antes de comprometer la arquitectura.

### Fases de desarrollo

1. Extracción de audio y análisis del vídeo.
2. Separación de diálogos, música y efectos.
3. Transcripción y diarización.
4. Traducción contextual al castellano.
5. Clonación vocal y generación de diálogos.
6. Sincronización y reconstrucción del audio.
7. Interfaz gráfica completa.
8. Exportación y pruebas con películas completas.

Cada fase debe quedar **funcionando y probada** antes de pasar a la siguiente.

Hasta la fase 7, la app se usa desde la terminal con un script. Mientras tanto, las correcciones se hacen editando a mano los archivos JSON.

Se acompaña de documentación, instrucciones de instalación y scripts de ejecución.

## Criterio de finalización

El resultado debe ser una **aplicación real y funcional**, no una demostración conceptual.

La prueba definitiva es procesar una secuencia de película con varios personajes y comprobar:

- Que los personajes se identifican correctamente.
- Que la traducción suena natural.
- Que las voces están diferenciadas y son consistentes.
- Que cada voz se parece razonablemente a la voz original del actor.
- Que la música y los efectos se conservan.
- Que la sincronización es correcta.
- Que no hay cortes, solapamientos ni distorsiones.
