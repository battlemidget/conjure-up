class Spec:
    def __init__(self):
        self.friendly_name = None
        self.description = None
        self.cloud_whitelist = []
        self.packages = []
        self.options_whitelist = {}

    def pre_deploy(self):
        raise NotImplementedError

    def is_deploy_done(self):
        raise NotImplementedError

    def post_deploy(self):
        raise NotImplementedError
