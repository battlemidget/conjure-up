from conjure.api.models import model_info
from conjure.utils import pollinate
from conjure.app_config import app
from conjure import controllers


def finish(back=False):
    """ handles deployment

    Arguments:
    back: if true returns to previous controller
    """
    if back:
        return controllers.use('jujucontroller')

    pollinate(app.session_id, 'PC')
    controllers.use('deploysummary')


def render(model):
    app.current_model = model
    info = model_info(app.current_model)

    # Set our provider type environment var so that it is
    # exposed in future processing tasks
    app.env['JUJU_PROVIDERTYPE'] = info['ProviderType']
