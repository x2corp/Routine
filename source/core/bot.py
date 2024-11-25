from discord.ext import commands

class Routine(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def on_ready(self):
        print("Bot is up on", self.user.name)