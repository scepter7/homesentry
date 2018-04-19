import uuid
import os


class Alerter:
    def __init__(self, basePath="./", ext=".jpg"):
        self.name = "{rand}{ext}".format(rand=str(uuid.uuid4()), ext=ext)
        self.path = "{base_path}/{image_name}".format(base_path=basePath, image_name=self.name)
    
    def cleanup(self):
        os.remove(self.path)