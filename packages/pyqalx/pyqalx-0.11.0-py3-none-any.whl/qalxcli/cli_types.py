import json
from importlib import import_module
from json import JSONDecodeError

import click

from pyqalx import Bot, QalxSession
from pyqalx.config import UserConfig, BotConfig
from pyqalx.core.entities import QalxEntity
from pyqalx.factories.mixins import FactoryValidateMixin


class QalxImport(click.ParamType):
    """
    A custom type to handle how the cli does imports.
    Expects a string in the format `my.dotted.module:attr_to_import`.
    """

    name = "import path"

    def __init__(self, expected_class, is_instance=False, *args, **kwargs):
        """
        :param expected_class: The class that this import should be an
        instance/subclass of
        :param is_instance: Should we do an `isinstance` check?  Defaults to
        doing an `issubclass` check
        """
        self.expected_class = expected_class
        self.is_instance = is_instance
        super(QalxImport, self).__init__(*args, **kwargs)

    def convert(self, value, param, ctx):
        module_name, variable_name = value.split(":")
        try:
            module = import_module(module_name)
        except ImportError:
            self.fail(f"Failed to import `{module_name}`")
        if variable_name not in dir(module):
            self.fail(f"`{variable_name}` not found in `{module_name}`.")
        _import_target = getattr(module, variable_name)

        method = issubclass
        message = "a subclass"

        if self.is_instance:
            method = isinstance
            message = "an instance"
        if not method(_import_target, self.expected_class):
            self.fail(
                f"`{variable_name}` is not {message} "
                f"of `{self.expected_class.__name__}`."
            )
        return _import_target


class QalxFactoryStage(click.ParamType):
    """
    Custom click type for a factory stage. Checks that the stage plan exists in
    a plan
    """

    name = "factory stage"

    def convert(self, value, param, ctx):
        """
        Check the stage exists in the plan. The plan in parsed from the yml file
        path and the stage must exist in the stages of the provided plan
        """
        plan_yml_path = ctx.params.get("plan")
        plan_yml = FactoryValidateMixin.read_plan(plan_yml_path)
        plan = FactoryValidateMixin.load_plan(plan_yml)
        try:
            stage_exists = value in plan["factory"]["stages"]
        except (KeyError, TypeError):
            # Return the value and the validation can handle the rest
            return value
        if stage_exists:
            return value
        else:
            self.fail("The stage does not exist in the plan", param, ctx)


class QalxDict(click.ParamType):
    """
    Custom click type for key-value pair inputs. Allows such pairs to be passed
    as arguments from the CLI with the following syntax format: `<key>=<value>`.
    Also allows a user to pass a complex object using
    a JSON string: `<key>='{"complex": "structure"}'`
    """

    name = "qalx dict"

    def convert(self, value, param, ctx):
        """
        Check that the input is in the format: "<key>:<value>" and return as a
        dictionary
        """
        # Remove all whitespace
        key_val = "".join((i for i in value.split()))
        try:
            key, val = key_val.split("=")
            try:
                # Attempt to handle metadata being passed as a JSON string
                val = json.loads(val)
            except JSONDecodeError:
                # JSONDecodeError - the metadata is not JSON.  Save it as it is
                pass
            return {key: val}
        except ValueError:
            fail_msg = (
                f'Argument "{key_val}" is not in the expected '
                + '"<key>=<value>" format'
            )
            self.fail(fail_msg)


BOT_IMPORT = QalxImport(Bot, is_instance=True)
QALX_SESSION_IMPORT = QalxImport(QalxSession)
USER_CONFIG_IMPORT = QalxImport(UserConfig)
BOT_CONFIG_IMPORT = QalxImport(BotConfig)
QALX_ENTITY_IMPORT = QalxImport(QalxEntity)
QALX_FACTORY_STAGE = QalxFactoryStage()
QALX_DICT = QalxDict()
