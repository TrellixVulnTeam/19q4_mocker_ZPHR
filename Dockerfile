FROM ubuntu:xenial

RUN apt-get update && apt-get install -y sudo git

# for sudo use
RUN adduser --disabled-password --gecos '' docker
RUN adduser docker sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER docker

COPY ./bootstrap /bootstrap
ARG bootstrap_path=/bootstrap
RUN $bootstrap_path/setup_general.sh
RUN $bootstrap_path/setup_python.sh
RUN $bootstrap_path/btrfs_install.sh
RUN $bootstrap_path/volumes_create.sh
RUN $bootstrap_path/volumes_mount.sh

COPY . /vagrant
RUN $bootstrap_path/setup_links.sh

CMD ["/bin/bash", "-c", "/vagrant/bootstrap/volumes_mount.sh && /vagrant/tests/autotest.sh"]
