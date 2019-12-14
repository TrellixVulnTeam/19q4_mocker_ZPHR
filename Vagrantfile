$script = <<SCRIPT
(
sudo apt update
sudo apt install -y python3-pip

sudo apt --purge remove -y btrfs-tools
sudo apt install -y autoconf pkg-config
sudo apt install -y asciidoc xmlto --no-install-recommends
sudo apt install -y uuid-dev libattr1-dev zlib1g-dev libacl1-dev e2fslibs-dev libblkid-dev liblzo2-dev
git clone https://github.com/kdave/btrfs-progs.git
cd btrfs-progs
./autogen.sh
./configure --disable-documentation --disable-zstd --prefix=""
make
sudo make install
./configure --disable-documentation --disable-zstd
make 
sudo make install_python
cd ..

fallocate -l 1G ~/btrfs.img
sudo mkdir /var/mocker
mkfs.btrfs ~/btrfs.img
sudo mount -o loop,user_subvol_rm_allowed ~/btrfs.img /var/mocker
sudo chmod 777 /var/mocker

sudo ln -s /vagrant/mocker.py /usr/bin/mocker

/vagrant/tests/autotests.sh
) 2>&1
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.provision 'shell', inline: $script
end
