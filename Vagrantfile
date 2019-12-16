Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"

  config.vm.provision "shell", path: "./bootstrap/setup_general.sh"
  config.vm.provision "shell", path: "./bootstrap/setup_links.sh"
  config.vm.provision "shell", path: "./bootstrap/setup_python.sh"

  config.vm.provision "shell", path: "./bootstrap/btrfs_install.sh"
  config.vm.provision "shell", path: "./bootstrap/volumes_create.sh"

  config.vm.provision "shell", path: "./bootstrap/volumes_mount.sh", run: "always"
end
