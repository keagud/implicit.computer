
OUTPUT_DIR="$1"

mkdir -p "$OUTPUT_DIR" || exit

node ./Resume/convert.js web || exit
node ./Resume/convert.js pdf || exit

cp ./Resume/output/output.pdf "$OUTPUT_DIR/resume.pdf" || exit
cp ./Resume/output/output.html "$OUTPUT_DIR/resume.html" || exit


