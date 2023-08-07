import streamlit as st
import requests, os

from dotenv import load_dotenv

load_dotenv()

OPENAI_BASE = os.getenv("OPENAI_BASE", "https://api.openai.com/v1")
OPENAI_KEY = os.getenv("OPENAI_KEY")

TEMPLATE = """
Stable Diffusion is an AI art generation model similar to DALLE-2.
Below is a list of prompts that can be used to generate images with Stable Diffusion:

- portait of a homer simpson archer shooting arrow at forest monster, front game card, drark, marvel comics, dark, intricate, highly detailed, smooth, artstation, digital illustration by ruan jia and mandy jurgens and artgerm and wayne barlowe and greg rutkowski and zdislav beksinski
- pirate, concept art, deep focus, fantasy, intricate, highly detailed, digital painting, artstation, matte, sharp focus, illustration, art by magali villeneuve, chippy, ryan yee, rk post, clint cearley, daniel ljunggren, zoltan boros, gabor szikszai, howard lyon, steve argyle, winona nelson
- ghost inside a hunted room, art by lois van baarle and loish and ross tran and rossdraws and sam yang and samdoesarts and artgerm, digital art, highly detailed, intricate, sharp focus, Trending on Artstation HQ, deviantart, unreal engine 5, 4K UHD image
- red dead redemption 2, cinematic view, epic sky, detailed, concept art, low angle, high detail, warm lighting, volumetric, godrays, vivid, beautiful, trending on artstation, by jordan grimmer, huge scene, grass, art greg rutkowski
- a fantasy style portrait painting of rachel lane / alison brie hybrid in the style of francois boucher oil painting unreal 5 daz. rpg portrait, extremely detailed artgerm greg rutkowski alphonse mucha greg hildebrandt tim hildebrandt
- athena, greek goddess, claudia black, art by artgerm and greg rutkowski and magali villeneuve, bronze greek armor, owl crown, d & d, fantasy, intricate, portrait, highly detailed, headshot, digital painting, trending on artstation, concept art, sharp focus, illustration
- closeup portrait shot of a large strong female biomechanic woman in a scenic scifi environment, intricate, elegant, highly detailed, centered, digital painting, artstation, concept art, smooth, sharp focus, warframe, illustration, thomas kinkade, tomasz alen kopera, peter mohrbacher, donato giancola, leyendecker, boris vallejo
- ultra realistic illustration of steve urkle as the hulk, intricate, elegant, highly detailed, digital painting, artstation, concept art, smooth, sharp focus, illustration, art by artgerm and greg rutkowski and alphonse mucha

I want you to write me immediately give only one prompter of detailed prompts exactly about the idea written after IDEA. 

Follow the structure of the example prompts. 
This means a very short description of the scene, 
followed by modifiers divided by commas to alter the mood, style, lighting, and more.

IDEA: {idea}
"""

session = requests.Session()
session.headers.update(
    {
        "accept": "application/json",
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json",
    }
)


def make_prompt(text):
    url = OPENAI_BASE + "/chat/completions"
    payload = {
        "messages": [
            {"role": "user", "content": TEMPLATE.format(idea=text)},
        ],
        "model": "gpt-3.5-turbo-16k",
    }

    response = session.post(url, json=payload)
    return response.json()["choices"][0]["message"]["content"]


def stabble_difussion(prompt):
    url = OPENAI_BASE + "/images/generations"
    payload = {
        "prompt": prompt,
        "size": "512x512",
    }

    response = session.post(url, json=payload)
    return response.json()["data"][0]["url"]


if __name__ == "__main__":
    st.title("DALL-E Playground")

    text = st.text_input("Enter your idea here")
    if text:
        with st.spinner("Generating prompt..."):
            prompt = make_prompt(text)
        with st.spinner("Generating image..."):
            image = stabble_difussion(text)
        st.image(image, caption=prompt, use_column_width=True)
