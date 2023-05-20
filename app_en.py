# IMPORTS
from auth import auth_token
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import requests

import speech_recognition as sr

# pip install openai + api connect
import openai
openai.api_key = auth_token


# Create app
app = tk.Tk()
app.geometry("532x632")
app.title("FB Speech2Image App")
app.configure(background="dark red")
ctk.set_appearance_mode("dark")

main_image = tk.Canvas(app, width=512, height=512)
main_image.place(x=10, y=110)
metin=""
# INPUT
# DALL•E 2 Prompt Input
promt_input = ctk.CTkEntry(
    master=app,
    height=40,
    width=512,
    font=("Arial", 20),
    text_color="black",
    fg_color="white",
    placeholder_text="==>Your verbal statement will go here<==",
)
promt_input.place(x=10, y=10)


# FUNCTION
# Function that takes the prompt and makes API request

def apply_dinle():
    r=sr.Recognizer()

    with sr.Microphone(device_index=0) as source:
        promt_input.delete(0, tk.END)
        promt_input.insert(0,"Do you speak...",)
        print("Do you speak...")
        #r.pause_threshold = 1
        audio=r.listen(source)

    try:
        a=r.recognize_google(audio, language="en")
        print("Your statement:"+str(a))
        global metin
        metin=str(r.recognize_google(audio, language="en"))
        promt_input.delete(0, tk.END)
        promt_input.insert(0,r.recognize_google(audio, language="en"))
    except sr.UnknownValueError:
        print("The sound could not be detected")
    except sr.RequestError as e:
        print("Could not be deducted:{0}".format(e))
    global tk_img
    global img

    prompt = str(a)
    response = openai.Image.create(prompt=prompt, n=1, size="512x512")
    image_url = response["data"][0]["url"]
    img = Image.open(requests.get(image_url, stream=True).raw)
    tk_img = ImageTk.PhotoImage(img)
    main_image.create_image(0, 0, anchor=tk.NW, image=tk_img)



# Function to save the image


def save_image():
    prompt = promt_input.get().replace(" ", "_")
    img.save(f"{prompt}.png")


# BUTTONS


# Button that triggers the above function
dalle_button = ctk.CTkButton(
    master=app,
    height=40,
    width=120,
    font=("Arial", 20),
    text_color="white",
    fg_color=("white", "gray38"),
    command=apply_dinle,
)
dalle_button.configure(text="Listen and Draw")
dalle_button.place(x=40, y=60)

# Button to save the image
save_button = ctk.CTkButton(
    master=app,
    height=40,
    width=120,
	font=("Arial", 20),
    text_color="white",
    fg_color=("white", "gray38"),
    command=save_image,
)
save_button.configure(text="Save to Image")
save_button.place(x=326, y=60)


# Running the App
app.mainloop()
