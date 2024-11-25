from source.core.bot import Routine
import yaml, os

with open("config.yml", 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

bot = Routine(
    command_prefix = config['prefix'],
    description = "Akatsuki-focused Discord bot",
)

if __name__ == "__main__":
    for _, _, cogs in os.walk("cogs"):
        for cog in cogs:
            if cog.endswith(".py"):
                try:
                    cog = cog.replace(".py", "")
                    bot.load_extension(f"cogs.{cog}")
                except Exception as e:
                    raise Exception(e)
                else:
                    print(f"Loaded {cog}")

bot.run(config['token'])