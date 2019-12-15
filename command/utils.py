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
        print(*["=".join([key, repr(val)]) for key, val in kwargs.items()])
        return function(self, *args, **kwargs)
    return wrapper
