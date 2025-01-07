from discord.ext import commands
from logging import handlers, Formatter
from .. import cogs
import logging, yaml, os, discord

with open("config.yml", "r") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
            
class Routine(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def setup_hook(self) -> None:
        for extension in os.listdir("./source/cogs"):
          if extension.endswith(".py"):
              await self.load_extension(f"source.cogs.{extension[:-3]}")

        logger = logging.getLogger('main')
        logger.setLevel(logging.WARN)

        handler = handlers.BaseRotatingHandler(
            filename='Routine.log',
            mode='a',
            delay=True
        )

        datetime_format = '%d/%m/%Y %H:%M'
        formatter = Formatter('[{asctime} | {levelname}] {name}: {message}', datetime_format, style='{')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    async def on_ready(self):
        print("Bot is running on user {0}, returned in {1}ms.".format(
            self.user.name, 
            round(self.latency, 1)
        ))

async def create_client() -> None:
    async with Routine(
        command_prefix = config['prefix'],
        description = "Akatsuki-focused Discord bot",
        intents = discord.Intents.all()
    ) as bot:
        await bot.start(config["token"])

