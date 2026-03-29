import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import requests
import random
from PIL import Image, ImageTk  # for jfif logo

# Free OMDb API key: replace with your key
OMDB_API_KEY = "YOUR_OMDB_KEY"

class ARIBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("A.R.I - Artificial Response Intelligence")
        self.root.geometry("750x650")
        self.root.configure(bg="#0F0F0F")

        # Logo
        try:
            img = Image.open("ARI_BOT.jfif")
            img = img.resize((100, 100))  # scale the logo
            self.logo_img = ImageTk.PhotoImage(img)
            self.logo_label = tk.Label(root, image=self.logo_img, bg="#0F0F0F")
            self.logo_label.pack(pady=5)
        except:
            pass

        # Header
        self.header = tk.Label(
            root,
            text="A.R.I - Artificial Response Intelligence",
            font=("Helvetica", 16, "bold"),
            bg="#6A0DAD",
            fg="white",
            pady=12
        )
        self.header.pack(fill=tk.X)

        # Chat area
        self.chat_area = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            font=("Helvetica", 11),
            bg="#1C1C1C",
            fg="white",
            insertbackground="white"
        )
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)

        # Input area
        self.input_frame = tk.Frame(root, bg="#0F0F0F")
        self.input_frame.pack(fill=tk.X, padx=10, pady=10)

        self.user_input = tk.Entry(
            self.input_frame,
            font=("Helvetica", 12),
            bg="#1C1C1C",
            fg="white",
            insertbackground="white"
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,5))
        self.user_input.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            self.input_frame,
            text="Send",
            command=self.send_message,
            bg="#6A0DAD",
            fg="white",
            activebackground="#8A2BE2"
        )
        self.send_button.pack(side=tk.RIGHT)

        # Footer
        self.footer = tk.Label(
            root,
            text="Powered by A.R.I ",
            font=("Helvetica", 9),
            bg="#0F0F0F",
            fg="#888888"
        )
        self.footer.pack(pady=5)

        # Welcome message
        self.display_message(
            "A.R.I",
            "Hi there! I hope you're well. I'm ready to assist you. 😊",
            typing_effect=True
        )

    def display_message(self, sender, message, typing_effect=False):
        self.chat_area.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M")
        bubble = f"[{timestamp}] {sender}: "

        if typing_effect:
            self.chat_area.insert(tk.END, bubble)
            for char in message:
                self.chat_area.insert(tk.END, char)
                self.chat_area.update()
                self.chat_area.after(10)
            self.chat_area.insert(tk.END, "\n\n")
        else:
            self.chat_area.insert(tk.END, bubble + message + "\n\n")

        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

    def send_message(self, event=None):
        user_text = self.user_input.get()
        if not user_text.strip():
            return

        self.display_message("You", user_text)
        self.user_input.delete(0, tk.END)

        self.display_message("A.R.I", "Fetching data...", typing_effect=False)
        self.root.after(800, lambda: self.respond(user_text))

    def respond(self, user_text):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.delete("end-3l", "end-1l")
        self.chat_area.config(state=tk.DISABLED)

        response = self.generate_response(user_text)
        self.display_message("A.R.I", response, typing_effect=True)

    def generate_response(self, user_text):
        text = user_text.lower()

        if "hello" in text or "hi" in text:
            return "Hello. How may I assist you today?"

        if "time" in text:
            return f"The current time is {datetime.now().strftime('%H:%M:%S')}."

        if "weather" in text:
            return self.get_weather(text)

        if "bitcoin" in text or "crypto" in text:
            return self.get_crypto()

        if "news" in text:
            return self.get_news()

        if "movie" in text:
            return self.get_movie(text)

        if any(word in text for word in ["sad","stressed","tired","angry","upset"]):
            return self.therapist_mode()

        return "I'm still learning. Try asking about weather, crypto, news, or movies 😊"

    def get_weather(self, text):
        try:
            lat, lon = -26.2041, 28.0473
            if "in" in text:
                city = text.split("in")[-1].strip()
                cities = {"london": (51.5074,-0.1278), "new york": (40.7128,-74.0060)}
                if city.lower() in cities:
                    lat, lon = cities[city.lower()]
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            response = requests.get(url)
            data = response.json()
            temp = data["current_weather"]["temperature"]
            return f"The current temperature is {temp}°C 🌤"
        except:
            return "Sorry, I couldn't fetch the weather."

    def get_crypto(self):
        try:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
            response = requests.get(url)
            data = response.json()
            price = data["bitcoin"]["usd"]
            return f"Bitcoin is currently ${price} 💰"
        except:
            return "Sorry, I couldn't fetch crypto prices."

    def get_news(self):
        try:
            url = "https://api.spaceflightnewsapi.net/v4/articles/?limit=1"
            response = requests.get(url)
            data = response.json()
            headline = data["results"][0]["title"]
            return f"Latest headline: {headline} 📰"
        except:
            return "Sorry, I couldn't fetch news."

    def get_movie(self, text):
        try:
            if "movie" in text:
                movie_name = text.split("movie")[-1].strip()
                url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={movie_name}"
                response = requests.get(url)
                data = response.json()
                if data["Response"] == "True":
                    title = data["Title"]
                    year = data["Year"]
                    plot = data["Plot"]
                    rating = data["imdbRating"]
                    return f"{title} ({year}) ⭐{rating}\n{plot}"
                else:
                    return "Movie not found. Please check the title."
        except:
            return "Sorry, I couldn't fetch movie info."

    def therapist_mode(self):
        responses = [
            "I'm here for you. Do you want to talk about it?",
            "Take a deep breath. You're doing better than you think.",
            "It's okay to feel this way. Your feelings are valid.",
            "Remember: tough moments don't last forever."
        ]
        return random.choice(responses)

if __name__ == "__main__":
    root = tk.Tk()
    app = ARIBotGUI(root)
    root.mainloop()