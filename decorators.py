def Service(suid):
    def inner(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs, suid=suid)
        return wrapper
    return inner

def WriteCharacteristic(write_characteristic):
    def inner(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs, write_characteristic=write_characteristic)
        return wrapper
    return inner

def ReadCharacteristic(read_characteristic):
    def inner(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs, read_characteristic=read_characteristic)
        return wrapper
    return inner