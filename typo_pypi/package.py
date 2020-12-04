class Package:
    harmful = False
    found_mal_code = None
    namesquat = False
    typosquat = False

    def __init__(self, project):
        self.project = project
        self.typos = []
    def __setitem__(self, key, value):
        self.typos = [1]
        self.typos[key] = value
    '''
    def __iter__(self):
        return self

    def __next__(self):
        num = self.num
        self.num += 1
        return num
'''
