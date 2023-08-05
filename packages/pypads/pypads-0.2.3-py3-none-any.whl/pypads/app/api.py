import os
from abc import ABCMeta
from contextlib import contextmanager
from functools import wraps
from typing import List, Iterable

import mlflow
from mlflow.utils.autologging_utils import try_mlflow_log

from pypads import logger
from pypads.app.injections.base_logger import FunctionHolder
from pypads.app.injections.run_loggers import PreRunFunction, PostRunFunction
from pypads.app.misc.caches import Cache
from pypads.app.misc.extensions import ExtendableMixin, Plugin
from pypads.bindings.anchors import get_anchor, Anchor
from pypads.importext.mappings import Mapping, MatchedMapping, make_run_time_mapping_collection
from pypads.importext.package_path import PackagePathMatcher, PackagePath
from pypads.utils.logging_util import WriteFormats, try_write_artifact, try_read_artifact, get_temp_folder, \
    _to_artifact_meta_name, _to_metric_meta_name, _to_param_meta_name
from pypads.utils.util import inheritors

api_plugins = set()


class Cmd(FunctionHolder, metaclass=ABCMeta):

    def __init__(self, *args, fn, **kwargs):
        super().__init__(*args, fn=fn, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.__real_call__(*args, **kwargs)


class IApi(Plugin):

    def __init__(self):
        super().__init__(type=Cmd)
        api_plugins.add(self)

    def _get_meta(self):
        """ Method returning information about where the actuator was defined."""
        return self.__module__

    def _get_methods(self):
        return [method_name for method_name in dir(self) if callable(getattr(object, method_name))]


def cmd(f):
    """
    Decorator used to convert a function to a tracked actuator.
    :param f:
    :return:
    """

    @wraps(f)
    def wrapper(self, *args, **kwargs):
        # self is an instance of the class
        return Cmd(fn=f)(self, *args, **kwargs)

    return wrapper


class PyPadsApi(IApi):
    """
    Default api functions of pypads
    """

    def __init__(self):
        super().__init__()

    @property
    def pypads(self):
        from pypads.app.pypads import get_current_pads
        return get_current_pads()

    # noinspection PyMethodMayBeStatic
    @cmd
    def track(self, fn, ctx=None, anchors: List = None, mapping: Mapping = None):
        """
        Method to inject logging capabilities into a function
        :param fn: Function to extend
        :param ctx: Ctx which defined the function
        :param anchors: Anchors to trigger on function call
        :param mapping: Mapping defining this extension
        :return: The extended function
        """

        # Warn if ctx doesn't defined the function we want to track
        if ctx is not None and not hasattr(ctx, fn.__name__):
            logger.warning("Given context " + str(ctx) + " doesn't define " + str(fn.__name__))
            ctx = None

        # If we don't have a valid ctx the fn is unbound, otherwise we can extract the ctx path
        if ctx is not None:
            if hasattr(ctx, '__module__') and ctx.__module__ is not str.__class__.__module__:
                ctx_path = ctx.__module__.__name__
            else:
                ctx_path = ctx.__name__
        else:
            ctx_path = "<unbound>"

        if anchors is None:
            anchors = [get_anchor("pypads_log")]
        elif not isinstance(anchors, Iterable):
            anchors = [anchors]

        _anchors = set()
        for a in anchors:
            if isinstance(a, str):
                anchor = get_anchor(a)
                if anchor is None:
                    anchor = Anchor(a, "No description available")
                _anchors.add(anchor)
            elif isinstance(a, Anchor):
                _anchors.add(a)

        # If no mapping was given a default mapping has to be created
        if mapping is None:
            logger.warning("Tracking a function without a mapping definition. A default mapping will be generated.")
            if '__file__' in fn.__globals__:
                lib = fn.__globals__['__file__']
            else:
                lib = fn.__module__

            # For all events we want to hook to
            mapping = Mapping(PackagePathMatcher(ctx_path + "." + fn.__name__), make_run_time_mapping_collection(lib),
                              _anchors, {"concept": fn.__name__})

        # Wrap the function of given context and return it
        return self.pypads.wrap_manager.wrap(fn, ctx=ctx, matched_mappings={MatchedMapping(mapping, PackagePath(
            ctx_path + "." + fn.__name__))})

    @cmd
    def start_run(self, run_id=None, experiment_id=None, run_name=None, nested=False, _pypads_env=None):
        """
        Method to start a new mlflow run. And run its setup functions.
        Every run is supposed to be an own execution. This may make sense if a single file defines multiple executions
        you want to track. (Entry to hyperparameter searches?)
        :param run_id: The id the run should get. This will be chosen automatically if None.
        :param experiment_id: The id the parent experiment has.
        :param run_name: A name for the run. This will also be chosen automatically if None.
        :param nested: If the run should be a nested run. (Run spawned in context of another run)
        :param _pypads_env: Pass the logging env if one is set.
        :return: The newly spawned run
        """
        out = mlflow.start_run(run_id=run_id, experiment_id=experiment_id, run_name=run_name, nested=nested)
        self.run_setups(_pypads_env)
        return out

    # ---- logging ----
    @cmd
    def log_artifact(self, local_path, meta=None):
        """
        Function to log an artifact on local disk. This artifact is transferred into the context of mlflow.
        The context might be a local repository, sftp etc.
        :param local_path: Path of the artifact to log
        :param meta: Meta information you want to store about the artifact. This is an extension by pypads creating a
        json containing some meta information.
        :return:
        """
        try_mlflow_log(mlflow.log_artifact, local_path)
        self._write_meta(_to_artifact_meta_name(os.path.basename(local_path)), meta)

    @cmd
    def log_mem_artifact(self, name, obj, write_format=WriteFormats.text.name, meta=None, preserve_folder=True):
        """
        See log_artifact. This logs directly from memory by storing the memory to a temporary file.
        :param name: Name of the new file to create.
        :param obj: Object you want to store
        :param write_format: Format to write to. WriteFormats currently include text and binary.
        :param meta: Meta information you want to store about the artifact. This is an extension by pypads creating a
        json containing some meta information.
        :param preserve_folder: Preserve the folder structure
        :return:
        """
        try_write_artifact(name, obj, write_format, preserve_folder)
        self._write_meta(_to_artifact_meta_name(name), meta)

    @cmd
    def log_metric(self, key, value, step=None, meta=None):
        """
        Log a metric to mlflow.
        :param key: Metric key
        :param value: Metric value
        :param step: A step for metrics which can change while executing
        :param meta: Meta information you want to store about the metric. This is an extension by pypads creating a
        json containing some meta information.
        :return:
        """
        mlflow.log_metric(key, value, step)
        self._write_meta(_to_metric_meta_name(key), meta)

    @cmd
    def log_param(self, key, value, meta=None):
        """
        Log a parameter of the execution.
        :param key: Parameter key
        :param value: Parameter value
        :param meta: Meta information you want to store about the parameter. This is an extension by pypads creating a
        json containing some meta information.
        :return:
        """
        mlflow.log_param(key, value)
        self._write_meta(_to_param_meta_name(key), meta)

    @cmd
    def set_tag(self, key, value):
        """
        Set a tag for your current run.
        :param key: Tag key
        :param value: Tag value
        :return:
        """
        return mlflow.set_tag(key, value)

    def _write_meta(self, name, meta):
        """
        Write the meta information about an given object name as artifact.
        :param name: Name of the object
        :param meta: Metainformation to store
        :return:
        """
        if meta:
            try_write_artifact(name + ".meta", meta, WriteFormats.text, preserve_folder=True)

    def _read_meta(self, name):
        """
        Read the metainformation of a object name.
        :param name:
        :return:
        """
        # TODO format / json / etc?
        return try_read_artifact(name + ".meta.txt")

    @cmd
    def metric_meta(self, name):
        """
        Load the meta information of a metric by given name.
        :param name: Name of the metric
        :return:
        """
        return self._read_meta(_to_metric_meta_name(name))

    @cmd
    def param_meta(self, name):
        """
        Load the meta information of a parameter by given name.
        :param name: Name of the parameter
        :return:
        """
        return self._read_meta(_to_param_meta_name(name))

    @cmd
    def artifact_meta(self, name):
        """
        Load the meta information of an artifact by given name.
        :param name: Name of the artifact
        :return:
        """
        return self._read_meta(_to_artifact_meta_name(name))

    # !--- logging ----

    # ---- run management ----
    @contextmanager
    @cmd
    def intermediate_run(self, **kwargs):
        """
        Spawn an intermediate nested run.
        This run closes automatically after the "with" block and restarts the parent run.
        :param kwargs: Other kwargs to pass to start_run()
        :return:
        """
        enclosing_run = mlflow.active_run()
        try:
            run = self.pypads.api.start_run(**kwargs, nested=True)
            self.pypads.cache.run_add("enclosing_run", enclosing_run)
            yield run
        finally:
            if not mlflow.active_run() is enclosing_run:
                self.pypads.api.end_run()
                self.pypads.cache.run_clear()
                self.pypads.cache.run_delete()
            else:
                mlflow.start_run(run_id=enclosing_run.info.run_id)

    def _get_setup_cache(self):
        """
        Get registered pre_run functions.
        :return:
        """
        if not self.pypads.cache.exists("pre_run_fns"):
            pre_run_fn_cache = Cache()
            self.pypads.cache.add("pre_run_fns", pre_run_fn_cache)
        return self.pypads.cache.get("pre_run_fns")

    @cmd
    def register_setup(self, name, pre_fn: PreRunFunction, silent=True):
        """
        Register a new pre_run function.
        :param name: Name of the registration
        :param pre_fn: Function to register
        :param silent: Ignore log output if pre_run was already registered.
        This makes sense if a logger running multiple times wants to register a single setup function.
        :return:
        """
        cache = self._get_setup_cache()
        if cache.exists(name):
            if not silent:
                logger.debug("Pre run fn with name '" + name + "' already exists. Skipped.")
        else:
            cache.add(name, pre_fn)

    @cmd
    def register_setup_fn(self, name, fn, nested=True, intermediate=True, order=0, silent=True):
        """
        Register a new pre_run_function by building it from given parameters.
        :param name: Name of the registration
        :param fn: Function to register
        :param nested: Parameter if this function should be called on nested runs.
        :param intermediate: Parameter if this function should be called on a intermediate run.
        An intermediate run is a nested run managed specifically by pypads.
        :param order: Value defining the execution order for pre run function.
        The lower the value the sooner a function gets executed.
        :param silent:
        :return:
        """
        self.register_setup(name, PreRunFunction(fn=fn, nested=nested, intermediate=intermediate, order=order),
                            silent=silent)

    @cmd
    def run_setups(self, _pypads_env=None):
        cache = self._get_setup_cache()
        fns = []
        for k, v in cache.items():
            fns.append(v)
        fns.sort(key=lambda f: f.order())
        for fn in fns:
            if callable(fn):
                fn(self, _pypads_env=_pypads_env)

    def _get_teardown_cache(self):
        """
        Register a new post run function.
        :return:
        """
        # General post run cache
        if not self.pypads.api.active_run():
            if not self.pypads.cache.exists("post_run_fns"):
                post_run_fn_cache = Cache()
                self.pypads.cache.add("post_run_fns", post_run_fn_cache)
            return self.pypads.cache.get("post_run_fns")

        # Post run cache for especially this run
        if not self.pypads.cache.run_exists("post_run_fns"):
            post_run_fn_cache = Cache()
            self.pypads.cache.run_add("post_run_fns", post_run_fn_cache)
        return self.pypads.cache.run_get("post_run_fns")

    @cmd
    def register_teardown(self, name, post_fn: PostRunFunction, silent=True):
        """
        Register a new post run function.
        :param name: Name of the registration
        :param post_fn: Function to register
        :param silent: Ignore log output if post_run was already registered.
        This makes sense if a logger running multiple times wants to register a single cleanup function.
        :return:
        """
        cache = self._get_teardown_cache()
        if cache.exists(name):
            if not silent:
                logger.debug("Post run fn with name '" + name + "' already exists. Skipped.")
        else:
            cache.add(name, post_fn)

    @cmd
    def register_teardown_fn(self, name, fn, error_message=None, nested=True, intermediate=True, order=0,
                             silent=True):
        """
        Register a new post_run_function by building it from given parameters.
        :param name: Name of the registration
        :param fn: Function to register
        :param error_message: Error message on failure.
        :param nested: Parameter if this function should be called on nested runs.
        :param intermediate: Parameter if this function should be called on a intermediate run.
        An intermediate run is a nested run managed specifically by pypads.
        :param order: Value defining the execution order for post run function.
        The lower the value the sooner a function gets executed.
        :param silent:
        :return:
        """
        self.register_teardown(name,
                               post_fn=PostRunFunction(fn=fn, message=error_message, nested=nested,
                                                       intermediate=intermediate, order=order), silent=silent)

    @cmd
    def active_run(self):
        """
        Get the currently active run
        :return: Active run
        """
        return mlflow.active_run()

    @cmd
    def is_intermediate_run(self):
        """
        Check if the current run is an intermediate run.
        :return:
        """
        enclosing_run = self.pypads.cache.run_get("enclosing_run")
        return enclosing_run is not None

    @cmd
    def end_run(self):
        """
        End the current run and run its tearDown functions.
        :return:
        """
        run = self.active_run()

        chached_fns = self._get_teardown_cache()
        fn_list = [v for i, v in chached_fns.items()]
        fn_list.sort(key=lambda t: t.order())
        for fn in fn_list:
            try:
                fn(self, _pypads_env=None)
            except (KeyboardInterrupt, Exception) as e:
                logger.warning("Failed running post run function " + fn.__name__ + " because of exception: " + str(e))

        mlflow.end_run()

        # --- Clean tmp files in disk cache after run ---
        folder = get_temp_folder(run)
        if os.path.exists(folder):
            import shutil
            shutil.rmtree(folder)
        # !-- Clean tmp files in disk cache after run ---
    # !--- run management ----


class ApiPluginManager(ExtendableMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(plugin_list=api_plugins)


pypads_api = PyPadsApi()


def api():
    """
    Returns classes of
    :return:
    """
    return inheritors(Cmd)
