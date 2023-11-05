FROM python:3.11.3-slim-buster
WORKDIR /web
# install dependencies

RUN apt-get update && apt-get -y install cron coreutils git
RUN pip install gunicorn
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .


RUN  git submodule update --init --recursive --remote
RUN pip install -r Resume/requirements.txt

RUN ln -s -f  Resume site_src/Resume
RUN sh watch.sh 

# set up cronjob to run ./watch.sh every 10 minutes
RUN mkdir -p /etc/cron.d/
RUN echo  "*/10 * * * * $(pwd)/watch.sh" > /etc/cron.d/watch-cron
RUN chmod 0644 "$(pwd)/watch.sh"
# cron requires all command end with newline
RUN echo "" >> /etc/cron.d/watch-cron
RUN chmod 0644 /etc/cron.d/watch-cron
RUN crontab /etc/cron.d/watch-cron

EXPOSE 8000

ENTRYPOINT [ "bash", "init.sh"]



