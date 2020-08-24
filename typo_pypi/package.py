class Package:
    checked = False
    validated = False

    def __init__(self, project, downloads, typos, start=0):
        self.num = start
        self.project = project
        self.downloads = downloads
        self.typos = typos

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
