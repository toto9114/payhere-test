FROM python:3.11-buster

ENV PROJECT_DIR /srv/payhere

RUN apt-get update && apt-get upgrade -y \
    && pip3 install supervisor pipenv

RUN mkdir -p ${PROJECT_DIR} \
    && mkdir -p ${PROJECT_DIR}/logs \
    && useradd -u 1000 -ms /bin/bash -d /home/payhere -G sudo,staff,www-data payhere \
    && echo "payhere ALL=NOPASSWD: ALL" >> /etc/sudoers

WORKDIR ${PROJECT_DIR}
COPY . .

RUN PIP_NO_CACHE_DIR=true pipenv install --system --deploy
RUN chown -R payhere:payhere /srv

VOLUME ["/srv/payhere/logs"]
CMD ["./script/runserver.sh"]
