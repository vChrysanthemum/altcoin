FROM ubuntu:16.04
COPY ./sources.list /etc/apt/sources.list

RUN apt-get update
RUN apt-get install -y ssh
RUN apt-get install -y vim
RUN apt-get install -y iputils-ping
RUN apt-get install -y net-tools
RUN apt-get install -y tmux
RUN apt-get install -y bash
RUN apt-get install -y dnsutils
RUN apt-get install -y python3 python3-pip

RUN pip3 install flask

RUN echo root:test | chpasswd

COPY ./sshd_config /etc/ssh/sshd_config
COPY ./tmux.conf /root/.tmux.conf
COPY ./entrypoint.sh /root/entrypoint.sh

RUN chmod 644 /etc/ssh/sshd_config

CMD [ "sh", "-c", "/root/entrypoint.sh; bash"]
