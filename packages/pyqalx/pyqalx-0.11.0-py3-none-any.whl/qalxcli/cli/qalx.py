from os import getcwd
import sys

import click
from click import ClickException

from pyqalx.config import UserConfig, BotConfig
from pyqalx.core.errors import QalxConfigProfileNotFound, QalxConfigFileNotFound
from qalxcli import cli_types


@click.group(chain=True)
@click.option(
    "-u",
    "--user-profile",
    help="User profile name in .qalx.",
    default="default",
)
@click.option(
    "-b", "--bot-profile", help="Bot profile name in .bots.", default="default"
)
@click.version_option()
@click.pass_context
def qalx(ctx, user_profile, bot_profile):
    """Command line interface to qalx."""
    ctx.ensure_object(dict)
    ctx.obj["USER_PROFILE"] = user_profile
    ctx.obj["BOT_PROFILE"] = bot_profile
    sys.path.append(getcwd())


@qalx.command("configure")
@click.option("--user/--no-user", default=True)
@click.option("--bot/--no-bot", default=True)
@click.argument("extra", nargs=-1, type=cli_types.QALX_DICT)
@click.pass_context
def configure(ctx, user, bot, extra):
    """
    Configures the .qalx and .bots config files.
    Usage:

    `qalx configure` - configures user and bot default profiles

    `qalx --user-profile=dev configure` - configures dev user profile and
    default bot profile

    `qalx --bot-profile=dev configure --no-user` - only configures bot dev
    profile.  Doesn't configure user profile

    `qalx configure --no-bot customkey=customvalue customkey2=customvalue2`
    - configures user profile with two extra key/values pairs on the config
    """

    if not user and not bot:
        raise ClickException(
            "`user` or `bot` must be specified otherwise no "
            "config files can be created.  Either call "
            "without any arguments or only use a "
            "single `--no-user` or `--no-bot` switch"
        )

    user_profile = ctx.obj["USER_PROFILE"]
    bot_profile = ctx.obj["BOT_PROFILE"]
    check_existing = []

    if user:
        check_existing.append((UserConfig, user_profile, "user"))
    if bot:
        check_existing.append((BotConfig, bot_profile, "bot"))

    for ConfigClass, profile_name, config_type in check_existing:
        # If the profiles already exist we just exit.  It's up to the user
        # to make any changes manually to the profile file - otherwise we risk
        # parsing the file incorrectly and overwriting data the user wants to
        # keep
        try:
            ConfigClass().from_inifile(profile_name)
            config_path = ConfigClass.config_path()
            raise ClickException(
                f"`{profile_name}` profile for config stored "
                f"at `{config_path}` "
                f"already exists.  To make changes you must "
                f"edit the config file directly or specify a "
                f"`--no-{config_type}` flag"
            )
        except (QalxConfigProfileNotFound, QalxConfigFileNotFound):
            # QalxConfigProfileNotFound: The specific profile could not be
            #                            found in the given ConfigClass file
            # QalxConfigFileNotFound: The specific file could not be found
            #                         for the given ConfigClass
            pass

    config_items = dict({k.upper(): v for d in extra for k, v in d.items()})

    if user:
        value = click.prompt("qalx Token", type=str)
        config_items["TOKEN"] = value
        UserConfig.configure(user_profile, config_items)
    if bot:
        BotConfig.configure(bot_profile)
