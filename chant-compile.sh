#!/bin/bash
# Usage: chant-compile.sh path/to/file.tex  (relative to Chant/ root)
# Can also be called from the file's directory with just the filename.

CHANT_ROOT="$(cd "$(dirname "$0")" && pwd)"
RC="$CHANT_ROOT/.latexmkrc"

if [ -z "$1" ]; then
    echo "Usage: chant-compile.sh <path/to/file.tex>"
    exit 1
fi

# Resolve absolute path to the tex file
if [[ "$1" = /* ]]; then
    TEX="$1"
else
    TEX="$(pwd)/$1"
fi

DIR="$(dirname "$TEX")"
BASE="$(basename "$TEX")"

cd "$DIR" && latexmk -r "$RC" "$BASE"
