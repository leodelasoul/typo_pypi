class Packages(list):


    checked = False
    validated = False

    def __init__(self, downloads, project):
        self.project = project
        self.downloads = downloads

    def get_check(self):
        return self.checked

    def get_validate(self):
        return self.validated

    def set_check(self, checked):
        self.checked = checked

    def set_validate(self, validated):
        self.validated = validated

    def __getitem__(self, idx):
        return list.__getitem__(self, idx)