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
app.title("Temelli Speech2Image Uygulaması")
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
    placeholder_text="Sözlü ifadeniz buraya gelecek ",
)
promt_input.place(x=10, y=10)


# FUNCTION
# Function that takes the prompt and makes API request

def apply_dinle():
    r=sr.Recognizer()

    with sr.Microphone(device_index=0) as source:
        promt_input.delete(0, tk.END)
        promt_input.insert(0,"Konuşur musunuz",)
        print("Konuşur musunuz")
        #r.pause_threshold = 1
        audio=r.listen(source)

    try:
        a=r.recognize_google(audio, language="tr")
        print("ifadeniz:"+str(a))
        global metin
        metin=str(r.recognize_google(audio, language="tr"))
        promt_input.delete(0, tk.END)
        promt_input.insert(0,r.recognize_google(audio, language="tr"))
    except sr.UnknownValueError:
        print("Ses algılanamadı")
    except sr.RequestError as e:
        print("Çıkarım yapılamadı:{0}".format(e))
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
dalle_button.configure(text="Dinle ve Çiz")
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
save_button.configure(text="Resmi Kaydet")
save_button.place(x=326, y=60)


# Running the App
app.mainloop()
