import discord, asyncio
import os
import shutil
import subprocess
from discord.ext import commands
import json
import time
import sys
import datetime

if not os.path.exists('config.json'):
    data = {
        'token': "",
        'prefix': "",
    }
    with open('config.json', 'w') as f:
        json.dump(data, f)

config = json.loads(open("config.json","r").read())
token = config['token']
prefix = config['prefix']

def getembed(text):
    embed = discord.Embed(
        description=text,
        color=0x2f3136
    )
    return embed

def checkConfig():
    if not token == "" and not prefix == "":
        return
    else: 
        if token == "":
            config['token'] = input('What is your token?\n')
        if prefix == "":
            config['prefix'] = input('Please choose a prefix for your commands e.g "+"\n')
        open('config.json','w+').write(json.dumps(config,indent=4,sort_keys=True))
        print('The program will now close so everything works correctly.')
        time.sleep(5)
        sys.exit()
        return

Client = discord.Client()
Client = commands.Bot(
    description='cnr selfbot',
    command_prefix=config['prefix'],
    self_bot=True
)
Client.remove_command('help') 

def getav(url, user):
    return discord.Embed(title='Avatar', color=0x2f3136).set_image(url=url).set_footer(text=user)    

@Client.event
async def on_ready():
    
    os.system('cls')
    width = shutil.get_terminal_size().columns

    def ui():
        print()
        print()
        print("[+] Made by cnr [+]".center(width))
        print()
        print(f"Current User: {Client.user}".center(width))
        print(f"User ID: {Client.user.id}".center(width))
        print()
        print(f"Prefix: {prefix}".center(width))
        print(f"Date: {datetime.date.today().strftime('%d, %B %Y')}".center(width))
        print()
        print("Commands:".center(width))
        print(f" {prefix}av (displays a user's avatar)".center(width))
    ui()
 

    @Client.command(aliases=['avatar', 'pfp'])
    async def av(ctx):
        args = ctx.message.content.split()
        await ctx.message.delete()
        embed = None
        if len(ctx.message.mentions) == 0:
            if len(args) == 1:
                embed = getav(ctx.message.author.avatar_url, ctx.author)
            else:
                if not args[1].isdigit():
                    embed = getembed(f"**{args[1]}** is not a valid user.")
                    return await ctx.send(embed=embed,delete_after=30)
                user = Client.get_user(int(args[1]))
                if user == None:
                    return await ctx.send(embed=getembed(f"User ID **{args[1]}** is invalid."))
                embed = getav(user.avatar_url, user)
        else:
            embed = getav(ctx.message.mentions[0].avatar_url, ctx.message.mentions[0])
        await ctx.send(embed=embed,delete_after=30)

checkConfig()
Client.run(config['token'], bot=False, reconnect=True)