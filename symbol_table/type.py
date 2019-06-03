from attr import dataclass


class Type:
    def is_i32(self):
        return False

    def is_data(self):
        return False

    def is_void(self):
        return False

    def is_function(self):
        return False


class I32(Type):
    def is_i32(self):
        return True


class Void(Type):
    def is_void(self):
        return True


@dataclass
class Data(Type):
    name: str

    def is_data(self):
        return True
