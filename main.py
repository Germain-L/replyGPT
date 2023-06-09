import openai
from dotenv import load_dotenv
import os
from discord.ext import commands
import discord


load_dotenv()

activity = discord.Activity(
    type=discord.ActivityType.watching, name="!reply - !insult",)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents,
                   activity=activity, status=discord.Status.online)

openai.api_key = os.getenv("OPENAI_API_KEY")
DISCORD_KEY = os.getenv("DISCORD_KEY")


def generate_sarcastic_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Ecrit une insulte qui répond a ce message : {prompt}",
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"].strip()


def generate_chatgpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chatbot that replies with short answers in the language of the prompt"},
            {"role": "user", "content": prompt},
        ]
    )
    
    print(response)

    return response["choices"][0]["message"]["content"].strip()


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def reply(ctx):
    message = await ctx.channel.fetch_message(ctx.message.reference.message_id)

    response = generate_chatgpt_response(message.content)

    await ctx.send(response)

@bot.command()
async def insult(ctx):
    message = await ctx.channel.fetch_message(ctx.message.reference.message_id)

    response = generate_sarcastic_response(message.content)

    await ctx.send(response)


bot.run(DISCORD_KEY)
