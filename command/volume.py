import btrfsutil as btfrs

from .config import VOLUMES_PATH


class VolumeType:
    def __init__(self, name, prefix, ids_range, **properties):
        self.name = name
        self.prefix = prefix
        self.ids_range = ids_range
        self.properties = properties


IMAGE = VolumeType(
    'IMAGE', 'img_', range(1000), source='.mocker_src')
CONTAINER = VolumeType(
    'CONTAINER', 'ps_', range(2, 255), command='.mocker_cmd')
VOLUME_TYPES = [IMAGE, CONTAINER]


class Volume:
    def __init__(self, id, type):
        self.id = id
        self.type = type

    @staticmethod
    def get_image(id):
        return Volume(id, IMAGE)

    @staticmethod
    def get_container(id):
        return Volume(id, CONTAINER)

    def name(self):
        return self.type.prefix + str(self.id)

    def path(self):
        return VOLUMES_PATH / self.name()

    def exists(self):
        return self.path().exists()


class VolumeNotFoundError(Exception):
    pass


class NoFreeVolumeError(Exception):
    pass


def list_volumes(type_):
    print(type_.name + '_ID',
          'VOLUME_NAME',
          *[name.upper() for name in type_.properties.keys()],
          sep='\t')
    for volume in VOLUMES_PATH.iterdir():
        name = volume.name
        if not name.startswith(type_.prefix):
            continue

        properties = []
        for path in type_.properties.values():
            properties.append((volume / path).read_text().strip())

        id_ = name[len(type_.prefix):]
        print(id_, volume.name, *properties, sep='\t\t')


def delete_volumes(type_):
    for volume_path in VOLUMES_PATH.iterdir():
        name = volume_path.name
        if not name.startswith(type_.prefix):
            continue

        id_ = name[len(type_.prefix):]
        volume = Volume(id_, type_)
        delete(volume)


def get_free_volume(type_):
    for id in type_.ids_range:
        volume = Volume(id, type_)
        if not volume.exists():
            return volume
    raise NoFreeVolumeError(
        'No more slots for volume type  ' + type_.name +
        '. Delete some volumes with prefix ' + type_.prefix)


def create(type_):
    volume = get_free_volume(type_)
    btfrs.create_subvolume(str(volume.path()))
    for path in volume.type.properties.values():
        (volume.path() / path).touch()
    print('Created: ' + volume.name())
    return volume


def copy(source, target):
    if not source.exists():
        raise VolumeNotFoundError(source.name())
    if target.exists():
        delete(target)
    btfrs.create_snapshot(str(source.path()), str(target.path()))
    print('Copied: ' + source.name() + ' to ' + target.name())


def delete(volume):
    if not volume.exists():
        raise VolumeNotFoundError(volume.name())
    btfrs.delete_subvolume(str(volume.path()))
    print('Deleted: ' + volume.name())
