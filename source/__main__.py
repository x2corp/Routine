from discord.ext import commands
from logging import Formatter
import logging
import os, sys, pathlib
import yaml, discord
import asyncio

config_file = pathlib.Path(__file__).parents[0] / 'glob/config.yml'
with open(config_file) as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
            
class Routine(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
    
    async def setup_hook(self) -> None:
        for extension in os.listdir("./source/cogs"):
          if extension.endswith(".py"):
              await self.load_extension(f"source.cogs.{extension[:-3]}")

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)

        formatter = Formatter('[%(asctime)s | %(levelname)s] %(name)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    async def on_ready(self):
        print("Bot is running on user {0}, returned in {1}ms.".format(
            self.user.name, 
            round(self.latency, 1)
        ))

async def initialize(supplied_intents) -> None:
    async with Routine(
        command_prefix = config['prefix'],
        description = "Rhythm-game focused Discord bot",
        intents = supplied_intents
    ) as bot:
        await bot.start(config["token"])

intents = discord.Intents.default()
intents.message_content = True
asyncio.run(initialize(intents))