import petname

from conjureup import async, controllers, juju, utils
from conjureup.app_config import app
from conjureup.controllers.clouds.common import list_clouds
from conjureup.ui.views.cloud import CloudView


class CloudsController:

    def __init__(self):
        self.view = None

    def __handle_exception(self, exc):
        utils.pollinate(app.session_id, "E004")
        app.ui.show_exception_message(exc)

    def __add_model(self):
        juju.add_model(app.current_model, app.current_controller)

    def finish(self, cloud):
        """ Load the Model controller passing along the selected cloud.

        Arguments:
        cloud: Cloud to create the controller/model on.
        """
        utils.pollinate(app.session_id, 'CS')
        existing_controller = juju.get_controller_in_cloud(cloud)

        if existing_controller is None:
            return controllers.use('newcloud').render(cloud)

        app.current_controller = existing_controller
        app.current_model = petname.Name()
        async.submit(self.__add_model,
                     self.__handle_exception,
                     queue_name=juju.JUJU_ASYNC_QUEUE)

        return controllers.use('deploy').render()

    def render(self):
        clouds = list_clouds()
        excerpt = app.config.get(
            'description',
            "Please select from a list of available clouds")
        view = CloudView(app,
                         clouds,
                         self.finish)

        app.ui.set_header(
            title="Choose a Cloud",
            excerpt=excerpt
        )
        app.ui.set_body(view)
        app.ui.set_footer('Please press [ENTER] on highlighted '
                          'Cloud to proceed.')


_controller_class = CloudsController
