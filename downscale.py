from io import BytesIO
import numpy as np
import os 
import re
import cv2
import urllib

import discord
import yaml
from discord.ext import commands
from discord_slash import SlashCommand

import helpers

description = """downscale bot entirely in python"""


config = yaml.safe_load(open("./config.yml"))

bot = commands.Bot(
    command_prefix=config["bot_prefix"], description=description)

bot.remove_command("help")
# Declares slash commands through the bot.
slash = SlashCommand(bot, sync_commands=True) 


# imagrurl下载图片
def download_img_from_url(imageurl):
    req = urllib.request.Request(
            imageurl,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
            },
        )
    url = urllib.request.urlopen(req)
    image = np.asarray(bytearray(url.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
    return image
    
class Processor(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    def downscale_method(img,scale):
        # 缩放计算
        '''
        formula: w * (1/x * 100) / 100
                 h * (1/x * 100) / 100
        '''
        scale_percent = 1 / float(scale) * 100
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        image = cv2.resize(image, dim, interpolation=cv2.INTER_NEAREST)
        return image
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user.name} - {self.bot.user.id}")
        await bot.change_presence(
            status=discord.Status.online, activity=discord.Game("Downscale")
        )
        
    @slash.slash(name="help",description="description for downscale capacity")
    async def help(ctx):
        await ctx.send(
            """Commands:

`/image [url] --{0} [scaleFactor]` Downscale your image to scale what you want   

Example: `/image www.imageurl.com/image.png --downto 4x`""".format(
                bot.command_prefix
            )
        )
    
    @slash.slash
    async def downscale(ctx, input):
        '''
        downscale：downscale image to lower status for the goal that user use it
        '''
        imageurl = ""
        scale = 0
        result = "result.jpg"
        data = re.split(r'(?:,|;|\s)\s*', input)
        if len(data)!=2:
            await ctx.send("输入姿势有错误，请检查后，再试一次！")
            return 
        if re.match(r'^(?:http|ftp)s?://', data[0]) is not None:
            imageurl = data[0]
        if int(data[2]) > 0:
            scale = int(data[2])
        if imageurl == "" or scale == 0:
            await ctx.send("输入姿势有错误，请检查后，再试一次！")
            return 
        
        image = download_img_from_url(imageurl)
        filename = image[image.rfind("/") + 1:]
        
        await ctx.send("降分中.......")
        # 缩放图片到一定比例
        image = Processor.downscale_img(image, scale)
        
        data = BytesIO(
            cv2.imencode(".png", image, [cv2.IMWRITE_PNG_COMPRESSION, 16])[
                1].tostring()
        )
        
        await ctx.send("图片成功降分到{}".format(scale),file= discord.File(data, "{}.png".format(filename.split(".")[0])))
        

bot.add_cog(Processor(bot))

bot.run(config['bot_token'])
