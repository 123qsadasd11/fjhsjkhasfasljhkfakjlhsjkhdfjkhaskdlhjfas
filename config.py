import os
import json


class Config(object):

    def __init__(self, **kwargs):
        file = kwargs['file']
        mode = kwargs['mode']
        self.mode = mode
        self.file = file
        self.json = None
        if not os.path.exists(file):
            os.mkdir(file)
        if not os.path.isfile(file):
            f = open(file, 'a+')
            f.write(json.dumps({}))
            f.close()
            if mode == 'json':
                self.json = {}
            elif mode == 'enum':
                self.json = []
        else:
            f = open(file, 'r+')
            self.json = json.loads(f.read())
            f.close()

    def getAll(self):
        return self.json

    def set(self, get, set):
        if self.mode == 'json':
            try:
                self.json[get] = set
                return True
            except IndexError:
                return None
        elif self.mode == 'enum':
            self.json.append(set)

    def setAll(self, array):
        self.json = array

    def remove(self, get):
        try:
            del self.json[get]
        except IndexError:
            return

    def get(self, get):
        if self.mode == 'json':
            try:
                return self.json[get]
            except IndexError:
                return None
        elif self.mode == 'enum':
            return self.json[self.json.index(get)]

    def isset(self, issetcf):
        try:
            t = self.json[str(issetcf)]
            return True
        except:
            return False

    def save(self):
        f = open(self.file, 'w')
        f.write(json.dumps(self.json))
        f.close()
