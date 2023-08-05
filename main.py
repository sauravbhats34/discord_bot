import discord
from discord import app_commands
from discord.ext import commands
from discord import ui
import time
import requests
from threading import Timer
from keep_alive import keep_alive

# send discord notificaiton to a channel
async def sendMessage(message):
  await discord.utils.get(bot.get_all_channels(),name='general').send(message)



# instantiate a discord client
#intents = discord.Intents.default()
#intents.message_content = True
#bot = discord.bot(intents=intents)
#client = discord.Client(intents=discord.Intents.all())
#client = discord.Client()


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
#bot = commands.Bot(intents=intents)


@bot.event
async def on_ready():
    print('Logged in as')
    # Loop over all guilds (servers) and channels the bot can see
    for guild in bot.guilds:
        print('Guild:', guild.name, guild.id)
        #for channel in guild.channels:
        #    print('  Channel:', channel.name, channel.id)
    print(f'You have logged in as {bot}')
    #await bot.get_channel(channel.id).send('bot is now online!')
    try: 
      synced = await bot.tree.sync()
      print(f"Synced {len(synced)} command(s)")
    except Exception as e:
      print(e)
#hello command
@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
  #await interaction.respsonse.send_message(f"Hey {interaction.user.mention}! this is a slash command!", ephemeral=True)
  await interaction.response.send_message("hello to you")

#say command  

@bot.tree.command(name="say")
@app_commands.describe(things_to_say = "what should I say?")
async def say (interaction: discord.Interaction, things_to_say:str):
  await interaction.response.send_message(things_to_say)


# Start check-in command
class StartCheckInModal(discord.ui.Modal):
  def __init__(self):
    super().__init__(title="Start")
    
    self.startcheckToday = discord.ui.TextInput(label='Today', style=discord.TextStyle.paragraph, required = True)
    self.add_item(self.startcheckToday)
    self.startcheckBlockers = discord.ui.TextInput(label='Blockers', required = False)
    self.add_item(self.startcheckBlockers)

  async def on_submit(self, interaction: discord.Interaction): 
    today = self.startcheckToday.value
    blockers = self.startcheckBlockers.value
    startcheckin = discord.Embed(title="Start", description="Today: " + today + "\nBlockers: " + blockers)
    await interaction.response.send_message(embeds=[startcheckin])

@bot.tree.command(name="checkin-start")
async def startcheckin(interaction: discord.Interaction):
  await interaction.response.send_modal(StartCheckInModal())

# End check-in command
class EndCheckInModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="End")

        self.endcheckToday = discord.ui.TextInput(label='Today', style=discord.TextStyle.paragraph, required=True)
        self.add_item(self.endcheckToday)
        self.endcheckCompleted = discord.ui.TextInput(label='Completed', style=discord.TextStyle.paragraph, required=True)
        self.add_item(self.endcheckCompleted)
        self.endcheckLeftover = discord.ui.TextInput(label='Leftover', required=False)
        self.add_item(self.endcheckLeftover)
        self.endcheckBlockers = discord.ui.TextInput(label='Blockers', required=False)
        self.add_item(self.endcheckBlockers)

    async def on_submit(self, interaction: discord.Interaction):
        today = self.endcheckToday.value
        completed = self.endcheckCompleted.value
        leftover = self.endcheckLeftover.value
        blockers = self.endcheckBlockers.value
        description = "Today: {}\nCompleted: {}\nLeftover: {}\nBlockers: {}".format(today, completed, leftover, blockers)
        endcheckin = discord.Embed(title="End", description=description)
        await interaction.response.send_message(embeds=[endcheckin])

@bot.tree.command(name="checkin-end")
async def endcheckin(interaction: discord.Interaction):
    await interaction.response.send_modal(EndCheckInModal())

  #

keep_alive()

BOT_TOKEN = 'OTM1ODIzOTc2OTI2NzAzNjI2.YfEP_g.npGnqbsfKvLuztoDf2RqzLvCK_4'
bot.run(BOT_TOKEN)
