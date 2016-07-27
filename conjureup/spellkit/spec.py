class Spec:
    friendly_name = None
    description = None
    packages = []
    options_whitelist = {}
    _cloud_whitelist = []
    _cloud_blacklist = []

    @property
    def cloud_whitelist(self):
        return self._cloud_whitelist

    @property
    def cloud_blacklist(self):
        return self._cloud_blacklist

    @cloud_whitelist.setter
    def cloud_whitelist(self, val):
        if self.cloud_blacklist:
            raise Exception(
                "In order to use whitelist the cloud blacklist must be empty.")
        self._cloud_whitelist = val

    @cloud_blacklist.setter
    def cloud_blacklist(self, val):
        if self.cloud_whitelist:
            raise Exception(
                "In order to use blacklist the cloud whitelist must be empty.")
        self._cloud_blacklist = val

    def __repr__(self):
        return (
            "<Friendly Name: {}, Description: {}, "
            "Whitelist: {}, Blacklist: {}, Packages: {}, "
            "Options-Whitelist: {}>".format(self.friendly_name,
                                            self.description,
                                            self.cloud_whitelist,
                                            self.cloud_blacklist,
                                            self.packages,
                                            self.options_whitelist))
