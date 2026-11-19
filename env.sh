# Carga con: source env.sh — manda modelos, cachés y temporales a la carpeta del proyecto (/home)
export DUBB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
export HF_HOME="$DUBB_ROOT/modelos/huggingface" TORCH_HOME="$DUBB_ROOT/modelos/torch"
export XDG_CACHE_HOME="$DUBB_ROOT/modelos/cache" UV_CACHE_DIR="$DUBB_ROOT/modelos/uv-cache"
export UV_PYTHON_INSTALL_DIR="$DUBB_ROOT/entornos/python" TMPDIR="$DUBB_ROOT/tmp"
mkdir -p "$TMPDIR"
