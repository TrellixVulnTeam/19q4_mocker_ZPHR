import os


def can_chroot():
    try:
        os.chroot('/')
    except PermissionError:
        return False
    else:
        return True


def with_logging(function):
    def wrapper(self, *args, **kwargs):
        print("mocker.py " + self.NAME + " ", end="")
        print(*[repr(arg) for arg in args], end="")
        print(*["=".join([key, repr(kwargs[key])])
                for key in sorted(kwargs.keys())])
        return function(self, *args, **kwargs)
    return wrapper
