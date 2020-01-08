# Mocker: Basic Docker Implementation using Python

Based on [Bocker](https://github.com/p8952/bocker) - a basic docker implementation using Bash.

```
$ mocker help

usage: mocker [-h]
              {init,pull,rmi,images,ps,run,exec,logs,rm,commit,help,clean} ...

Docker Python implementation

optional arguments:
  -h, --help            show this help message and exit

mocker_commands:
  {init,pull,rmi,images,ps,run,exec,logs,rm,commit,help,clean}
    init                create image from directory
    pull                create image from dockerhub image (latest)
    rmi                 remove image
    images              list all image volumes
    ps                  list all container volumes
    run                 run command in isolated container based on image
                        (REQUIRES ROOT)
    exec                enter container and execute command (REQUIRES ROOT)
    logs                print container logs
    rm                  remove container and associated namespaces (REQUIRES
                        ROOT)
    commit              apply changes made in container to image
    help                print help
    clean               run rmi,rm on all images,containers (MAY REQUIRE ROOT)

```

### Includes:
- Gitlab CI
- Dockerfile for container environment setup
- Vagrantfile for vm setup

---

To launch tests in Vagrant:

```
$ vagrant up
$ vagrant ssh
$ /vagrant/tests/autotest.sh
```
