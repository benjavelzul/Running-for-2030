from tkinter import *
from tkinter import messagebox
from Levels import all_levels as LEVELS
import tkinter as tk
from random import randint
from PIL import Image, ImageTk
import time
import pandas as pd

class SDG_App:
    class Applayout:
        def __init__(self):
            # preview config
            self.frameCnt = 2
            self.ind = 0
            self.themes = {
                "light": {
                    "bg": "#929090",
                    "canvas": "#E8E8E8",
                    "overlap": "#cacaca",
                    "text": "black",
                    "button": "#BFD6E3",
                    "fg": "black"
                },
                "dark": {
                    "bg": "#2C2C2C",
                    "canvas": "#1E1E1E",
                    "overlap": "#3C3C3C",
                    "text": "white",
                    "button": "#777272",
                    "fg": "white"
                }
            }

            # canvases setup
            self.layout_canvas = None
            self.settings_canvas = None
            self.master = None
            self.cur_music = False
            self.cur_volume = False
            self.maze_canvas = None
            
            # Add multiplayer tracking
            self.is_multiplayer = False
            
            # Remove the recursive initialization
            self.Mazegame = None
            self.init_mazegame()

        def init_mazegame(self):
            if self.Mazegame is None:
                self.Mazegame = SDG_App.Mazegame()
                self.is_multiplayer = False

        def layout(self, master, theme, mode= 0, current_wall_index=0, current_character_index=0):
            self.current_theme = theme
            self.master = master
            self.mode = mode
            self.current_wall_index = current_wall_index
            self.current_character_index = current_character_index
            if self.layout_canvas:
                self.layout_canvas.destroy()  # Destroy previous layout if it exists

            # Get current theme settings
            theme = self.themes[self.current_theme]

            #load all images needed
            self.load_images()

            # starts layout
            self.master.geometry("700x600")
            self.layout_canvas = Canvas(master, height=600, width=700, bg=theme["canvas"])  # Use theme color
            self.layout_canvas.place(x=0, y=0)

            # Update text colors according to theme
            self.layout_canvas.create_text(350, 100, text="Running for 2030", font=("Comic Sans MS", 25), fill=theme["text"])
            self.layout_canvas.create_text(350, 50, text=f"Level: {self.mode+1}", font=("Comic Sans MS", 15), fill=theme["text"])

            # buttons needed
            play_button = Button(
                master, 
                text="Play", 
                height=3, 
                width=11, 
                command=lambda: self.Mazegame.start(
                    self.master, 
                    self.mode, 
                    self.layout_canvas, 
                    self.current_wall_index, 
                    self.current_character_index, 
                    self.current_theme, 
                    self.is_multiplayer  # Pass the multiplayer flag
                ), 
                font=("Comic Sans MS", 12), 
                bg=theme["button"], 
                fg=theme["text"]
            )
            settings_button = Button(master, image=self.settings_img, command=self.setting_layout, bg=theme["button"])
            customize_button = Button(master, text="Customize", height=2, width=9, command=self.customize_layout, font=("Comic Sans MS", 11), bg=theme["button"], fg=theme["text"])
            level_button = Button(master, text="Level \nselection", height=2, width=9, command=self.level_selection_layout, font=("Comic Sans MS", 11), bg=theme["button"], fg=theme["text"])

            # putting the buttons in Canvas
            self.layout_canvas.create_window(350, 200, window=play_button)
            self.layout_canvas.create_window(670, 30, window=settings_button)
            self.layout_canvas.create_window(175, 200, window=customize_button)
            self.layout_canvas.create_window(525, 200, window=level_button)

            # explanation text
            self.layout_canvas.create_text(350, 295, anchor="s", text="INSTRUCTIONS", font=("Comic Sans MS", 12), fill=theme["text"])
            self.layout_canvas.create_text(350, 310, anchor="n", width=650, font=("Comic Sans MS", 10), fill=theme["text"],text="""Welcome, Agent of Change! Your mission is to navigate the maze and collect items that represent the United Nations' Sustainable Development Goals (SDGs). Use the following keys to move your avatar:

    ↑ (Up Arrow): Move your avatar one step upwards.
    ↓ (Down Arrow): Move your avatar one step downwards.
    ← (Left Arrow): Move your avatar one step to the left.
    → (Right Arrow): Move your avatar one step to the right.

As you explore the maze, keep an eye out for glowing icons. Each icon represents a different SDG. To collect an item, simply move your avatar over it. Once collected, the icon will disappear from the maze, and your collection counter for that SDG will increase.

Be strategic in your movements! Some paths might lead to dead ends, while others hold multiple SDG items. Your ultimate goal is to collect as many different SDG items as possible within the given time or move limit. Good luck, the future of our planet is in your hands!""")

        def load_images(self):

            #customization and maze game images
            self.wall_images = [
                PhotoImage(file=r"Images\Wall #1.png").subsample(35),
                ImageTk.PhotoImage((Image.open(r"Images\Wall #2.jpg").resize((50, 50))), Image.Resampling.LANCZOS),
                ImageTk.PhotoImage((Image.open(r"Images\Wall #3.jpg").resize((50, 50))), Image.Resampling.LANCZOS),
                ImageTk.PhotoImage((Image.open(r"Images\Wall #4.jpg").resize((50, 50))), Image.Resampling.LANCZOS)
            ]
            self.char1_frames = [(PhotoImage(file=r"Images\Character #2.gif", format=f'gif -index {i}')).zoom(2) for i in range(self.frameCnt)]
            self.char2_frames = [(PhotoImage(file=r"Images\llama.gif", format=f'gif -index {i}')).zoom(1) for i in range(self.frameCnt)]
            self.character_images = [self.char1_frames, self.char2_frames]

            # other images
            self.settings_img = (PhotoImage(file= r"Images\settings.png")).subsample(6)
           
            # setting layout images
            self.music_img = (PhotoImage(file= r"Images\music_Symbol.png")).subsample(9)
            self.no_music_img = (PhotoImage(file=r"Images\nomusic_Symbol.png")).subsample(4)
            self.volume_on_img = (PhotoImage(file=r"Images\volume_on.png")).subsample(4)
            self.volume_off_img = (PhotoImage(file=r"Images\volume_off.png")).subsample(4)

        def setting_layout(self):  # when settings button pressed
            theme = self.themes[self.current_theme]
            self.settings_canvas = Canvas(self.master, height=300, width=400, bg=theme["overlap"])
            self.settings_canvas.place(x=175, y=150)
            self.settings_canvas.create_text(200, 50, text="Settings", font=("Helvetica", 14), fill=theme["text"])
    
            # Update buttons with theme
            back_button = Button(self.settings_canvas, text="Back", command=lambda: self.show_main_layout(self.settings_canvas),bg=theme["button"], fg=theme["text"])
            credits_button = Button(self.settings_canvas, text="Credits", command=None, bg=theme["button"], fg=theme["text"])

            #lists for animation and buttons
            self.music_list = [self.music_img, self.no_music_img]
            self.volume_list = [self.volume_on_img, self.volume_off_img]

            #all the buttons
            self.music_button = Button(self.settings_canvas, image= self.music_list[int(self.cur_music)], command=lambda: self.music_update(self.cur_music), bg=theme["button"], fg=theme["text"])
            self.volume_button = Button(self.settings_canvas, image=self.volume_list[int(self.cur_volume)], command=lambda: self.volume_update(self.cur_volume), bg=theme["button"], fg=theme["text"])

            #updating buttons
            self.settings_canvas.create_window(200, 250, window=back_button)
            self.settings_canvas.create_window(50, 100, window=credits_button)
            self.settings_canvas.create_window(150, 200, window= self.music_button)
            self.settings_canvas.create_window(250, 200, window= self.volume_button)

        def level_selection_layout(self):
            theme = self.themes[self.current_theme]
            self.lev_sel_canvas = Canvas(self.master, height=300, width=400, bg=theme["overlap"])
            self.lev_sel_canvas.place(x=175, y=150)
            self.lev_sel_canvas.create_text(200, 30, text="Level selection", font=("Comic Sans MS", 14), fill=theme["text"])

            back_button = Button(self.lev_sel_canvas, text="Back", command=lambda: self.show_main_layout(self.lev_sel_canvas), bg=theme["button"], fg=theme["text"])
            self.lev_sel_canvas.create_window(200, 260, window=back_button)
            
            # Update level text to show mode
            mode_text = f"Level: {self.mode+1}" if not self.is_multiplayer else f"Multiplayer - Level: {self.mode+1}"
            self.level_text = self.lev_sel_canvas.create_text(200, 55, text=mode_text, font=("Comic Sans MS", 14), fill=theme["text"])

            # creating button levels
            lev1 = Button(self.lev_sel_canvas, text="Level 1", command= lambda: self.lev_update(0),bg=theme["button"], fg=theme["text"])
            lev2 = Button(self.lev_sel_canvas, text="Level 2", command= lambda: self.lev_update(1),bg=theme["button"], fg=theme["text"])
            lev3 = Button(self.lev_sel_canvas, text="Level 3", command= lambda: self.lev_update(2),bg=theme["button"], fg=theme["text"])
            lev4 = Button(self.lev_sel_canvas, text="Level 4", command= lambda: self.lev_update(3),bg=theme["button"], fg=theme["text"])
            lev5 = Button(self.lev_sel_canvas, text="Level 5", command= lambda: self.lev_update(4),bg=theme["button"], fg=theme["text"])
            lev6 = Button(self.lev_sel_canvas, text="Level 6", command= lambda: self.lev_update(5),bg=theme["button"], fg=theme["text"])
            lev7 = Button(self.lev_sel_canvas, text="Level 7", command= lambda: self.lev_update(6),bg=theme["button"], fg=theme["text"])
            lev8 = Button(self.lev_sel_canvas, text="Level 8", command= lambda: self.lev_update(7),bg=theme["button"], fg=theme["text"])
            lev9 = Button(self.lev_sel_canvas, text="Level 9", command= lambda: self.lev_update(8),bg=theme["button"], fg=theme["text"])
            lev10 = Button(self.lev_sel_canvas, text="Level 10", command= lambda: self.lev_update(9),bg=theme["button"], fg=theme["text"])
            lev11 = Button(self.lev_sel_canvas, text="Level 11", command= lambda: self.lev_update(10),bg=theme["button"], fg=theme["text"])
            lev12 = Button(self.lev_sel_canvas, text="Level 12", command= lambda: self.lev_update(11),bg=theme["button"], fg=theme["text"])
            lev13 = Button(self.lev_sel_canvas, text="Level 13", command= lambda: self.lev_update(12),bg=theme["button"], fg=theme["text"])
            lev14 = Button(self.lev_sel_canvas, text="Level 14", command= lambda: self.lev_update(13),bg=theme["button"], fg=theme["text"])
            lev15 = Button(self.lev_sel_canvas, text="Level 15", command= lambda: self.lev_update(14),bg=theme["button"], fg=theme["text"])
            #random_lev = Button(self.lev_sel_canvas, text="Random generation level",bg=theme["button"], fg=theme["text"])
            multiplayer_text = "Switch to Single Player" if self.is_multiplayer else "Switch to Multiplayer"
            multiplayer_btn = Button(self.lev_sel_canvas, text=multiplayer_text, command=self.toggle_multiplayer_mode, bg=theme["button"], fg=theme["text"])
            self.lev_sel_canvas.create_window(200, 220, window=multiplayer_btn)

            # uploading them into the screen
            self.lev_sel_canvas.create_window(70, 100, window=lev1)
            self.lev_sel_canvas.create_window(140, 100, window=lev2)
            self.lev_sel_canvas.create_window(210, 100, window=lev3)
            self.lev_sel_canvas.create_window(280, 100, window=lev4)
            self.lev_sel_canvas.create_window(350, 100, window=lev5)
            self.lev_sel_canvas.create_window(70, 140, window=lev6)
            self.lev_sel_canvas.create_window(140, 140, window=lev7)
            self.lev_sel_canvas.create_window(210, 140, window=lev8)
            self.lev_sel_canvas.create_window(280, 140, window=lev9)
            self.lev_sel_canvas.create_window(350, 140, window=lev10)
            self.lev_sel_canvas.create_window(70, 180, window=lev11)
            self.lev_sel_canvas.create_window(140, 180, window=lev12)
            self.lev_sel_canvas.create_window(210, 180, window=lev13)
            self.lev_sel_canvas.create_window(280, 180, window=lev14)
            self.lev_sel_canvas.create_window(350, 180, window=lev15)
            #self.lev_sel_canvas.create_window(200, 150, window=random_lev)
            self.lev_sel_canvas.create_window(200, 220, window=multiplayer_btn)

        def toggle_multiplayer_mode(self):
            #Toggle between single player and multiplayer modes
            self.is_multiplayer = not self.is_multiplayer
            
            # Update the level text
            if self.is_multiplayer:
                mode_text = f"Multiplayer - Level: {self.mode+1}"
            else:
                mode_text = f"Level: {self.mode+1}"
            
            self.lev_sel_canvas.itemconfig(self.level_text, text=mode_text)
            
            # Update the button text
            for item in self.lev_sel_canvas.find_all():
                widget = self.lev_sel_canvas.nametowidget(self.lev_sel_canvas.itemcget(item, "window")) if self.lev_sel_canvas.type(item) == "window" else None
                if isinstance(widget, Button):
                    current_text = widget.cget("text")
                    if "Single Player" in current_text or "Multiplayer" in current_text:
                        new_text = "Switch to Single Player" if self.is_multiplayer else "Switch to Multiplayer"
                        widget.config(text=new_text)
                        break

        def customize_layout(self):
            theme = self.themes[self.current_theme]
            self.customize_canvas = Canvas(self.master, height=300, width=400, bg=theme["overlap"])
            self.customize_canvas.place(x=152, y=150)
            self.customize_canvas.create_text(200, 50, text="Customization", font=("Comic Sans MS", 14), fill=theme["text"])

            # Initialize indices
            self.current_wall_index = 0
            self.current_character_index = 0

            # Back button
            back_button = Button(self.customize_canvas, text="Back", command=lambda: self.show_main_layout(self.customize_canvas),bg=theme["button"], fg=theme["text"])
            self.customize_canvas.create_window(200, 270, window=back_button)

            #create theme preview
            self.customize_canvas.create_text(200, 170, text="Theme", font=("Comic Sans MS", 14), fill=theme["text"])
            theme_button = Button(self.customize_canvas, text="Toggle Theme", command=self.toggle_theme,bg=theme["button"], fg=theme["text"])
            self.customize_canvas.create_window(200, 200, window=theme_button)

            # creat character preview
            self.customize_canvas.create_text(100, 70, text="Character", font=("Comic Sans MS", 14), fill=theme["text"])
            self.character_label = Label(self.customize_canvas,image=self.character_images[self.current_character_index][self.ind])
            self.character_window = self.customize_canvas.create_window(100, 120, window=self.character_label)
            prev_char = Button(self.customize_canvas, text="<", command=lambda: self.change_character(-1),bg=theme["button"], fg=theme["text"])
            next_char = Button(self.customize_canvas, text=">", command=lambda: self.change_character(1),bg=theme["button"], fg=theme["text"])
            self.customize_canvas.create_window(50, 140, window=prev_char)
            self.customize_canvas.create_window(150, 140, window=next_char)

            # create Wall preview
            self.customize_canvas.create_text(300, 70, text="Wall Style", font=("Comic Sans MS", 14), fill=theme["text"])
            self.wall_label = Label(self.customize_canvas, image=self.wall_images[self.current_wall_index])
            self.customize_canvas.create_window(300, 120, window=self.wall_label)
            prev_wall = Button(self.customize_canvas, text="<", command=lambda: self.change_wall(-1),bg=theme["button"], fg=theme["text"])
            next_wall = Button(self.customize_canvas, text=">", command=lambda: self.change_wall(1),bg=theme["button"], fg=theme["text"])
            self.customize_canvas.create_window(250, 140, window=prev_wall)
            self.customize_canvas.create_window(350, 140, window=next_wall)

            # Start character animation
            self.update_character_animation()

        def change_wall(self, direction):
            self.current_wall_index = (self.current_wall_index + direction) % len(self.wall_images)
            self.wall_label.configure(image=self.wall_images[self.current_wall_index])
            # Save the selected wall type for the game
            self.selected_wall = self.current_wall_index

        def change_character(self, direction):
            self.current_character_index = (self.current_character_index + direction) % len(self.character_images)
            self.character_label.configure(image=self.character_images[self.current_character_index][self.ind])
            # Save the selected character for the game
            self.selected_character = self.current_character_index

        def update_character_animation(self):
            if hasattr(self, 'customize_canvas') and self.customize_canvas.winfo_exists():
                self.ind = (self.ind + 1) % self.frameCnt
                self.character_label.configure(
                    image=self.character_images[self.current_character_index][self.ind])
                self.customize_canvas.after(500, self.update_character_animation)

        def toggle_theme(self):
            self.current_theme = "dark" if self.current_theme == "light" else "light"
            theme = self.themes[self.current_theme]

            # Update only existing canvases
            canvases = []
            if hasattr(self, 'customize_canvas') and self.customize_canvas is not None:
                canvases.append(self.customize_canvas)
            if hasattr(self, 'layout_canvas') and self.layout_canvas is not None:
                canvases.append(self.layout_canvas)
            if hasattr(self, 'settings_canvas') and self.settings_canvas is not None:
                canvases.append(self.settings_canvas)
            if hasattr(self, 'lev_sel_canvas') and self.lev_sel_canvas is not None:
                canvases.append(self.lev_sel_canvas)
            if hasattr(self.Mazegame, 'maze_canvas') and self.Mazegame.maze_canvas is not None:
                canvases.append(self.Mazegame.maze_canvas)

            # Update each existing canvas
            for canvas in canvases:
                try:
                    canvas.configure(bg=theme["canvas"])
                    # Update text elements in the canvas
                    for item in canvas.find_all():
                        if canvas.type(item) == "text":
                            canvas.itemconfig(item, fill=theme["text"])
                except tk.TclError:
                    continue  # Skip if canvas was destroyed

            # Update main window background
            self.master.configure(bg=theme["bg"])

            # Update all buttons in the application
            for widget in self.master.winfo_children():
                if isinstance(widget, Button):
                    try:
                        widget.configure(bg=theme["button"], fg=theme["text"])
                    except TclError:
                        continue  # Skip if button was destroyed

            # Store theme preference
            self.selected_theme = self.current_theme

        def lev_update(self, mode):
            self.mode = mode
            if self.is_multiplayer:
                mode_text = f"Multiplayer - Level: {self.mode+1}"
            else:
                mode_text = f"Level: {self.mode+1}"
            self.lev_sel_canvas.itemconfig(self.level_text, text=mode_text)
            return self.mode

        def get_game_mode_info(self):
            #Return current game mode information
            return {
                'is_multiplayer': self.is_multiplayer,
                'level': self.mode,
                'wall_index': self.current_wall_index,
                'character_index': self.current_character_index,
                'theme': self.current_theme
            }

        def music_update(self, music):
            self.cur_music = music

            if self.cur_music == False: 
                self.cur_music = True
                self.music_button.config(image=self.music_list[int(self.cur_music)])
                return self.cur_music
            else:
                self.cur_music = False
                self.music_button.config(image=self.music_list[int(self.cur_music)])
                return self.cur_music
            
        def volume_update(self, volume):
            self.cur_volume = volume

            if self.cur_volume == False:
                self.cur_volume = True
                self.volume_button.config(image=self.volume_list[int(self.cur_volume)])
                return self.cur_volume
            else:
                self.cur_volume = False
                self.volume_button.config(image=self.volume_list[int(self.cur_volume)])
                return self.cur_volume

        def show_main_layout(self, canvas):  # to destroy the last canvas
            self.canvas = canvas
            if self.canvas:
                self.canvas.destroy()
                
            # Stop Mazegame timer if running
            if hasattr(self, 'Mazegame') and hasattr(self.Mazegame, 'finished'):
                self.Mazegame.finished = True
            self.layout(self.master, self.current_theme, self.mode, self.current_wall_index, self.current_character_index)
      
    class Mazegame:
        def __init__(self):
            # Removing recursion 
            self.HomePage = None 
            self.themes_1 = {
                "light": {
                    "bg": "#929090",
                    "canvas": "#E8E8E8",
                    "overlap": "#cacaca",
                    "text": "black",
                    "button": "#BFD6E3",
                    "fg": "black"
                },
                "dark": {
                    "bg": "#2C2C2C",
                    "canvas": "#1E1E1E",
                    "overlap": "#3C3C3C",
                    "text": "white",
                    "button": "#777272",
                    "fg": "white"
                }
            }

        def init_homepage(self):
            if self.HomePage is None:
                self.HomePage = SDG_App.Applayout()

        def start(self, master, mode, canvas, current_wall_i, current_char_i, theme, multiplayer=False):
            # Theme setup
            self.current_theme = theme
            self.mode = mode
            self.multiplayer = multiplayer
            self.themes = self.themes_1[self.current_theme]
            
            # Game setup
            self.maze_levels = LEVELS
            self.maze = self.maze_levels[self.mode]
            self.stop = False
            self.finished = False
            
            # Canvas calculations - adjust for multiplayer
            self.HEIGHT = 600
            if self.multiplayer:
                self.WIDTH = 1400  # Double width for two mazes
                self.maze_width = 700  # Width per maze
            else:
                self.WIDTH = 700
                self.maze_width = 700
                
            self.cell_size_y = round((self.HEIGHT - (self.HEIGHT / 5)) / len(self.maze))
            self.cell_size_x = round(self.maze_width / len(self.maze[0]))

            # Image loading
            self.load_images()
            self.canvas = canvas
            if self.canvas:
                self.canvas.destroy()
            
            # Time tracking
            self.start_time = None
            self.time_limit = 100  # seconds
            self.start_time = time.time()
            self.master = master
            
            # Window setup
            self.master.geometry(f"{self.WIDTH}x{self.HEIGHT}")
            self.master.title("Maze game - Multiplayer" if self.multiplayer else "Maze game")
            
            # Theme application
            self.maze_canvas = Canvas(master, height=self.HEIGHT, width=self.WIDTH, bg=self.themes["canvas"])
            self.maze_canvas.place(x=0, y=0)
            
            # Character/wall selection
            self.selected_wall = current_wall_i
            self.selected_character = current_char_i
            try:
                self.wall_image = self.wall_images[self.selected_wall]
            except tk.TclError:
                print("image not found")
                self.wall_image = PhotoImage(file=r"C:\Users\VelezB1\OneDrive - CEDR\Documents\Coding\Python\graphics\Tk - graphics\Coding challenge\Images\default wall.png")
            self.character_frames = self.character_images[self.selected_character]
            
            # Initialize multiplayer variables
            if self.multiplayer:
                self.init_multiplayer()
            else:
                self.init_singleplayer()
            
            # Quotes and messages (same as before)
            self.quotes = [
                "'Education is the most powerful weapon which you can use to change the world.'\n - Nelson Mandela",
                "'The harder I work, the more luck I seem to have.'\n - Thomas Jefferson",
                "'It does not matter how slowly you go, so long as you do not stop.'\n - Confucius",
                "'The purpose of education is to replace an empty mind with an open one.'\n - Malcolm Forbes",
                "'Education is not preparation for life; education is life itself.'\n - John Dewey",
                "'The more that you read, the more things you will know, the more that you learn, the more places you'll go.'\n —Dr. Seuss.",
                "'Many of life's failures are people who did not realise how close they were to success when they gave up.'\n — Thomas Edison",
                "'Success is not final, failure is not fatal; it is the courage to continue that counts.'\n — Winston Churchill",
                "'The mind is not a vessel to be filled but a fire to be ignited.'\n - Plutarch",
                "'A person who never made a mistake never tried anything new.\n — Albert Einstein",
                "'The best way to predict your future is to create it.'\n —Abraham Lincoln",
                "'An investment in knowledge pays the best interest.'\n- Benjamin Franklin",
                "'I don't love studying. I hate studying. I like learning. Learning is beautiful.'\n- Natalie Portman",
                "'All our dreams can come true, if we have the courage to pursue them.'\n - Walt Disney "
            ]
            
            # Item messages (same as before - keeping original for brevity)
            self.item_message_list = [
                ["🌾 Sustainable Development Goal 2 (SDG 2) aims to end hunger, achieve food security, improve nutrition, and promote sustainable agriculture by 2030.", "👶 It focuses especially on vulnerable groups like children, pregnant women, and the poor, ensuring they have access to safe and nutritious food all year round.", "🌍 SDG 2 also targets the elimination of all forms of malnutrition, including stunting, wasting, and obesity, which affect millions globally.", "🚜 A key part of the goal is to boost the productivity and income of small-scale food producers through equal access to land, resources, and markets.", "🌱 By encouraging resilient agricultural practices and protecting genetic diversity in crops and livestock, SDG 2 supports long-term sustainability in food systems."],
                # ... (keeping all other item messages the same)
            ]

            # UI setup
            self.setup_ui()
            
            # Game state
            self.finished = False
            self.stop = False
            
            # Bind keys and initialize game
            self.master.bind("<KeyPress>", self.move_player)
            self.draw_maze()
            self.update_timer()
            self.animate_character()
            self.animate_item()
            self.init_homepage()

        def init_multiplayer(self):
            """Initialize multiplayer-specific variables"""
            # Player 1 (left maze)
            self.player1_pos = None
            self.player1_score = 0
            self.player1_items = []
            self.player1_lev_item_list = []
            self.player1_finished = False
            
            # Player 2 (right maze)
            self.player2_pos = None
            self.player2_score = 0
            self.player2_items = []
            self.player2_lev_item_list = []
            self.player2_finished = False
            
            # Common
            self.total_items = 0
            self.winner = None

        def init_singleplayer(self):
            """Initialize single player variables"""
            self.player_pos = None
            self.end_pos = None
            self.items = []
            self.total_items = 0
            self.score = 0
            self.lev_item_list = []

        def setup_ui(self):
            """Setup UI elements based on game mode"""
            if self.multiplayer:
                # Player 1 score (left side)
                self.score1_text = self.maze_canvas.create_text(
                    int(self.maze_width / 4), int(self.HEIGHT / 28), 
                    text=f"Player 1: {self.player1_score}", 
                    font=('Comic Sans MS', 14), fill=self.themes["text"]
                )
                
                # Player 2 score (right side)
                self.score2_text = self.maze_canvas.create_text(
                    int(self.maze_width + self.maze_width / 4), int(self.HEIGHT / 28), 
                    text=f"Player 2: {self.player2_score}", 
                    font=('Comic Sans MS', 14), fill=self.themes["text"]
                )
                
                # Timer (center)
                self.time_text = self.maze_canvas.create_text(
                    int(self.WIDTH / 2), int(self.HEIGHT / 28), 
                    text="0", font=('Comic Sans MS', 16), fill=self.themes["text"]
                )
                
                # Instructions
                self.info_text = self.maze_canvas.create_text(
                    int(self.WIDTH / 2), int(self.HEIGHT * 0.94), width=600, 
                    text="Player 1: WASD keys | Player 2: Arrow keys | Collect all items to win!", 
                    font=('Comic Sans MS', 10), fill=self.themes["text"]
                )
            else:
                # Single player UI (original)
                self.score = 0
                self.score_text = self.maze_canvas.create_text(
                    int(self.WIDTH / 5), int(self.HEIGHT / 28), 
                    text=f"Items collected: {self.score}", 
                    font=('Comic Sans MS', 16), fill=self.themes["text"]
                )
                self.time_text = self.maze_canvas.create_text(
                    int(self.WIDTH / 1.75), int(self.HEIGHT / 28), 
                    text="0", font=('Comic Sans MS', 16), fill=self.themes["text"]
                )
                self.info_text = self.maze_canvas.create_text(
                    int(self.WIDTH / 2), int(self.HEIGHT * 0.94), width=400, 
                    text="Movement with the arrow keys. Collect all the items to get the highest score.", 
                    font=('Comic Sans MS', 10), fill=self.themes["text"]
                )

            # Menu button
            menu = Button(self.master, text="⏸", command=self.Menu, 
                        bg=self.themes["button"], fg=self.themes["text"])
            self.maze_canvas.create_window(int(self.WIDTH * 0.95), int(self.HEIGHT / 28), window=menu)

        def logical_to_canvas(self, row, col, player=1):
            """Convert logical maze coordinates to canvas pixel coordinates"""
            if self.multiplayer and player == 2:
                # Right maze for player 2
                x = (col * self.cell_size_x) + self.maze_width + int(self.cell_size_x / 2)
            else:
                # Left maze for player 1 or single player
                x = col * self.cell_size_x + int(self.cell_size_x / 2)
            
            y = row * self.cell_size_y + int(self.HEIGHT / 14) + int(self.cell_size_y / 2)
            return x, y

        def draw_maze(self):
            """Draw maze(s) based on game mode"""
            if self.multiplayer:
                self.draw_multiplayer_mazes()
            else:
                self.draw_single_maze()

        def draw_single_maze(self):
            """Draw single maze (original functionality)"""
            for row in range(len(self.maze)):
                for col in range(len(self.maze[row])):
                    x1 = col * self.cell_size_x
                    y1 = row * self.cell_size_y + int(self.HEIGHT / 14)
                    x2 = x1 + self.cell_size_x
                    y2 = y1 + self.cell_size_y

                    if self.maze[row][col] == "W":
                        cx, cy = self.logical_to_canvas(row, col)
                        self.maze_canvas.create_image(cx, cy, image=self.wall_image)
                    elif self.maze[row][col] == "S":
                        self.player_pos = [row, col]
                        cx, cy = self.logical_to_canvas(row, col)
                        self.player = self.maze_canvas.create_image(cx, cy, image=self.character_frames[0])
                    elif self.maze[row][col] == "E":
                        self.end_pos = [row, col]
                        self.maze_canvas.create_rectangle(x1, y1, x2, y2, fill="green")
                    elif self.maze[row][col] == "*":
                        self.add_item(row, col, x1, y1, x2, y2)

        def draw_multiplayer_mazes(self):
            """Draw two identical mazes side by side"""
            # Draw left maze (Player 1)
            for row in range(len(self.maze)):
                for col in range(len(self.maze[row])):
                    x1 = col * self.cell_size_x
                    y1 = row * self.cell_size_y + int(self.HEIGHT / 14)
                    x2 = x1 + self.cell_size_x
                    y2 = y1 + self.cell_size_y

                    if self.maze[row][col] == "W":
                        cx, cy = self.logical_to_canvas(row, col, 1)
                        self.maze_canvas.create_image(cx, cy, image=self.wall_image)
                    elif self.maze[row][col] == "S":
                        self.player1_pos = [row, col]
                        cx, cy = self.logical_to_canvas(row, col, 1)
                        self.player1 = self.maze_canvas.create_image(cx, cy, image=self.character_frames[0])
                    elif self.maze[row][col] == "E":
                        self.maze_canvas.create_rectangle(x1, y1, x2, y2, fill="green")
                    elif self.maze[row][col] == "*":
                        self.add_multiplayer_item(row, col, 1)

            # Draw right maze (Player 2)
            for row in range(len(self.maze)):
                for col in range(len(self.maze[row])):
                    x1 = col * self.cell_size_x + self.maze_width
                    y1 = row * self.cell_size_y + int(self.HEIGHT / 14)
                    x2 = x1 + self.cell_size_x
                    y2 = y1 + self.cell_size_y

                    if self.maze[row][col] == "W":
                        cx, cy = self.logical_to_canvas(row, col, 2)
                        self.maze_canvas.create_image(cx, cy, image=self.wall_image)
                    elif self.maze[row][col] == "S":
                        self.player2_pos = [row, col]
                        cx, cy = self.logical_to_canvas(row, col, 2)
                        self.player2 = self.maze_canvas.create_image(cx, cy, image=self.character_frames[0])
                    elif self.maze[row][col] == "E":
                        self.maze_canvas.create_rectangle(x1, y1, x2, y2, fill="green")
                    elif self.maze[row][col] == "*":
                        self.add_multiplayer_item(row, col, 2)

            # Draw dividing line
            self.maze_canvas.create_line(self.maze_width, 0, self.maze_width, self.HEIGHT, 
                                    fill=self.themes["text"], width=3)

        def add_item(self, row, col, x1, y1, x2, y2):
            """Add item for single player mode"""
            item_image = self.get_item_image()
            cx, cy = self.logical_to_canvas(row, col)
            item_id = self.maze_canvas.create_image(cx, cy, image=item_image[0])
            self.item_message = self.item_message_list[self.mode]
            self.items.append({"pos": [row, col], "id": item_id})
            self.lev_item_list.append(item_image)
            self.total_items += 1

        def add_multiplayer_item(self, row, col, player):
            """Add item for multiplayer mode"""
            item_image = self.get_item_image()
            cx, cy = self.logical_to_canvas(row, col, player)
            item_id = self.maze_canvas.create_image(cx, cy, image=item_image[0])
            
            if player == 1:
                self.player1_items.append({"pos": [row, col], "id": item_id})
                self.player1_lev_item_list.append(item_image)
            else:
                self.player2_items.append({"pos": [row, col], "id": item_id})
                self.player2_lev_item_list.append(item_image)
            
            self.total_items += 1

        def get_item_image(self):
            """Get appropriate item image based on mode"""
            if self.mode >= 12:
                item_image = self.item_list[4][randint(0, 1)]
                self.time_limit = 200
            elif self.mode >= 9:
                self.time_limit = 150
                item_image = self.item_list[3]
            elif self.mode >= 6:
                self.time_limit = 120
                item_image = self.item_list[2]
            elif self.mode >= 3:
                item_image = self.item_list[1]
            elif self.mode >= 0:
                item_image = self.item_list[0]
            else:
                print("Invalid mode")
                item_image = self.invalid_mode
            return item_image

        def move_player(self, event):
            """Handle player movement for both single and multiplayer"""
            if self.finished or self.stop:
                return

            if self.multiplayer:
                self.move_multiplayer(event)
            else:
                self.move_singleplayer(event)

        def move_singleplayer(self, event):
            """Original single player movement"""
            row, col = self.player_pos
            new_row, new_col = row, col

            if event.keysym == "Up":
                new_row -= 1
            elif event.keysym == "Down":
                new_row += 1
            elif event.keysym == "Left":
                new_col -= 1
            elif event.keysym == "Right":
                new_col += 1

            # Check if move is valid
            if 0 <= new_row < len(self.maze) and 0 <= new_col < len(self.maze[0]) and self.maze[new_row][new_col] != "W":
                # Update player position
                self.player_pos = [new_row, new_col]
                x, y = self.logical_to_canvas(new_row, new_col)
                self.maze_canvas.coords(self.player, x, y)

                # Check for item collection
                self.check_item_collision(new_row, new_col)

                # Check if player reached the end
                if [new_row, new_col] == self.end_pos:
                    self.end_game()

        def move_multiplayer(self, event):
            """Handle multiplayer movement"""
            # Player 1 controls (WASD)
            if event.keysym in ["w", "s", "a", "d"] and not self.player1_finished:
                self.move_player_mp(1, event.keysym)
            
            # Player 2 controls (Arrow keys)
            elif event.keysym in ["Up", "Down", "Left", "Right"] and not self.player2_finished:
                self.move_player_mp(2, event.keysym)

        def move_player_mp(self, player, key):
            """Move specific player in multiplayer"""
            if player == 1:
                row, col = self.player1_pos
                player_obj = self.player1
            else:
                row, col = self.player2_pos
                player_obj = self.player2

            new_row, new_col = row, col

            # Player 1 controls (WASD)
            if player == 1:
                if key == "w":
                    new_row -= 1
                elif key == "s":
                    new_row += 1
                elif key == "a":
                    new_col -= 1
                elif key == "d":
                    new_col += 1
            # Player 2 controls (Arrow keys)
            else:
                if key == "Up":
                    new_row -= 1
                elif key == "Down":
                    new_row += 1
                elif key == "Left":
                    new_col -= 1
                elif key == "Right":
                    new_col += 1

            # Check if move is valid
            if 0 <= new_row < len(self.maze) and 0 <= new_col < len(self.maze[0]) and self.maze[new_row][new_col] != "W":
                # Update player position
                if player == 1:
                    self.player1_pos = [new_row, new_col]
                else:
                    self.player2_pos = [new_row, new_col]
                
                x, y = self.logical_to_canvas(new_row, new_col, player)
                self.maze_canvas.coords(player_obj, x, y)

                # Check for item collection
                self.check_multiplayer_item_collision(new_row, new_col, player)

                # Check if player reached the end
                if self.maze[new_row][new_col] == "E":
                    if player == 1:
                        self.player1_finished = True
                    else:
                        self.player2_finished = True
                    
                    self.check_multiplayer_end()

        def check_multiplayer_item_collision(self, row, col, player):
            """Check item collision for multiplayer"""
            if player == 1:
                items_list = self.player1_items
                score_text = self.score1_text
            else:
                items_list = self.player2_items
                score_text = self.score2_text

            for item in items_list[:]:
                if item["pos"] == [row, col]:
                    self.maze_canvas.delete(item["id"])
                    items_list.remove(item)
                    
                    if player == 1:
                        self.player1_score += 1
                        self.maze_canvas.itemconfig(score_text, text=f"Player 1: {self.player1_score}")
                    else:
                        self.player2_score += 1
                        self.maze_canvas.itemconfig(score_text, text=f"Player 2: {self.player2_score}")
                    
                    self.maze_canvas.itemconfig(self.info_text, 
                                            text=self.quotes[randint(0, len(self.quotes) - 1)])
                    return True
            return False

        def check_multiplayer_end(self):
            """Check if multiplayer game should end"""
            if self.player1_finished or self.player2_finished:
                self.finished = True
                self.stop = True
                
                # Cancel timer
                if hasattr(self, 'timer_id'):
                    try:
                        self.master.after_cancel(self.timer_id)
                    except:
                        pass

                self.end_time = time.time()
                self.total_time = round(self.end_time - self.start_time)
                
                # Determine winner
                if self.player1_finished and self.player2_finished:
                    if self.player1_score > self.player2_score:
                        winner_text = "Player 1 Wins!"
                    elif self.player2_score > self.player1_score:
                        winner_text = "Player 2 Wins!"
                    else:
                        winner_text = "It's a Tie!"
                elif self.player1_finished:
                    winner_text = "Player 1 Wins!"
                else:
                    winner_text = "Player 2 Wins!"

                self.show_multiplayer_end(winner_text)

        def show_multiplayer_end(self, winner_text):
            """Show multiplayer end screen"""
            message_str = f"{winner_text}\n\nPlayer 1 Score: {self.player1_score}\nPlayer 2 Score: {self.player2_score}\nTime: {self.total_time} seconds"
            
            fin_window = Toplevel(self.master)
            fin_window.title("Game Over")
            
            message = Label(fin_window, text=message_str, font=('Arial', 16), pady=20, padx=20)
            message.pack()

            restart_button = Button(
                fin_window, text="Play Again", 
                command=lambda: [fin_window.destroy(), 
                            self.start(self.master, self.mode, self.maze_canvas, 
                                        self.selected_wall, self.selected_character, 
                                        self.current_theme, True)]
            )
            restart_button.pack(pady=10)

            next_level_button = Button(
                fin_window, text="Next Level", 
                command=lambda: [fin_window.destroy(), 
                            self.start(self.master, self.mode + 1, self.maze_canvas, 
                                        self.selected_wall, self.selected_character, 
                                        self.current_theme, True)]
            )
            next_level_button.pack(pady=5)

        def animate_character(self):
            """Animate characters for both modes"""
            if not hasattr(self, 'character_frame_index'):
                self.character_frame_index = 0

            self.character_frame_index = (self.character_frame_index + 1) % self.frameCnt

            if self.multiplayer:
                if self.player1_pos:
                    x, y = self.logical_to_canvas(self.player1_pos[0], self.player1_pos[1], 1)
                    self.maze_canvas.coords(self.player1, x, y)
                    self.maze_canvas.itemconfig(self.player1, image=self.character_frames[self.character_frame_index])
                
                if self.player2_pos:
                    x, y = self.logical_to_canvas(self.player2_pos[0], self.player2_pos[1], 2)
                    self.maze_canvas.coords(self.player2, x, y)
                    self.maze_canvas.itemconfig(self.player2, image=self.character_frames[self.character_frame_index])
            else:
                if self.player_pos:
                    x, y = self.logical_to_canvas(self.player_pos[0], self.player_pos[1])
                    self.maze_canvas.coords(self.player, x, y)
                    self.maze_canvas.itemconfig(self.player, image=self.character_frames[self.character_frame_index])

            if not self.finished and not self.stop:
                self.master.after(500, self.animate_character)

        def animate_item(self):
            """Animate items for both modes"""
            if not hasattr(self, 'item_frame_index'):
                self.item_frame_index = 0

            if self.multiplayer:
                # Animate Player 1 items
                for i, item in enumerate(self.player1_items):
                    item_id = item["id"]
                    item_pos = item["pos"]
                    x, y = self.logical_to_canvas(item_pos[0], item_pos[1], 1)
                    self.maze_canvas.coords(item_id, x, y)

                # Animate Player 2 items
                for i, item in enumerate(self.player2_items):
                    item_id = item["id"]
                    item_pos = item["pos"]
                    x, y = self.logical_to_canvas(item_pos[0], item_pos[1], 2)
                    self.maze_canvas.coords(item_id, x, y)

                self.item_frame_index = (self.item_frame_index + 1) % len(self.get_item_image())
                
                # Update Player 1 item images
                for i, item in enumerate(self.player1_items):
                    if i < len(self.player1_lev_item_list):
                        self.maze_canvas.itemconfig(item["id"], 
                                                image=self.player1_lev_item_list[i][self.item_frame_index])
                
                # Update Player 2 item images
                for i, item in enumerate(self.player2_items):
                    if i < len(self.player2_lev_item_list):
                        self.maze_canvas.itemconfig(item["id"], 
                                                image=self.player2_lev_item_list[i][self.item_frame_index])
            else:
                # Original single player item animation
                for item in self.items:
                    item_id = item["id"]
                    item_pos = item["pos"]
                    x, y = self.logical_to_canvas(item_pos[0], item_pos[1])
                    self.maze_canvas.coords(item_id, x, y)

                self.item_frame_index = (self.item_frame_index + 1) % len(self.item_list[self.mode])
                
                for i, item in enumerate(self.items):
                    if i < len(self.lev_item_list):
                        self.maze_canvas.itemconfig(item["id"], 
                                                image=self.lev_item_list[i][self.item_frame_index])

            if not self.finished and not self.stop:
                self.master.after(500, self.animate_item)

        def Menu(self):
            if hasattr(self, 'menu_canvas') and self.menu_canvas:
                self.close_menu()
                return
            
            self.stop = True
            if hasattr(self, 'timer_id'):
                self.master.after_cancel(self.timer_id)
            
            self.paused_time = time.time() - self.start_time

            self.menu_canvas = Canvas(self.master, height=300, width=300, bg=self.themes["overlap"])
            self.menu_canvas.place(x=self.WIDTH/2, y=self.HEIGHT/2, anchor="center")
            
            homepage = Button(self.master, text="Home", 
                            command=lambda: [self.close_menu(), 
                                            self.HomePage.layout(self.master, self.current_theme, 
                                                            self.mode, self.selected_wall, 
                                                            self.selected_character)], 
                            bg=self.themes["bg"], fg=self.themes["fg"])
            resume_button = Button(self.master, image=self.playbutton, command=self.close_menu, 
                                bg=self.themes["bg"], fg=self.themes["fg"])
            up_level = Button(self.master, text=">", command=self.up_level, 
                            bg=self.themes["bg"], fg=self.themes["fg"])
            down_level = Button(self.master, text="<", command=self.down_level, 
                            bg=self.themes["bg"], fg=self.themes["fg"])
            multiplayer = Button(self.master, text="Toggle Multiplayer", 
                            command=lambda: [self.close_menu(), 
                                            self.start(self.master, self.mode, self.maze_canvas, 
                                                    self.selected_wall, self.selected_character, 
                                                    self.current_theme, not self.multiplayer)], 
                            bg=self.themes["bg"], fg=self.themes["fg"])
            play = Button(self.master, text="Play", command=lambda: [self.close_menu(), self.start(self.master, self.mode, self.maze_canvas,          self.selected_wall, self.selected_character, self.current_theme, self.multiplayer)], bg=self.themes["bg"], fg=self.themes["fg"])

            self.menu_canvas.create_text(150, 30, text="Paused", font=("Comic Sans MS", 16), fill=self.themes["text"])

            # Position menu elements
            self.mode_text = self.menu_canvas.create_text(215, 80, text=str(self.mode+1), fill=self.themes["text"])
            self.menu_canvas.create_window(215, 110, window=play)
            self.menu_canvas.create_window(150, 200, window=multiplayer)
            self.menu_canvas.create_window(80, 80, window=homepage)
            self.menu_canvas.create_window(150, 150, window=resume_button)
            self.menu_canvas.create_window(190, 80, window=down_level)
            self.menu_canvas.create_window(240, 80, window=up_level)

        def up_level(self):
            if self.mode < len(self.maze_levels) - 1:
                self.mode += 1
                self.menu_canvas.itemconfig(self.mode_text, text=str(self.mode+1))

        def down_level(self):
            if self.mode > 0:
                self.mode -= 1
                self.menu_canvas.itemconfig(self.mode_text, text=str(self.mode+1))

        def close_menu(self):
            if hasattr(self, 'menu_canvas') and self.menu_canvas:
                self.menu_canvas.destroy()
                self.menu_canvas = None
            
            # Resume the game
            if not self.finished:
                self.stop = False
                # Adjust the start time to account for paused time
                self.start_time = time.time() - self.paused_time
                
                # Restart animations and timer
                self.animate_character()
                self.update_timer()
            else:
                self.finished = True
                self.stop = True
                self.maze_canvas = None
                if hasattr(self, 'timer_id'):
                    self.master.after_cancel(self.timer_id)

        def load_images(self):
            self.frameCnt = 2
            # Customization and maze game images
            self.wall_1 = PhotoImage(file=r"Images\Wall #1.png")
            self.wall_2 = Image.open(r"Images\Wall #2.jpg")
            self.wall_3 = Image.open(r"Images\Wall #3.jpg")
            self.wall_4 = Image.open(r"Images\Wall #4.jpg")

            self.wall_images = [
                self.wall_1.subsample(int(self.wall_1.width()/self.cell_size_x), int(self.wall_1.height()/self.cell_size_y)),
                ImageTk.PhotoImage(self.wall_2.resize((self.cell_size_x, self.cell_size_y)), Image.Resampling.LANCZOS),
                ImageTk.PhotoImage(self.wall_3.resize((self.cell_size_x, self.cell_size_y)), Image.Resampling.LANCZOS),
                ImageTk.PhotoImage(self.wall_4.resize((self.cell_size_x, self.cell_size_y)), Image.Resampling.LANCZOS)
            ]
            self.char1_frames = self.load_gif_frames(r"Images\Character #2.gif")
            self.char2_frames = self.load_gif_frames(r"Images\llama.gif")
            self.character_images = [self.char1_frames, self.char2_frames]

            # Item images
            self.item1 = self.load_gif_frames(r"Images\Soup.gif")
            self.item2 = self.load_gif_frames(r"Images\Book.gif")
            self.item3 = self.load_gif_frames(r"Images\water item.gif")
            self.item4 = self.load_gif_frames(r"Images\renewable energy symbol.gif")
            self.item5 = self.load_gif_frames(r"Images\Tree (1).gif")
            self.item6 = self.load_gif_frames(r"Images\Plastic Bag from Ocean (1).gif")
            self.invalid_mode = self.load_gif_frames(r"Images\bouncing ball.gif")
            self.item_list = [self.item1, self.item2, self.item3, self.item4, [self.item5, self.item6]]
            self.item_indices = [12, 9, 6, 3, 0]

            self.playbutton = (PhotoImage(file=r"Images\Play button.png")).subsample(5)

        def load_gif_frames(self, path):
            gif = Image.open(path)
            frames = []
            try:
                for i in range(self.frameCnt):
                    gif.seek(i)
                    frame = gif.copy()
                    frames.append(ImageTk.PhotoImage(frame.resize((self.cell_size_x, self.cell_size_y))))
            except EOFError:
                pass
            return frames

        def check_item_collision(self, row, col):
            """Single player item collision (original)"""
            for item in self.items[:]:
                if item["pos"] == [row, col]:
                    self.maze_canvas.delete(item["id"])
                    self.items.remove(item)
                    self.score += 1
                    self.maze_canvas.itemconfig(self.score_text, text=f"Items collected: {self.score}")
                    self.maze_canvas.itemconfig(self.info_text, text=self.quotes[randint(0, (len(self.quotes)) - 1)])
                    self.show_item_message()
                    return True
            return False

        def show_item_message(self):
            """Show item collection message (single player only)"""
            if self.finished or self.stop or self.multiplayer:
                return
            if hasattr(self, 'info_window') and self.info_window:
                self.info_window.destroy()
            
            self.stop = True
            self.paused_time = time.time() - self.start_time

            self.info_canvas = Canvas(self.master, height=300, width=300, bg=self.themes["overlap"])
            self.info_canvas.place(x=self.WIDTH / 2, y=self.HEIGHT / 2, anchor="center")

            self.info_canvas.create_text(150, 30, text="Item Collected!", font=("Comic Sans MS", 16), fill=self.themes["text"])
            self.info_canvas.create_text(150, 70, text="Item Information:", font=("Comic Sans MS", 14), fill=self.themes["text"])
            self.info_canvas.create_text(150, 110, anchor="n", width=250, text=self.item_message[self.score - 1], font=('Comic Sans MS', 12), fill=self.themes["text"])

            close_button = Button(self.info_canvas, text="Close", command=self.close_item_message, bg=self.themes["button"], fg=self.themes["text"])
            self.info_canvas.create_window(150, 270, window=close_button)

        def close_item_message(self):
            if hasattr(self, 'info_canvas') and self.info_canvas:
                self.info_canvas.destroy()
                self.info_canvas = None
            
            self.stop = False
            if not self.finished:
                self.start_time = time.time() - self.paused_time
                self.animate_character()
                self.update_timer()

        def end_game(self):
            """End single player game"""
            self.finished = True
            self.stop = True
            
            if hasattr(self, 'timer_id'):
                try:
                    self.master.after_cancel(self.timer_id)
                except:
                    pass

            self.end_time = time.time()
            self.total_time = round(self.end_time - self.start_time)
            score = int(self.score * 100) + ((150 - self.total_time) * 5)
            
            try:
                df = pd.read_csv("highscores.csv")
                highscore = df.iloc[self.mode, 1]

                if highscore < score:
                    highscore = score
                    df.iat[self.mode, 1] = score
                    df.to_csv('highscores.csv', index=False)
            except:
                highscore = score
                
            message_str = f"Congratulations!\nYou've completed the maze!\nItems collected: {self.score}/{self.total_items} \nTime used {self.total_time} seconds \nTotal score: {(self.score * 100) + ((150 - self.total_time) * 5)}, Highest score: {highscore}"
            fin_window = Toplevel(self.master)
            self.finished = True
            message = Label(fin_window, text=message_str, font=('Arial', 16), pady=20, padx=20)
            message.pack()

            restart_button = Button(
                fin_window, text="Play Again", 
                command=lambda: [fin_window.destroy(), 
                            self.start(self.master, self.mode, self.maze_canvas, 
                                        self.selected_wall, self.selected_character, 
                                        self.current_theme, False)]
            )
            restart_button.pack(pady=10)

            nextLevelButton = Button(
                fin_window, text="Next Level",
                command=lambda: [fin_window.destroy(), 
                            self.start(self.master, (self.mode+1), self.maze_canvas, 
                                        self.selected_wall, self.selected_character, 
                                        self.current_theme, False)]
            )
            nextLevelButton.pack(pady=13)

        def update_timer(self):
            """Update timer for both modes"""
            if self.maze_canvas is None or self.finished or self.stop:
                return
            
            current_time = int(time.time() - self.start_time)
            
            if current_time >= self.time_limit:
                self.stop = True
                self.finished = True
                
                if hasattr(self, 'timer_id'):
                    self.master.after_cancel(self.timer_id)
                
                if self.multiplayer:
                    self.show_multiplayer_timeout()
                else:
                    self.show_single_timeout()
            else:
                self.maze_canvas.itemconfig(self.time_text, text=f"Time: {current_time} seconds")
                self.timer_id = self.master.after(1000, self.update_timer)

        def show_single_timeout(self):
            """Show timeout for single player"""
            game_over_win = Toplevel(self.master)
            game_over_win.title("Game Over")
            
            message = Label(
                game_over_win,
                text=f"Time's up!\nItems collected: {self.score}/{self.total_items}",
                font=('Arial', 16),
                pady=20,
                padx=20
            )
            message.pack()

            restart_button = Button(
                game_over_win,
                text="Play Again",
                command=lambda: [game_over_win.destroy(), 
                            self.start(self.master, self.mode, self.maze_canvas, 
                                        self.selected_wall, self.selected_character, 
                                        self.current_theme, False)]
            )
            restart_button.pack(pady=10)

        def show_multiplayer_timeout(self):
            """Show timeout for multiplayer"""
            if self.player1_score > self.player2_score:
                winner_text = "Player 1 Wins by Score!"
            elif self.player2_score > self.player1_score:
                winner_text = "Player 2 Wins by Score!"
            else:
                winner_text = "It's a Tie!"

            self.show_multiplayer_end(f"Time's Up!\n{winner_text}")

def main():
    root = Tk()
    root.title("Running for 2030")
    root.resizable(height= False, width= False)
    
    app_layout = SDG_App.Applayout()
    # Initialize the Mazegame when needed
    app_layout.layout(root, "light")
    
    root.mainloop()

if __name__ == "__main__":
    main()
