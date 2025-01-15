from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.AutoShardedBot = bot
    
    @commands.command(pass_context=True)
    async def latency(self, ctx):
        await ctx.send('Fully returned at {0}ms.'.format(round(self.bot.latency, 1)))

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(Utility(bot))