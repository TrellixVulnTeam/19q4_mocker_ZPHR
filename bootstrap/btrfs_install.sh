(
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
) 2>&1
