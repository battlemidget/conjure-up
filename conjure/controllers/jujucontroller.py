from conjure.ui.views.jujucontroller import JujuControllerView
from conjure.utils import pollinate
from conjure import juju
from ubuntui.ev import EventLoop
from conjure.models.bundle import BundleModel
from conjure import async
from functools import partial
import os.path as path
import os
from subprocess import check_output
import json
import petname


class TUI:
    def __init__(self, app):
        self.app = app

    def finish(self):
        self.app.log.debug("TUI finish")

    def render(self):
        self.app.log.debug("TUI render")


class GUI:
    def __init__(self, app):
        self.app = app
        self.cloud = None
        self.bootstrap = None
        self._post_bootstrap_pollinate = False

    def handle_exception(self, exc):
        pollinate(self.app.session_id, 'EB', self.app.log)
        self.app.ui.show_exception_message(exc)

    def finish(self, controller=None, back=False):
        """ Deploy to juju controller

        Arguments:
        controller: Juju controller to deploy to
        back: if true returns to previous controller
        """
        self.app.log.debug(
            "jujucontroller - selected: {}".format(controller))
        self.app.current_controller = controller

        if back:
            return self.app.controllers['welcome'].render()

        if self.bootstrap:
            self.app.log.debug("Performing bootstrap: {} {}".format(
                controller, self.cloud))
            future = juju.bootstrap_async(
                controller=self.app.current_controller,
                cloud=self.cloud,
                series=BundleModel.bootstrapSeries(),
                exc_cb=self.handle_exception,
                log=self.app.log)
            future.add_done_callback(
                self._handle_bootstrap_done)

            self.app.controllers['bootstrapwait'].render()
            pollinate(self.app.session_id, 'J003', self.app.log)

        else:
            self.app.controllers['deploy'].render(self.app.current_controller)

    def _handle_bootstrap_done(self, future):
        self.app.log.debug("handle bootstrap")
        result = future.result()
        if result.code > 0:
            self.app.log.error(result.errors())
            return self.handle_exception(Exception(result.errors()))
        pollinate(self.app.session_id, 'J004', self.app.log)
        EventLoop.remove_alarms()
        juju.switch(self.app.current_controller)
        self._post_bootstrap_exec()

    def _post_bootstrap_exec(self):
        """ Executes post-bootstrap.sh if exists
        """
        self._post_bootstrap_sh = path.join('/usr/share/',
                                            self.app.config['name'],
                                            'bundles',
                                            BundleModel.key(),
                                            'post-bootstrap.sh')
        if not path.isfile(self._post_bootstrap_sh) \
           or not os.access(self._post_bootstrap_sh, os.X_OK):
            self.app.log.debug(
                "Unable to execute: {}, skipping".format(
                    self._post_bootstrap_sh))
            return self.app.controllers['deploy'].render(
                self.app.current_controller)

        self.app.ui.set_footer('Running post-bootstrap tasks.')

        pollinate(self.app.session_id, 'J001', self.app.log)

        self.app.log.debug("post_bootstrap running: {}".format(
            self._post_bootstrap_sh
        ))

        try:
            future = async.submit(partial(check_output,
                                          self._post_bootstrap_sh,
                                          shell=True,
                                          env=self.app.env),
                                  self.handle_exception)
            future.add_done_callback(self._post_bootstrap_done)
        except Exception as e:
            return self.handle_exception(e)

    def _post_bootstrap_done(self, future):
        try:
            result = json.loads(future.result().decode('utf8'))
        except Exception as e:
            self.handle_exception(e)

        self.app.log.debug("post_bootstrap_done: {}".format(result))
        if result['returnCode'] > 0:
            pollinate(self.app.session_id, 'E001', self.app.log)
            return self.handle_exception(Exception(
                'There was an error during the post '
                'bootstrap processing phase: {}.'.format(result)))
        pollinate(self.app.session_id, 'J002', self.app.log)
        self.app.log.debug("Switching to controller: {}".format(
            self.app.current_controller))
        juju.switch(self.app.current_controller)
        self.app.controllers['deploy'].render(self.app.current_controller)

    def render(self, cloud=None, bootstrap=None):
        """ Render controller

        Arguments:
        cloud: defined cloud to use when deploying
        bootstrap: is this a new environment that needs to be bootstrapped
        """

        self.cloud = cloud

        # Set provider type for post-bootstrap
        self.app.env['JUJU_PROVIDERTYPE'] = self.cloud

        self.bootstrap = bootstrap

        if self.cloud and self.bootstrap:
            if self.app.current_controller is not None:
                return self.finish(self.app.current_controller)
            else:
                self.app.current_controller = petname.Name()
                return self.finish(self.app.current_controller)
            return self.handle_exception(Exception(
                "Unable to determine a controller to bootstrap"))
        else:
            controllers = juju.get_controllers().keys()
            models = {}
            for c in controllers:
                juju.switch(c)
                models[c] = juju.get_models()
            self.view = JujuControllerView(self.app,
                                           models,
                                           self.finish)

        self.app.ui.set_header(
            title="Juju Model",
        )
        self.app.ui.set_body(self.view)


def load_jujucontroller_controller(app):
    if app.headless:
        return TUI(app)
    else:
        return GUI(app)
