


echo "*/10 * * * * $(pwd)/watch.sh" > crontab 


git submodule update --init --recursive --remote

REQUIREMENTS="$(pwd)/requirements.txt"
poetry export -f requirements.txt -o requirements.txt
cd Resume && poetry export -f requirements.txt -o requirements.txt; cd ..


docker build . -t flask-site



