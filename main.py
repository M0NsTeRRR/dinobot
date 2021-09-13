import logging
from argparse import ArgumentParser

import toml

from bot import DinoBot

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")
logger = logging.getLogger(__name__)

parser = ArgumentParser()
parser.add_argument(
    "-c",
    "--config",
    action="store",
    dest="config",
    default="/etc/DinoBot/config.toml",
    help="Path to config file",
)
args = parser.parse_args()

logger.info(f"Bot started")
config = toml.load(args.config)
logger.info(f"Config loaded")

log_level = logging.getLevelName(config["log_level"])
logger.setLevel(log_level)
logger.info(f"Started bot with log level {logging.getLevelName(logger.level)}")

if len(config["sentry_dsn"]) > 0:
    import sentry_sdk

    sentry_sdk.init(
        config["sentry_dsn"],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=0.5,
    )

bot = DinoBot(config)

for extension in config["discord"]["initial_cogs"]:
    bot.load_extension(extension)

bot.run(config["discord"]["token"], bot=True, reconnect=True)
