from discord.ext import commands
from discord import Color
import requests, json, discord

class Rhythia(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.AutoShardedBot = bot
        self.API_BASE: str = "https://development.rhythia.com/api/"
        self.SEARCH_USERS: str = "searchUsers"
        self.GET_PROFILE: str = "getProfile"
    
    @commands.command(
        aliases = ['rp', 'rhythiaprofile', 'rprofile'],
        pass_context = True
    )
    async def rhythia(self, ctx: commands.Context, username: str):
        if not username:
            await ctx.send('Please provide a valid username.'); return
        
        payload = {'text': username}
        request = requests.post(
            self.API_BASE + self.SEARCH_USERS,
            data = json.dumps(payload)
        )

        json_resp = request.json()
        json_data = json_resp['results']
        user_found = None

        for k in json_data:
            if k['username'] == username:
                user_found = k['id']
        
        if not user_found:
            if json_data[0]:
                user_found = json_data[0]['id']
            else:
                await ctx.send('Could not find that user.'); return
            
        user_payload = {
            'id': user_found,
            'session': self.bot.config['rhythia_session']
        }

        user_request = requests.post(
            self.API_BASE + self.GET_PROFILE,
            data = json.dumps(user_payload)
        )
        user_data = user_request.json()['user']

        embed = discord.Embed(
            colour = Color.from_rgb(46, 6, 36),
            description = ''
        )
        embed.set_author(
            name = 'Global profile for ' + user_data['username'], 
            url = 'https://rhythia.com/player/' + str(user_data['id']),
            icon_url = 'https://flagsapi.com/' + user_data['flag'] + '/flat/64.png'
        )
        embed.set_thumbnail(url = user_data['avatar_url'])

        information = ''
        information += '• **Global rank:** #' + str(user_data['position']) + '\n'
        information += '• **Skill points:** ' + str(round(user_data['skill_points'])) + 'rp\n'
        information += '• **Playcount:** ' + str(user_data['play_count']) + ' (' + str(user_data['squares_hit']) + ' hits)\n'
        embed.description = information
        
        if user_data['ban'] != "restricted": 
            footer = ('Currently' + (user_data['is_online'] and 'playing on Rhythia Online' or 'offline'))
        else:
            footer = 'User is currently restricted.'
            
        embed.set_footer(
            text =  footer,
            icon_url = 'https://www.rhythia.com/rhythia.png'
        )

        await ctx.channel.send(embed = embed)
        
async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(Rhythia(bot))
