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
RUN apt-get install -y curl
RUN apt-get install -y jq

RUN pip3 install --upgrade pip
RUN pip3 install flask
RUN pip3 install requests

RUN echo root:test | chpasswd

COPY ./sshd_config /etc/ssh/sshd_config
COPY ./tmux.conf /root/.tmux.conf
COPY ./entrypoint.sh /root/entrypoint.sh
COPY ./bash_profile /root/.bash_profile

RUN chmod 644 /etc/ssh/sshd_config

RUN mkdir -p /root/.ssh
COPY ./sshkey/altcoin /root/.ssh/id_rsa
COPY ./sshkey/altcoin.pub /root/.ssh/id_rsa.pub
COPY ./sshkey/altcoin.pub /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/authorized_keys

COPY lib/* /usr/lib/x86_64-linux-gnu/

CMD [ "sh", "-c", "/root/entrypoint.sh; bash"]
