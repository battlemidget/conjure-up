from conjure.models.bundle import BundleModel

class CraftModelException(Exception):
    """ Exception in CraftModel """


class CraftModel:
    """ Stores craft metadata and containing bundles
    """

    def __init__(self, craft):
        if not isinstance(craft, dict):
            raise CraftModelException(
                "Craft metadata is not a dictionary")
        self.craft = craft
        self.name = craft.get('name', None)
        self.version = craft.get('version', None)
        self.summary = craft.get('summary', None)
        self.excerpt = craft.get('excerpt', None)
        self.maintainer = craft.get('maintainer', None)
        self._bundles = [BundleModel(b) for b in craft['bundles']]


    @property
    def bundles(self):
        """ Returns a list of Bundle model objects
        """
        return self._bundles
