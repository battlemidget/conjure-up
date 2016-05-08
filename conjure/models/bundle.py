class BundleModelException(Exception):
    """ Exception in BundleModel """


class BundleModel:
    """ Stores bundle location for juju deploy
    """
    def __init__(self, bundle):
        self.key = bundle.get('key', None)
        self.name = bundle.get('name', None)
        self.summary = bundle.get('summary', None)
        self.revision = bundle.get('revision', None)
        self.location = bundle.get('location', None)
        self.blacklist = bundle.get('blacklist', [])
        self.whitelist = bundle.get('whitelist', [])
        self.recommendedCharms = bundle.get('recommendedCharms', [])
        self.bootstrapSeries = bundle.get('bootstrapSeries', None)

    def to_entity(self, use_latest=True):
        """ Returns proper entity key to query the charmstore.

        Arguments:
        use_latest: Use latest bundle revision from charmstore

        Returns:
        Formatted entity string suitable for charmstore lookup
        """
        if self.location is None and self.key is None:
            raise BundleModelException("Unable to determine bundle path.")
        if self.location:
            return self.location
        if not use_latest:
            return "{}-{}".format(self.key, self.revision)
        return self.key

    def to_path(self):
        """ Returns bundle path suitable for juju deploy <bundle>
        """
        bundle = self.key
        if bundle is None:
            raise BundleModelException("Unable to determine bundle")
        if self.revision is not None:
            bundle = "{}-{}".format(bundle, self.revision)
        return "cs:bundle/{}".format(bundle)
