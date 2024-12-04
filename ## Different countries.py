## Different countries
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser
import pyttsx3

# Sample data for friends, countries, and languages
friends_data = [
    {"name": "louis", "photo": "louis.jpg", "country": "South Africa", "language": "Afrikaans", "greeting": "Gelukkige verjaarsdag!", "flag": "south_africa_flag.jpg"},
    {"name": "kart", "photo": "kart.jpg", "country": "USA", "language": "English", "greeting": "Happy Birthday!", "flag": "usa_flag.jpg"},
    {"name": "bhunf", "photo": "bhunf.jpg", "country": "China", "language": "简体中文", "greeting": "生日快樂 (Shēngrì kuàilè)", "flag": "china_flag.jpg"},
    {"name": "indra", "photo": "indra.jpg", "country": "Indonesia", "language": " Bahasa Indonesia", "greeting": "Selamat ulang tahun!", "flag": "indonesia_flag.jpg"},
    {"name": "bot", "photo": "bot.jpg", "country": "Thailand", "language": "ไทย ", "greeting": "สุขสันต์วันเกิด (S̄uk̄hs̄ạnt̒ wạn keid)", "flag": "thailand_flag.jpg"},
    {"name": "hans", "photo": "hans.jpg", "country": "Germany", "language": "Deutsch", "greeting": "Alles Gute zum Geburtstag!", "flag": "germany_flag.jpg"},
    {"name": "ji", "photo": "ji.jpg", "country": "South Korea", "language": "한국어", "greeting": "생일 축하해요 (Saeng-il chugha haeyo)", "flag": "south_korea_flag.jpg"},
    {"name": "wei", "photo": "wei.jpg", "country": "Taiwan", "language": "繁體中文", "greeting": "生日快樂 (Shēngrì kuàilè)", "flag": "taiwan_flag.jpg"},
    {"name": "mei", "photo": "mei.jpg", "country": "Macau", "language": "粵式中文", "greeting": "生日快樂 (Shēngrì kuàilè)", "flag": "macau_flag.jpg"}
    {"name": "dong", "photo": "dong.jpg", "country": "Netherlands", "language": "Dutch", "greeting": "Gefeliciteerd met je verjaardag!", "flag": "netherlands_flag.jpg"}
]

# Sample options for languages
language_options = ["Afrikaans", "English", "简体中文", "Bahasa Indonesia", "ไทย", "Deutsch", "한국어","繁體中文","粵式中文","Nederlands"]

class GuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Guess the Country and Language Game")
        self.root.geometry("600x700")
        self.root.configure(bg="#ADD8E6")  # Change background color to light blue
        
        self.current_friend_index = 0
        self.score = 0
        self.selected_country = None
        self.selected_language = None
        
        self.engine = pyttsx3.init()  # 初始化语音引擎
        
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Fill out your name:", bg="#ADD8E6", font=("Helvetica", 12)).pack(pady=10)
        self.name_entry = tk.Entry(self.root, font=("Helvetica", 12))
        self.name_entry.pack(pady=5)

        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game, bg="#4CAF50", fg="white", font=("Helvetica", 12))
        self.start_button.pack(pady=20)

    def start_game(self):
        self.player_name = self.name_entry.get()
        if not self.player_name:
            messagebox.showwarning("Input Error", "Please enter your name to start the game.")
            return

        self.start_button.pack_forget()
        self.name_entry.pack_forget()
        
        self.condition_label = tk.Label(self.root, text="You need to get at least 70 points to win the prize :)", bg="#ADD8E6", font=("Helvetica", 12))

        self.condition_label.pack(pady=10)

        self.instructions_label = tk.Label(self.root, text="This game is designed to test how well you know your ten friends (some of whom might be really close to you). You need to identify their nationalities and the languages they speak. If you get both answers correct, you earn 10 points; otherwise, you get 0 points. The goal is to score above 70 points to win a special gift. If you don't reach 70 points, you'll need to try again to show more affection towards your friends. Good luck!", bg="#ADD8E6", font=("Helvetica", 12), wraplength=500, justify="left")
        self.instructions_label.pack(pady=10)

        self.root.after(5000, self.hide_initial_labels)  # 5秒后隐藏标签

        self.title_label = tk.Label(self.root, text="", bg="#ADD8E6", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=10)

        self.photo_label = tk.Label(self.root, bg="#ADD8E6")  # Change background color to light blue
        self.photo_label.pack(pady=20)

        tk.Label(self.root, text="Select Country:", bg="#ADD8E6", font=("Helvetica", 12)).pack()  # Change background color to light blue

        self.flag_frame = tk.Frame(self.root, bg="#ADD8E6")
        self.flag_frame.pack(pady=5)

        for friend in friends_data:
            flag_image = Image.open(friend["flag"])
            flag_image = flag_image.resize((100, 60), Image.LANCZOS)
            flag_photo = ImageTk.PhotoImage(flag_image)
            flag_button = tk.Button(self.flag_frame, image=flag_photo, command=lambda f=friend: self.select_country(f))
            flag_button.image = flag_photo
            flag_button.pack(side=tk.LEFT, padx=10)

        tk.Label(self.root, text="Select Language:", bg="#ADD8E6", font=("Helvetica", 12)).pack()  # Change background color to light blue

        self.language_frame = tk.Frame(self.root, bg="#ADD8E6")
        self.language_frame.pack(pady=5)

        for language in language_options:
            language_button = tk.Button(self.language_frame, text=language, command=lambda l=language: self.select_language(l), bg="#4CAF50", fg="white", font=("Helvetica", 10))
            language_button.pack(side=tk.LEFT, padx=10)

        self.submit_button = tk.Button(self.root, text="Submit Guess", command=self.check_guess, bg="#4CAF50", fg="white", font=("Helvetica", 12))
        self.submit_button.pack(pady=20)

        self.greeting_label = tk.Label(self.root, bg="#ADD8E6", font=("Helvetica", 12))  # Label to display greeting in selected language
        self.greeting_label.pack(pady=5)

        self.load_friend()

    def load_friend(self):
        friend = friends_data[self.current_friend_index]
        
        image = Image.open(friend["photo"])
        image = image.resize((250, 250), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        self.photo_label.config(image=photo)
        self.photo_label.image = photo

        self.title_label.config(text=f"How much do you know about {friend['name']}?")

    def select_country(self, friend):
        self.selected_country = friend["country"]

    def select_language(self, language):
        self.selected_language = language

    def check_guess(self):
        correct_country =  friends_data[self.current_friend_index]["country"]
        correct_language = friends_data[self.current_friend_index]["language"]
        correct_greeting = friends_data[self.current_friend_index]["greeting"]
        
        if (self.selected_country == friends_data[self.current_friend_index]["country"] and 
            self.selected_language == friends_data[self.current_friend_index]["language"]):
            messagebox.showinfo("Result", f"This is correct, Bao bao is so intelligent! {friends_data[self.current_friend_index]['greeting']}")
            greeting_text = friends_data[self.current_friend_index]["greeting"]
            self.greeting_label.config(text=greeting_text)
            self.score += 10
            
            # 使用语音引擎朗读生日快乐
            self.engine.say(greeting_text)
            self.engine.runAndWait()
        else:
            messagebox.showinfo("Result", f"So sorry but the correct answer is {correct_country} and {correct_language}.")
        # 使用语音引擎朗读生日快乐
            self.engine.say(correct_greeting)
            self.engine.runAndWait()
        
        self.current_friend_index += 1
        
        if self.current_friend_index < len(friends_data):
            self.load_friend()
            self.greeting_label.config(text="")
            self.selected_language = None
            self.selected_country = None
        else:
            if self.score >= 70:
                messagebox.showinfo("GG Well Play", f" Your score is {self.score}/{len(friends_data) * 10}, You are so smarrrrt! Congrats, check this out!")
                webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            else:
                messagebox.showinfo("Game Over", f"Game Over! Your score is {self.score}/{len(friends_data) * 10}.")
                play_again = messagebox.askyesno("Play Again?", "Your score is below 70. Do you want to try again?")
            if play_again:
                self.reset_game()
            else:
                self.root.quit()

    def reset_game(self):
        self.current_friend_index = 0
        self.score = 0
        self.selected_country = None
        self.selected_language = None
        self.condition_label.pack_forget()  # 隐藏条件标签
        self.load_friend()
        
if __name__ == "__main__":
    root = tk.Tk()
    game = GuessingGame(root)
    root.mainloop()