# Cómo trabajar en este proyecto

Lee `product.md` antes de empezar cualquier tarea.

## Comunicación
- Háblame siempre en español.
- Explícame las cosas **sin tecnicismos**. Si un término técnico es inevitable, explícalo en una frase.
- Sé breve: qué has hecho, qué falta y qué necesitas de mí.

## Aprobación
- **Pide mi aprobación antes de cualquier cambio grande:**
  - Nuevas dependencias o modelos.
  - Cambios de arquitectura o de estructura de carpetas.
  - Borrar archivos.
  - Cualquier descarga pesada.
- Si algo contradice `product.md`, avísame antes de hacerlo.

## Ritmo de trabajo
- Avanza en **pasos pequeños**: un paso, una cosa.
- **Comprueba cada paso** antes de pasar al siguiente: ejecútalo y enséñame el resultado.
- Si algo falla, dímelo tal cual. No lo escondas ni lo des por bueno.

## Estilo de código
- Usa el skill **Ponytail**: la solución más simple que funcione, sin abstracciones ni dependencias innecesarias.
- Python para todo lo relacionado con IA. FFmpeg/FFprobe para el vídeo y el audio.
- Todo debe funcionar solo con CPU. La GPU (CUDA, ROCm, Apple MPS) es un extra que se usa si está disponible.
- No depender de API comerciales de pago. Prioriza los modelos locales.
- No toques el Python del sistema: usa un entorno aislado para el proyecto.
