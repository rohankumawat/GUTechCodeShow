# import libraries
import discord
from discord.ext import commands
import openai
import requests
import json
from PIL import Image
from io import BytesIO
import random
import credentials

# set up discord API
# Intents
intents = discord.Intents.default() 
intents.message_content = True

TOKEN = credentials.dis_TOKEN
# client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='!', intents=intents)
# print(TOKEN)

# set up OPENAI API
openai.api_key = credentials.open_TOKEN

dall_e_url = "https://api.openai.com/v1/images/generations"

# set up Pokemon API
def pokemon_info(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    else:
        return None

# generate prompts
def generate_prompt(pokemon1, pokemon2):
    # use the information about the two pokemon to generate a prompt
    prompt = "A fusion of " + pokemon1['name'] + " and " + pokemon2['name'] + " with the body of " + pokemon1['name'] + " and the " + pokemon2['types'][0]['type']['name'] + " of " + pokemon2['name']
    return prompt

def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )

    # get image url from response
    image_url = response['data'][0]['url']

    # download the image
    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))

    # convert image to PNG format
    png_image = BytesIO()
    image.save(png_image, format="PNG")
    png_image.seek(0)

    return png_image
    """
    #set up api endpoint
    # url = "https://api.openapi.com/v1/images/generations"

    #set up api headers
    #headers = {
    #    "Content-Type": "application/json",
    #    "Authorisation": f"Bearer {openai.api_key}"
    #}
    
    #set up api data
    #data = {
    #    "model": "image-alpha-001",
    #    "prompt": prompt,
    #    "num_images": 1,
    #    "size": 512,
    #    "response_format": "url"
    #}

    #make api request
    #response = requests.post(url, headers=headers, json=data)

    #if response.status_code == 200:
       # get image url from response
        image_url = response.json()['data'][0]['url']

        # download the image
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image.response.content))

        # comvert image to PNG format
        png_image = BytesIO()
        image.save(png_image, format="PNG")
        png_image.seek(0)

        return png_image
    
    else:
        return None
    """
# Discord Bot
    
@client.event
async def on_ready():
    print('Bot is Ready.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!fusion'):
        # parse input
        # extract the name of the two Pokemon's
        pokemon_names = message.content.split()
        print(pokemon_names[1])
        print(pokemon_names[2])

        #retrieve information about the two pokemon
        pokemon1 = pokemon_info(pokemon_names[1].lower())
        pokemon2 = pokemon_info(pokemon_names[2].lower())
        
        print(pokemon1)
        print(pokemon2)
        # generate a prompt using Open AI API
        prompt = generate_prompt(pokemon1=pokemon1, pokemon2=pokemon2)

        # generate prompt
        image = generate_image(prompt)

        # send image back to user on discord
        await message.channel.send(file=discord.File(image, 'fusion.png'))
'''
@client.command()
async def helpp(ctx):
    ctx.send("Hello there😊! I'm PokePool. I'm in a build stage right now. Try using '!fusion Pikachu Jigglypuff' or '!fusion Snorlax Eevee' or '!fusion Hypno Squirtle'")
'''

client.run(TOKEN)