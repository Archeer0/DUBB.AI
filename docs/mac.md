# Probar IndexTTS en el MacBook

Objetivo: medir si el Mac genera la voz más rápido que el PC (PC: ~90 s por frase de 5 s).

**Aviso:** IndexTTS usa unos 9 GB de memoria en el PC. Con un Mac de 8 GB tendrá que tirar del disco (memoria de intercambio) y probablemente irá más lento que el PC. La prueba solo sirve para confirmarlo.
Todo se instala dentro de la carpeta del proyecto; no toca nada del sistema salvo `uv`.

## 1. Programas básicos (una sola vez)
Abre **Terminal** y ejecuta:
```
xcode-select --install
curl -LsSf https://astral.sh/uv/install.sh | sh
```
- El primero instala `git` (si ya lo tienes, te lo dirá).
- El segundo instala `uv`, que gestiona Python sin tocar el del Mac. Cierra y vuelve a abrir Terminal después.

## 2. Bajar el proyecto
```
cd ~
git clone https://github.com/Archeer0/DUBB.AI.git
cd DUBB.AI
source env.sh
```
`source env.sh` hay que repetirlo **cada vez que abras una Terminal nueva**.

## 3. Instalar IndexTTS (unos 2–3 GB)
```
mkdir -p entornos && cd entornos
git clone https://github.com/index-tts/index-tts.git indextts
cd indextts && git checkout d9e41aa
uv venv --python 3.11 .venv
VIRTUAL_ENV=.venv uv pip install -e .
```

## 4. Descargar el modelo (unos 11 GB)
```
.venv/bin/python -c "from huggingface_hub import snapshot_download; snapshot_download('IndexTeam/IndexTTS-2.5', local_dir='../../modelos/indextts-2.5')"
```

## 5. Copiar los audios de prueba desde el PC
No están en GitHub. Copia (pendrive o red) estos archivos a las mismas carpetas dentro de `DUBB.AI`:
- `pruebas/referencias/george.wav`
- `pruebas/referencias/barbara.wav`
- `pruebas/voces/muestra.wav`

## 6. Prueba
Desde `DUBB.AI/entornos/indextts`:
```
PYTORCH_ENABLE_MPS_FALLBACK=1 .venv/bin/python ../../pruebas/tts_indextts.py ../../pruebas/referencias/george.wav ../../pruebas/voces/mac_george.wav "¿Por qué te escribe a ti? ¿Por qué no le escribe directamente a Jesús?"
```
- Al arrancar, el modelo elige solo la gráfica del Mac si puede.
- Al final muestra `Generación: N s`. Compáralo con el PC (~95 s).
- `PYTORCH_ENABLE_MPS_FALLBACK=1` hace que, si alguna operación no funciona en la gráfica del Mac, se haga en el procesador en vez de fallar.

Si algo falla, copia el mensaje de error completo y pégamelo.
