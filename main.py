import openai
from dotenv import load_dotenv
import os
from discord.ext import commands
import discord


load_dotenv()

activity = discord.Activity(type=discord.ActivityType.watching, name="Reply with !r to a message",)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, activity=activity, status=discord.Status.idle)

openai.api_key = os.getenv("OPENAI_API_KEY")
DISCORD_KEY = os.getenv("DISCORD_KEY")

def generate_sarcastic_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Reply to this message in the same language with sarcasm : {prompt}",
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"].strip()

# prompt = "I'm so good at math."
# print(generate_sarcastic_response(prompt))


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command()
async def r(ctx):
    message = await ctx.channel.fetch_message(ctx.message.reference.message_id)

    # message_content = translator.translate(message.content)

    # keywords = modelling.get_keywords(message_content)
    # gif = gif_searcher.search_gif(keywords)

    # print(f'{ctx.author}, sending a gif to {message.author} with keywords {keywords}')
    
    response = generate_sarcastic_response(message.content)

    await ctx.send(response)


bot.run(DISCORD_KEY)