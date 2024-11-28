import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  
from PIL import Image, ImageTk
import random
import pygame

#Initialize pygame audio module
pygame.mixer.init()
# Initialize pygame mixer for sound effects
pygame.mixer.init()

#The name corresponding to the card
CARD_NAMES = {
    1: "Lucas",
    2: "Nancy",
    3: "Max",
    4: "Jonathan",
    5: "Dustin",
    6: "Eleven",
    7: "Steve",
    8: "Mike",
    9: "Robin"
}


class DraggableCard:
    def __init__(self, master, image_path, card_width=149, card_height=230, index=None):
        self.master = master
        self.original_image = self.load_image(image_path, card_width, card_height)
        self.card_image = self.original_image
        self.card = tk.Label(master, image=self.card_image)
        self.index = index
        self.name = CARD_NAMES.get(index)
        self.alternate_image = self.load_image(f'card_front_{index}.jpg', card_width, card_height)
        self.click_sound = pygame.mixer.Sound('clicksound.mp3')  # Load click sound effect

    def load_image(self, image_path, card_width, card_height):
        try:
            image = Image.open(image_path)
            image = image.resize((card_width, card_height), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except IOError:
            print(f"Unable to load image: {image_path}")
            return None

    def toggle_image(self):
        self.card_image, self.alternate_image = self.alternate_image, self.card_image
        self.card.config(image=self.card_image)

    def on_double_click(self, event):
        self.toggle_image()
        self.click_sound.play()  # Play the click sound effect

class CardGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Check The Card")
        self.root.geometry('1920x1080')
        self.background_image = ImageTk.PhotoImage(Image.open('background.png'))
        self.label = tk.Label(self.root, image=self.background_image)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)
        self.draggable_cards = []
        self.init_cards()  #Initialize card
        self.init_ui()

        # Load button click sound effect
        self.button_click_sound = pygame.mixer.Sound('startsound.mp3')  # Replace with your button click sound file path
        #Load background music
        self.music = pygame.mixer.music.load('background_music.mp3')  #Replace with your music file path
        #Loop playing background music
        pygame.mixer.music.play(-1)

    def init_cards(self):
        card_width = 149
        card_height = 230
        card_distance = 50
        rows = 3
        cols = 3
        center_x = 650  #Adjust the starting X coordinate according to your requirements
        center_y = 170  #Adjust the starting Y coordinate according to your requirements

        for i in range(1, 10):
            row = (i - 1) // cols
            col = (i - 1) % cols
            x = center_x + col * (card_width + card_distance)
            y = center_y + row * (card_height + card_distance)
            card = DraggableCard(self.root, 'cardback.jpg', card_width, card_height, i)
            card.card.grid(row=row, column=col, padx=card_distance, pady=card_distance)
            self.draggable_cards.append(card)
            card.card.bind('<Double-1>', card.on_double_click)

    def init_ui(self):
    #Load image
        self.start_game_image = self.load_image('button_background.png', 237, 290)
        if self.start_game_image:  #Check if the image was loaded successfully
        #Create a Button to display images and respond to click events
            self.start_game_button = tk.Button(self.root, image=self.start_game_image, command=self.start_game)
        #Place Button
            self.start_game_button.place(x=900, y=690, width=152, height=50)
        #Maintain reference to images
            self.start_game_button.image = self.start_game_image
        else:
            print("Failed to load button background image.")



    def load_image(self, image_path, width, height):
        try:
            image = Image.open(image_path)
            image = image.resize((width, height), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except IOError:
            print(f"Unable to load image: {image_path}")
            return None

    def start_game(self):
        self.button_click_sound.play()  # Play button click sound effect
        self.game_window = GameWindow(self.root)

class GameWindow:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("Find The Card")
        self.root.geometry('1920x1080')

        #Load background image
        self.background_image = ImageTk.PhotoImage(Image.open('custom_background.jpg'))
        self.label = tk.Label(self.root, image=self.background_image)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)

        # Load success and failure sound effects
        self.success_sound = pygame.mixer.Sound('successsound.mp3')  # Replace with your success sound file path
        self.failure_sound = pygame.mixer.Sound('gameover.mp3')  # Replace with your failure sound file path

        #Randomly select a name as the target
        self.target_index = random.randint(1, 9)
        self.target_name = CARD_NAMES[self.target_index]

        #Display target name
        self.name_label = tk.Label(self.root, text=f"  Find: {self.target_name}  ", font=("Helvetica", 36), fg='#FFFF00', bg='darkblue')
        self.name_label.place(x=950, y=450, anchor="center")

        #Create Card Button
        self.init_cards()

    def init_cards(self):
        card_width = 149
        card_height = 230
        card_distance = 50
        rows = 3
        cols = 3
        center_x = 650  #Half the width of the window minus half the width of the card
        center_y = 300  #Half of the window height minus half of the card height

        for i in range(1, 10):
            row = (i - 1) // cols
            col = (i - 1) % cols
            x = center_x + col * (card_width + card_distance)
            y = center_y + row * (card_height + card_distance)
            card_image = self.load_image('cardback.jpg', card_width, card_height)
            card_button = tk.Button(self.root, image=card_image, command=lambda idx=i: self.check_selection(idx))
            card_button.image = card_image  #Maintain reference to images
            card_button.grid(row=row, column=col, padx=card_distance, pady=card_distance)

    def load_image(self, image_path, width, height):
        try:
            image = Image.open(image_path)
            image = image.resize((width, height), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except IOError:
            print(f"Unable to load image: {image_path}")
            return None

    def check_selection(self, index):
        if index == self.target_index:
            self.show_custom_dialog('win_image.png')  # Replace with your victory image path
        else:
            self.show_custom_dialog('lose_image.png')  # Replace with your failed image path

    def show_custom_dialog(self, image_path):
        custom_dialog = tk.Toplevel(self.root)
        custom_dialog.title("")
        screen_width = custom_dialog.winfo_screenwidth()
        screen_height = custom_dialog.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 300) // 2
        custom_dialog.geometry(f'500x300+{x}+{y}')

        background_image = ImageTk.PhotoImage(Image.open(image_path))
        background_label = tk.Label(custom_dialog, image=background_image)
        image_width, image_height = background_image.width(), background_image.height()
        x = (500 - image_width) // 2
        y = (300 - image_height) // 2
        background_label.place(x=x, y=y)

        if 'win' in image_path:
            self.success_sound.play()  # Play success sound effect
        elif 'lose' in image_path:
            self.failure_sound.play()  # Play failure sound effect

        close_button = tk.Button(custom_dialog, text="Close", command=self.root.destroy)
        button_width = close_button.winfo_reqwidth()
        button_height = close_button.winfo_reqheight()
        x = 500 // 2 - button_width // 2
        y = 300 - button_height - 20
        close_button.place(x=x, y=y)

        custom_dialog.background_image = background_image

class StartWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Start Game")
        self.root.geometry('1920x1080')
        self.background_image = ImageTk.PhotoImage(Image.open('startbackground.png'))
        self.label = tk.Label(self.root, image=self.background_image)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)

        

        self.start_game_image = ImageTk.PhotoImage(Image.open('start_game.png'))
        self.start_game_button = tk.Label(self.root, image=self.start_game_image)
        self.start_game_button.place(x=950, y=750, anchor="center", width=165, height=55)
        self.start_game_button.bind("<Button-1>", self.start_game)

        self.quit_game_image = ImageTk.PhotoImage(Image.open('quit_game.png'))
        self.quit_game_button = tk.Label(self.root, image=self.quit_game_image)
        self.quit_game_button.place(x=950, y=850, anchor="center", width=165, height=55)
        self.quit_game_button.bind("<Button-1>", self.quit_game)

    def start_game(self, event=None):
        self.root.destroy()
        game_app = CardGameApp(tk.Tk())
        game_app.root.mainloop()

    def quit_game(self, event=None):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    start_window = StartWindow(root)
    root.mainloop()
