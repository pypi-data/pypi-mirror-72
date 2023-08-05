import os
import sys

import mlflow
from mlflow.tracking import MlflowClient

from pypads import logger
from pypads.utils.util import string_to_int


class MLFlowBackend:
    """
    Backend pushing data to mlflow
    """

    def __init__(self, uri, pypads):
        """
        :param uri: Location in which we want to write results.
        :param pypads: Owning pypads instance
        :return:
        """
        self._uri = uri
        self._pypads = pypads
        self._managed_result_git = None

        manage_results = self._uri.startswith("git://")

        # If the results should be git managed
        if manage_results:
            result_path = self._uri[5:]
            self._uri = os.path.join(self._uri[5:], "r_" + str(string_to_int(uri)), "experiments")
            self.manage_results(result_path)
            pypads.cache.add('uri', self._uri)

        # Set the tracking uri
        mlflow.set_tracking_uri(self._uri)

    def manage_results(self, result_path):
        """
        If we should push results for the user use a managed git.
        :param result_path: Path where the result git should be.
        :return:
        """
        self._managed_result_git = self.pypads.managed_git_factory(result_path)

        def commit(pads, *args, **kwargs):
            message = "Added results for run " + pads.api.active_run().info.run_id
            pads.managed_result_git.commit_changes(message=message)

            repo = pads.managed_result_git.repo
            remotes = repo.remotes

            if not remotes:
                logger.warning(
                    "Your results don't have any remote repository set. Set a remote repository for"
                    "to enable automatic pushing.")
            else:
                for remote in remotes:
                    name, url = remote.name, list(remote.urls)[0]
                    try:
                        # check if remote repo is bare and if it is initialize it with a temporary local repo
                        pads.managed_result_git.is_remote_empty(remote=name,
                                                                remote_url=url,
                                                                init=True)
                        # stash current state
                        repo.git.stash('push', '--include-untracked')
                        # Force pull
                        repo.git.pull(name, 'master', '--allow-unrelated-histories')
                        # Push merged changes
                        repo.git.push(name, 'master')
                        logger.info("Pushed your results automatically to " + name + " @:" + url)
                        # pop the stash
                        repo.git.stash('pop')
                    except Exception as e:
                        logger.error("pushing logs to remote failed due to this error '{}'".format(str(e)))

        self.pypads.api.register_teardown_fn("commit", commit, nested=False, intermediate=False,
                                             error_message="A problem executing the result management function was detected."
                                                           " Check if you have to commit / push results manually."
                                                           " Following exception caused the problem: {0}",
                                             order=sys.maxsize - 1)

    def add_result_remote(self, remote, uri):
        """
        Add a remote to track the results.
        :param remote: Remote name to be added
        :param uri: Remote address to be added
        :return:
        """
        if self.managed_result_git is None:
            raise Exception("Can only add remotes to the result directory if it is managed by pypads git.")
        try:
            self.managed_result_git.remote = remote
            self.managed_result_git.remote_uri = uri
            self.managed_result_git.repo.create_remote(remote, uri)
        except Exception as e:
            logger.warning("Failed to add remote due to exception: " + str(e))

    @property
    def uri(self):
        return self._uri

    @property
    def pypads(self):
        return self._pypads

    @property
    def managed_result_git(self):
        return self._managed_result_git

    @property
    def mlf(self) -> MlflowClient:
        return MlflowClient(self.uri)
