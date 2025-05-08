import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

application_id = os.environ['APP_ID']
bot_token = os.environ['BOT_TOKEN']

bot = commands.Bot(command_prefix='!', intents=intents, application_id=application_id)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'{bot.user} has connected to Discord!')

def evaluate_response(response):
    correct_answer = "jason"
    return response.lower() == correct_answer

@bot.tree.command(name='verify', description='Submit your answer')
async def verify(interaction: discord.Interaction, response: str):
    if evaluate_response(response):
        role = discord.utils.get(interaction.guild.roles, name="Verified")
        old_role = discord.utils.get(interaction.guild.roles, name="Unverified")
        if role and old_role:
            await interaction.user.add_roles(role)
            await interaction.user.remove_roles(old_role)
            await interaction.response.send_message("You have been verified! Please visit https://discordapp.com/channels/1368764933021634641/1368785712505159710 and read our rules to gain access to the rest of the server!", ephemeral=True)
    else:
        await interaction.response.send_message("That is not the correct answer! Please try again!", ephemeral=True)

@bot.event
async def on_interaction(interaction):
    if interaction.channel.id == 1368800194996736030:  # Replace CHANNEL_ID with the ID of the channel you want to monitor
        if interaction.type == discord.InteractionType.application_command:  # Check if the interaction is an application command
            return
        else:
            await interaction.response.send_message("This is not an application command", ephemeral=True)
            await interaction.delete_original_message()

@bot.event
async def on_message(message):
    if message.channel.id == 1368800194996736030:  # Replace CHANNEL_ID with the ID of the channel you want to monitor
        if not message.content.startswith(bot.command_prefix):  # Replace bot.command_prefix with your bot's command prefix
            await message.delete()
    await bot.process_commands(message)

reaction_roles = { '✅': 'Team Member'}

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 1370116495224475769:
        if payload.emoji.name == '✅':
            guild = bot.get_guild(payload.guild_id)
            member = await guild.fetch_member(payload.user_id)
            role = discord.utils.get(guild.roles, name=reaction_roles[payload.emoji.name]) 
            if role:
                try: 
                    await member.add_roles(role)
                    print(f'Assigned {role.name} to {member.name}')
                except Exception as e:
                    print("Error assigning role:", e)
        else:
            print("Emoji name mismatched.")

@bot.event
async def on_member_join(member):
    print(f"{member.name} has joined the guild!")
    
    guild = member.guild

    role = discord.utils.get(guild.roles, name="Unverified")
    if role:
        try:
            await member.add_roles(role)
            print(f"Role added to {member.name}")
        except discord.Forbidden:
            print(f"Bot does not have permission to add role to {member.name}")
        except discord.HTTPException as e:
            print(f"Error adding role to {member.name}: {e, text}")
    else:
        print(f"Role not found: Unverified")
    
    
    channel = bot.get_channel(1368764934019612803)
    await channel.send(f"Welcome to {member.guild.name}, {member.mention}! Please ensure you abide by {bot.get_channel(1368785712505159710).mention} at all times!")

bot.run(bot_token)
