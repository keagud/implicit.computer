VENV_PATH="./.venv/bin/python3"

OUTPUT_DIR="$1"

mkdir -p "$OUTPUT_DIR" || exit

$VENV_PATH ./Resume/render.py -f html -o "$OUTPUT_DIR/resume.html" || exit
$VENV_PATH ./Resume/render.py -f pdf -o  "$OUTPUT_DIR/resume.pdf" || exit

