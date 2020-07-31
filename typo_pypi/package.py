class Package:
    checked = False
    validated = False

    def __init__(self, project, downloads):
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


