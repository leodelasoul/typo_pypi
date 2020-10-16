class Package:
    checked = False
    validated = False
    harmful = False
    namesquat = False
    def __init__(self, project ):
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

    def get_check(self):
        return self.checked

    def get_validate(self):
        return self.validated

    def set_check(self, checked):
        self.checked = checked

    def set_validate(self, validated):
        self.validated = validated
