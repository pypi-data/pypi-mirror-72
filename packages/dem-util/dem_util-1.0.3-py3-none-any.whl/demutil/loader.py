from .processor import DEMObject


class DEMLoader:
    def query(self, shape) -> DEMObject:
        pass

    def process(self):
        pass

    @classmethod
    class LoadFailedException(Exception):
        pass
