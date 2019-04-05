
class AbstractStructure:
    pass

    @classmethod
    def from_dict(cls, dictionary):
        raise NotImplementedError("The child class must implement this method.")

    def to_dict(self):
        raise NotImplementedError("The child class must implement this method.")
