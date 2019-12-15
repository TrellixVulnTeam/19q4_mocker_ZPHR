(
sudo mkdir /var/mocker
sudo mkdir /var/mocker/volumes

sudo fallocate -l 1G /var/mocker/volumes.img
sudo mkfs.btrfs /var/mocker/volumes.img
) 2>&1
