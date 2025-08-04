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
            # previw config
            self.frameCnt = 2
            self.ind = 0
            self.themes = {
                "light": {
                    "bg": "#929090",
                    "canvas": "#E8E8E8",
                    "overlap": "#cacaca",
                    "text": "black",
                    "button": "#BFD6E3",
                    "fg": "black"  # Added for consistency
                },
                "dark": {
                    "bg": "#2C2C2C",
                    "canvas": "#1E1E1E",
                    "overlap": "#3C3C3C",
                    "text": "white",
                    "button": "#777272",
                    "fg": "white"  # Added for consistency
                }
            }

            #canvases setup
            self.layout_canvas = None
            self.settings_canvas = None
            self.master = None
            self.cur_music = False
            self.cur_volume = False
            self.maze_canvas = None
            # Remove the recursive initialization
            self.Mazegame = None  # We'll initialize it when needed
            self.init_mazegame()
        # Add a method to initialize Mazegame
        def init_mazegame(self):
            if self.Mazegame is None:
                self.Mazegame = SDG_App.Mazegame()
                self.multi_or_normal = True

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
            play_button = Button(master, text="Play", height=3, width=11, command=lambda: self.Mazegame.start(self.master, self.mode, self.layout_canvas, self.current_wall_index, self.current_character_index, self.current_theme), font=("Comic Sans MS", 12), bg=theme["button"], fg=theme["text"])
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

            back_button = Button(self.lev_sel_canvas, text="Back", command=lambda: self.show_main_layout(self.lev_sel_canvas),bg=theme["button"], fg=theme["text"])
            self.lev_sel_canvas.create_window(200, 260, window=back_button)
            self.level_text = self.lev_sel_canvas.create_text(200, 55, text= f"Level or mode: {self.mode+1}", font=("Comic Sans MS", 14), fill=theme["text"])

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
            multiplayer_btn = Button(self.lev_sel_canvas, text="Multiplayer", command= self.change_mazegame_multiplayer, bg=theme["button"], fg=theme["text"])

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

        def change_mazegame_multiplayer(self):
            if self.multi_or_normal == True:
                self.Mazegame = SDG_App.MultiplayerMazeGame
                self.multi_or_normal = False
                self.lev_sel_canvas.itemconfig(self.level_text, text= "Level or mode: Multiplayer")
            elif self.Mazegame == SDG_App.MultiplayerMazeGame:
                self.Mazegame = SDG_App.Mazegame
                self.lev_sel_canvas.itemconfig(self.level_text, text= "Level or mode: Soloplayer")

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
            self.lev_sel_canvas.itemconfig(self.level_text, text= f"Level or mode: {self.mode+1}")
            return self.mode

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
                    "fg": "black"  # Added for consistency
                },
                "dark": {
                    "bg": "#2C2C2C",
                    "canvas": "#1E1E1E",
                    "overlap": "#3C3C3C",
                    "text": "white",
                    "button": "#777272",
                    "fg": "white"  # Added for consistency
                }
            }

        def init_homepage(self):
            if self.HomePage is None:
                self.HomePage = SDG_App.Applayout()

        def start(self, master, mode, canvas, current_wall_i, current_char_i, theme):
            # Theme setup
            self.current_theme = theme
            self.mode = mode
            self.themes = self.themes_1[self.current_theme]
            
            # Game setup
            self.maze_levels = LEVELS
            self.maze = self.maze_levels[self.mode]
            self.stop = False
            self.finished = False
            
            # Canvas calculations
            self.HEIGHT = 600
            self.WIDTH = 700
            self.cell_size_y = round((self.HEIGHT - (self.HEIGHT / 5)) / len(self.maze))
            self.cell_size_x = round(self.WIDTH / len(self.maze[0]))

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
            self.master.title("Maze game")
            
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
            
            # Score and UI elements
            self.score = 0
            self.score_text = self.maze_canvas.create_text(int(self.WIDTH /5), int(self.HEIGHT / 28), text=f"Items collected: {self.score}", font=('Comic Sans MS', 16), fill=self.themes["text"])
            self.time_text = self.maze_canvas.create_text(int(self.WIDTH /1.75), int(self.HEIGHT / 28), text="0", font=('Comic Sans MS', 16), fill=self.themes["text"])

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
            self.item_message_list = [
                ["🌾 Sustainable Development Goal 2 (SDG 2) aims to end hunger, achieve food security, improve nutrition, and promote sustainable agriculture by 2030.", "👶 It focuses especially on vulnerable groups like children, pregnant women, and the poor, ensuring they have access to safe and nutritious food all year round.", "🌍 SDG 2 also targets the elimination of all forms of malnutrition, including stunting, wasting, and obesity, which affect millions globally.", "🚜 A key part of the goal is to boost the productivity and income of small-scale food producers through equal access to land, resources, and markets.", "🌱 By encouraging resilient agricultural practices and protecting genetic diversity in crops and livestock, SDG 2 supports long-term sustainability in food systems."],
                ["🌐 SDG 2 is one of the 17 goals established by the United Nations in 2015 to create a better and more sustainable future for all.", "📉 Despite decades of progress, hunger has been rising again since 2015 due to conflict, climate change, and economic instability.","👩‍🌾 The goal emphasizes empowering women, indigenous peoples, and small-scale farmers to improve agricultural productivity and income.","🌾 SDG 2 includes eight specific targets and 14 indicators to measure progress toward ending hunger and promoting sustainable agriculture.","🧬 One target focuses on preserving genetic diversity in seeds, plants, and animals to ensure resilient food systems."],
                ["📊 SDG 2 calls for better access to market information and stable food commodity markets to reduce price volatility.","🚫 It also aims to eliminate agricultural export subsidies and trade distortions that harm global food security.","🌍 SDG 2 is deeply interconnected with other goals—progress in health, education, and climate action directly affects food security.","📣 Everyone can contribute by reducing food waste, supporting local farmers, and making sustainable food choices.","💡 Investment in agricultural research, rural infrastructure, and technology is vital to achieving SDG 2, especially in developing countries."],
                ["SDG 4 promotes inclusive, quality education and lifelong learning for everyone", "📚 SDG 4 aims to ensure inclusive and equitable quality education for all and promote lifelong learning opportunities.","✊ It recognises that education is a fundamental human right and essential for breaking cycles of poverty.","👶 The goal includes improving access to early childhood education, especially for disadvantaged children.","🎓 SDG 4 strives for universal primary and secondary education, free and available to everyone by 2030.","🏫 It also promotes equal access to affordable and quality higher education, including university and vocational training."],
                ["Governments are investing in teacher training programs to enhance the quality of education and ensure students receive effective instruction.","Inclusive school infrastructure is being developed to provide safe, accessible, and supportive learning environments for all children.","Policies are being implemented to guarantee free and equitable access to primary and secondary education, especially in underserved communities.","Technology is being integrated into classrooms to bridge the digital divide and offer innovative learning opportunities for students worldwide.","Initiatives are focused on reducing dropout rates by supporting girls, children with disabilities, and other marginalized groups through targeted interventions.","Adult education and vocational training programs are expanding to promote lifelong learning and improve employment prospects for all age groups."],
                ["International partnerships are being strengthened to share best practices, resources, and funding aimed at improving global education systems.","Curriculum reforms are underway to incorporate critical thinking, sustainability, and digital literacy into national education standards.","Monitoring and evaluation frameworks are being developed to track progress toward education goals and ensure accountability at all levels.","Scholarship programs are being expanded to support students from low-income families in accessing higher education opportunities.","Community engagement initiatives are promoting parental involvement and local support for schools to enhance student outcomes.","Efforts are being made to eliminate gender disparities in education by addressing cultural barriers and promoting equal opportunities for girls and boys."],
                ["Governments and NGOs are investing in infrastructure to provide safe drinking water and sanitation facilities in rural and urban communities.","Water treatment technologies are being deployed to reduce contamination and ensure access to clean water for households and schools.","Public awareness campaigns are educating communities about hygiene practices, such as handwashing, to prevent disease and improve health outcomes.","Integrated water resource management strategies are being implemented to protect freshwater ecosystems and ensure sustainable water use.","Efforts are underway to build climate-resilient water systems that can withstand droughts, floods, and other environmental challenges.","International cooperation is supporting low-income countries in developing water and sanitation services through funding, training, and technical assistance.","Educational programs in schools are teaching children the importance of water conservation and hygiene from an early age."],
                ["Local communities are being empowered to manage and maintain their own water and sanitation systems through training and capacity-building programs.","Rainwater harvesting initiatives are helping households and schools collect and store water sustainably, especially in water-scarce regions.","Innovative financing models are being developed to make water and sanitation services affordable and accessible for marginalized populations.","Monitoring and data collection systems are being strengthened to track water quality, usage, and infrastructure performance in real time.","Sanitation solutions like eco-toilets and decentralized waste treatment are being introduced to reduce pollution and improve public health.","Youth-led organizations are advocating for water justice and engaging in projects that promote clean water access in underserved areas.","Partnerships between governments, private sector, and civil society are accelerating innovation in water purification and sanitation technologies."],
                ["Mobile apps and digital platforms are being used to report water service issues and improve accountability in water management.","Desalination projects are expanding access to freshwater in coastal and arid regions where natural sources are limited.","Community-led clean-up campaigns are restoring polluted rivers, lakes, and wetlands to improve local water quality.","Policies are being enacted to regulate industrial discharge and protect water sources from chemical contamination.","Water-saving technologies like low-flow fixtures and smart irrigation systems are being promoted to reduce waste.","Emergency response teams are providing clean water and sanitation supplies during natural disasters and humanitarian crises.","Research institutions are studying the links between water access, gender equality, and economic development to inform policy."],
                ["Solar panel installations are expanding in both urban and rural areas to harness clean energy from the sun.","Wind farms are being developed onshore and offshore to generate electricity with minimal environmental impact.","Battery storage systems are improving energy reliability by storing excess renewable power for later use.","Smart grids are being deployed to optimize energy distribution and integrate renewables efficiently.","Hydropower plants are being modernized to increase efficiency and reduce ecological disruption.","Geothermal energy is being tapped in volcanic regions to provide consistent, low-emission power.","Bioenergy projects are converting agricultural and organic waste into usable fuel and electricity.","Electric vehicle charging networks are expanding to support the transition to clean transportation."],
                ["Governments are offering subsidies and tax incentives to promote investment in renewable energy.","International climate agreements are encouraging countries to set clean energy targets and share technologies.","Carbon pricing mechanisms are being introduced to make fossil fuels less economically attractive.","Green bonds are financing large-scale renewable energy infrastructure projects around the world.","Public-private partnerships are accelerating the deployment of clean energy in developing regions.","Energy access programs are targeting off-grid communities with affordable solar and wind solutions.","Regulatory reforms are streamlining permits and approvals for renewable energy installations.","Development banks are supporting clean energy transitions through low-interest loans and grants."],
                ["Schools are incorporating renewable energy topics into science and environmental curricula.","Local cooperatives are managing community-owned solar and wind projects to generate shared benefits.","Training programs are equipping workers with skills for jobs in the renewable energy sector.","Awareness campaigns are educating the public about the benefits of switching to clean energy.","Youth organizations are leading advocacy efforts for sustainable energy policies and practices.","Rural electrification initiatives are improving livelihoods by powering homes, clinics, and businesses.","Workshops and webinars are helping entrepreneurs develop renewable energy startups.","Cultural leaders are promoting sustainable energy practices through storytelling and local traditions."],
                ["Marine protected areas are being expanded to safeguard biodiversity and restore fish populations.","Coral reef restoration projects are using techniques like coral gardening and artificial reefs.","Mangrove forests are being replanted to protect coastlines and support aquatic ecosystems.","Reforestation campaigns are restoring degraded land and improving carbon sequestration.","Wetland conservation efforts are preserving habitats for birds, amphibians, and aquatic life.","Sustainable forestry practices are reducing deforestation and promoting ecosystem health.","Invasive species are being removed to protect native flora and fauna in both land and marine environments.","Grassland restoration is improving soil health and supporting pollinators and grazing species.","Plastic clean-up initiatives are reducing ocean pollution and protecting marine animals."],
                ["Fishing quotas and bans on destructive practices are helping rebuild marine populations.","Environmental laws are being strengthened to protect endangered species and critical habitats.","Satellite monitoring is tracking deforestation, illegal fishing, and ecosystem changes in real time.","Eco-certification programs are promoting sustainable seafood and timber products.","Climate adaptation strategies are integrating biodiversity protection into national planning.","Funding for nature-based solutions is supporting projects that benefit both people and ecosystems.","Technology is being used to map biodiversity hotspots and guide conservation priorities.","Pollution control regulations are reducing runoff and waste that harm land and sea life.","International treaties are fostering cooperation on ocean governance and forest preservation."],
                ["Local communities are leading conservation efforts through traditional ecological knowledge.","Schools are teaching students about marine and terrestrial ecosystems and their importance.","Citizen science programs are engaging volunteers in monitoring wildlife and environmental health.","Eco-tourism is providing income while promoting awareness and protection of natural areas.","Youth groups are organizing beach clean-ups and tree planting events to support biodiversity.","Public campaigns are raising awareness about the impact of plastic and deforestation.","Indigenous leaders are advocating for land and water rights to protect sacred ecosystems.","Art and storytelling are being used to inspire action for ocean and forest conservation.","Community gardens and green spaces are reconnecting people with nature and promoting stewardship."]
            ]

            self.info_text = self.maze_canvas.create_text(int(self.WIDTH / 2), int(self.HEIGHT * 0.94), width=400, text="Movement with the arrow keys. Collect all the items to get the highest score.", font=('Comic Sans MS', 10), fill=self.themes["text"])
            self.lev_item_list = []

            # Menu button with theme colors
            menu = Button(self.master, text="⏸", command=self.Menu, bg=self.themes["button"], fg=self.themes["text"])
            self.maze_canvas.create_window(int(self.WIDTH * 0.95), int(self.HEIGHT / 28), window=menu)
            
            # Game state
            self.finished = False
            self.stop = False
            self.player_pos = None
            self.end_pos = None
            self.items = []  # Will store coordinates of collectible items
            self.total_items = 0
            
            # Bind keys and initialize game
            self.master.bind("<KeyPress>", self.move_player)
            self.draw_maze()
            self.update_timer()
            self.animate_character()
            self.animate_item()
            self.init_homepage()

        def Menu(self):
            if hasattr(self, 'menu_canvas') and self.menu_canvas:  # If menu is already open
                self.close_menu()
                return
            
            self.stop = True  # Pause the game

            if hasattr(self, 'timer_id'):
                self.master.after_cancel(self.timer_id)
            
            # Store current game state
            self.paused_time = time.time() - self.start_time

            # Create menu canvas with theme
            self.menu_canvas = Canvas(self.master, height=300, width=300, bg=self.themes["overlap"])
            self.menu_canvas.place(x=self.WIDTH/2, y=self.HEIGHT/2, anchor="center")
            
            # Menu buttons with theme colors
            homepage = Button(self.master, text="Home", command=lambda: [self.close_menu(), self.HomePage.layout(self.master, self.current_theme, self.mode, self.selected_wall, self.selected_character)], bg=self.themes["bg"], fg=self.themes["fg"])
            resume_button = Button(self.master, image=self.playbutton, command=self.close_menu, bg=self.themes["bg"], fg=self.themes["fg"])
            up_level = Button(self.master, text=">", command=self.up_level, bg=self.themes["bg"], fg=self.themes["fg"])
            down_level = Button(self.master, text="<", command=self.down_level, bg=self.themes["bg"], fg=self.themes["fg"])
            multiplayer = Button(self.master, text="Multiplayer", command=None, bg=self.themes["bg"], fg=self.themes["fg"])
            random_maze = Button(self.master, text="Random generation Mode", command=None, bg=self.themes["bg"], fg=self.themes["fg"])
            play = Button(self.master, text="Play", command=lambda: [self.close_menu(), self.start(self.master, self.mode, self.maze_canvas, self.selected_wall, self.selected_character, self.current_theme)], bg=self.themes["bg"], fg=self.themes["fg"])

            self.menu_canvas.create_text(150, 30, text="Paused", font=("Comic Sans MS", 16), fill=self.themes["text"])

            # Position menu elements
            self.mode_text = self.menu_canvas.create_text(215, 80, text=str(self.mode+1), fill=self.themes["text"])
            self.menu_canvas.create_window(215, 110, window=play)
            self.menu_canvas.create_window(150, 200, window=multiplayer)
            self.menu_canvas.create_window(150, 250, window=random_maze)
            self.menu_canvas.create_window(80, 80, window=homepage)
            self.menu_canvas.create_window(150, 150, window=resume_button)
            self.menu_canvas.create_window(190, 80, window=down_level)
            self.menu_canvas.create_window(240, 80, window=up_level)

        def up_level(self):
            self.mode += 1
            self.menu_canvas.itemconfig(self.mode_text, text= str(self.mode+1))

        def down_level(self):
            self.mode -= 1
            self.menu_canvas.itemconfig(self.mode_text, text= str(self.mode+1))

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
            #customization and maze game images
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

            # item images
            self.item1 = self.load_gif_frames(r"Images\Soup.gif")
            self.item2 = self.load_gif_frames(r"Images\Book.gif")
            self.item3 = self.load_gif_frames(r"Images\water item.gif")
            self.item4 = self.load_gif_frames(r"Images\renewable energy symbol.gif")
            self.item5 = self.load_gif_frames(r"Images\Tree (1).gif")
            self.item6 = self.load_gif_frames(r"Images\Plastic Bag from Ocean (1).gif")
            self.invalid_mode = self.load_gif_frames(r"Images\bouncing ball.gif")
            self.item_list = [self.item1, self.item2, self.item3, self.item4, [self.item5, self.item6]]
            self.item_indices = [12, 9, 6, 3, 0]  # Indices for each item type based on mode

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
                pass  # Reached end of frames
            return frames
        
        def logical_to_canvas(self, row, col):
            # Convert logical maze coordinates to canvas pixel coordinates (center of cell).
            x = col * self.cell_size_x + int(self.cell_size_x / 2)
            y = row * self.cell_size_y + int(self.HEIGHT / 14) + int(self.cell_size_y / 2)
            return x, y

        def draw_maze(self):
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
                        if self.mode >= 12:
                            item_image = self.item_list[4][randint(0, 1)]
                            self.time_limit = 200  # Increase time limit for higher levels
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
                            self.item_message = ["Error 404: Invalid mode selected."]
                        cx, cy = self.logical_to_canvas(row, col)
                        item_id = self.maze_canvas.create_image(cx, cy, image=item_image[0])
                        self.item_message = self.item_message_list[self.mode]
                        self.items.append({"pos": [row, col], "id": item_id})
                        self.lev_item_list.append(item_image)
                        self.total_items += 1

        def animate_character(self):
            if not hasattr(self, 'character_frame_index'):
                self.character_frame_index = 0

            if self.player_pos is None:
                return
            self.character_frame_index = (self.character_frame_index + 1) % self.frameCnt
            x, y = self.logical_to_canvas(self.player_pos[0], self.player_pos[1])
            self.maze_canvas.coords(self.player, x, y)
            self.maze_canvas.itemconfig(self.player, image=self.character_frames[self.character_frame_index])
            if not self.finished and not self.stop:
                self.master.after(500, self.animate_character)
            
        def animate_item(self):
            if not hasattr(self, 'item_frame_index'):
                self.item_frame_index = 0

            for item in self.items:
                item_id = item["id"]
                item_pos = item["pos"]
                x, y = self.logical_to_canvas(item_pos[0], item_pos[1])
                self.maze_canvas.coords(item_id, x, y)

            self.item_frame_index = (self.item_frame_index + 1) % len(self.item_list[self.mode])
            z = 0
            for item in self.items:
                self.maze_canvas.itemconfig(item["id"], image=self.lev_item_list[z][self.item_frame_index])
                z += 1

            if not self.finished and not self.stop:
                self.master.after(500, self.animate_item)

        def move_player(self, event):
            if self.finished or self.stop:
                return
            else:
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
                        self.finished = True
                        self.stop = True
                        
                        # Cancel the timer immediately
                        if hasattr(self, 'timer_id'):
                            try:
                                self.master.after_cancel(self.timer_id)
                            except:
                                pass

                        self.end_time = time.time()
                        self.total_time = round(self.end_time - self.start_time)
                        score = int(self.score * 100) + ((150 - self.total_time) * 5)
                        df = pd.read_csv("highscores.csv")
                        highscore = df.iloc[self.mode, 1]

                        if highscore < score:
                            highscore = score
                            df.iat[self.mode, 1] = score
                            df.to_csv('highscores.csv', index=False)
                            
                        message_str = f"Congratulations!\nYou've completed the maze!\nItems collected: {self.score}/{self.total_items} \nTime used {self.total_time} seconds \nTotal score: {(self.score * 100) + ((150 - self.total_time) * 5)}, Highest score: {highscore}"
                        fin_window = Toplevel(self.master)
                        self.finished = True
                        message = Label(
                            fin_window, 
                            text=message_str, 
                            font=('Arial', 16), 
                            pady=20, 
                            padx=20
                        )
                        message.pack()
                
                        restart_button = Button(
                            fin_window, 
                            text="Play Again", 
                            command=lambda: [fin_window.destroy(), self.start(self.master, self.mode, self.maze_canvas, self.selected_wall, self.selected_character, self.current_theme)]
                        )
                        restart_button.pack(pady=10)

                        nextLevelButton = Button(
                            fin_window,
                            text="Next Level",
                            command=lambda: [fin_window.destroy(), self.start(self.master, (self.mode+1), self.maze_canvas, self.selected_wall, self.selected_character, self.current_theme)]
                        )
                        nextLevelButton.pack(pady=13)

        def check_item_collision(self, row, col):
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
            # Show a message for the collected item
            if self.finished or self.stop:
                return
            if hasattr(self, 'info_window') and self.info_window:
                self.info_window.destroy()
            
            self.stop = True  # Stop the game for a moment to show the message
            self.paused_time = time.time() - self.start_time

            # create canvas for the message
            self.info_canvas = Canvas(self.master, height=300, width=300, bg=self.themes["overlap"])
            self.info_canvas.place(x=self.WIDTH / 2, y=self.HEIGHT / 2, anchor="center")

            # message text
            self.info_canvas.create_text(150, 30, text="Item Collected!", font=("Comic Sans MS", 16), fill=self.themes["text"])
            self.info_canvas.create_text(150, 70, text="Item Information:", font=("Comic Sans MS", 14), fill=self.themes["text"])
            self.info_canvas.create_text(150, 110, anchor="n", width=250, text=self.item_message[self.score - 1], font=('Comic Sans MS', 12), fill=self.themes["text"])

            # Close button
            close_button = Button(self.info_canvas, text="Close", command=self.close_item_message, bg=self.themes["button"], fg=self.themes["text"])
            self.info_canvas.create_window(150, 270, window=close_button)

        def close_item_message(self):
            if hasattr(self, 'info_canvas') and self.info_canvas:
                self.info_canvas.destroy()
                self.info_canvas = None
            
            # Resume the game
            self.stop = False
            if not self.finished:
                # Adjust the start time to account for paused time
                self.start_time = time.time() - self.paused_time
                
                # Restart animations and timer
                self.animate_character()
                self.update_timer()
        
        def update_timer(self):
            # Check if game should stop
            if self.maze_canvas is None or self.finished or self.stop:
                return
            
            current_time = int(time.time() - self.start_time)
            
            if current_time >= self.time_limit:
                self.stop = True
                self.finished = True
                
                # Cancel any pending timer updates
                if hasattr(self, 'timer_id'):
                    self.master.after_cancel(self.timer_id)
                
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
                    command=lambda: [game_over_win.destroy(), self.start(self.master, self.mode, self.maze_canvas, self.selected_wall, self.selected_character, self.current_theme)]
                )
                restart_button.pack(pady=10)
            else:
                self.maze_canvas.itemconfig(self.time_text, text=f"Time: {current_time} seconds")
                # Store the timer ID so we can cancel it if needed
                self.timer_id = self.master.after(1000, self.update_timer)

    class MultiplayerMazeGame:
        def __init__(self):
            # Removing recursion 
            self.HomePage = None 
            self.themes_1 = {
                "light": {
                    "bg": "#CCCCCC",
                    "canvas": "#98c1d9",
                    "text": "black",
                    "button": "#BFD6E3",
                    "fg": "black"  # Added for consistency
                },
                "dark": {
                    "bg": "#2C2C2C",
                    "canvas": "#1E1E1E",
                    "text": "white",
                    "button": "#777272",
                    "fg": "white"  # Added for consistency
                }
            }

        def start(self, master, mode, canvas, current_wall_i, current_char_i, theme):
            self.current_theme = theme
            self.mode = mode
            self.themes = self.themes_1[self.current_theme]
            self.master = master
            self.master.title("Running for 2030 - Multiplayer")
            self.canvas = canvas
            if self.canvas:
                self.canvas.destroy()
            
            # Divide screen into two halves
            self.left_frame = Frame(master)
            self.right_frame = Frame(master)
            self.left_frame.pack(side=LEFT, fill=BOTH, expand=True)
            self.right_frame.pack(side=RIGHT, fill=BOTH, expand=True)
            
            # Create canvases for each player
            self.canvas1 = Canvas(self.left_frame, height=500, width=560, bg=self.themes["canvas"])
            self.canvas2 = Canvas(self.right_frame, height=500, width=560, bg=self.themes["canvas"])
            self.canvas1.pack()
            self.canvas2.pack()
            
            # Initialize player scores
            self.score1 = 0
            self.score2 = 0
            self.player1_finished = False
            self.player2_finished = False
            
            # Prepare images
            self.img1 = PhotoImage(file=r"C:\Users\VelezB1\OneDrive - CEDR\Documents\Coding\Python\graphics\Tk - graphics\Coding challenge\Images\book.png")
            self.img2 = self.img1.subsample(12)
            
            self.cell_size = 20
            
            # Define the maze (same for both players)
            self.maze = LEVELS[self.mode]

            # Initialize player positions and items
            self.player1_pos = None
            self.player2_pos = None
            self.end_pos = None
            self.items1 = []  # Items for player 1
            self.items2 = []  # Items for player 2
            self.total_items = 0
            
            # Bind keys - Player 1 uses arrow keys, Player 2 uses WASD
            self.master.bind("<KeyPress>", self.handle_keypress)
            
            self.initialize_game()

        def initialize_game(self):
            # Draw maze for both players
            self.draw_maze(self.canvas1, 1)
            self.draw_maze(self.canvas2, 2)
            
            # Create score displays
            self.score_text1 = self.canvas1.create_text(280, 470, text=f"Player 1: {self.score1}", font=('Arial', 16), fill="blue")
            self.score_text2 = self.canvas2.create_text(280, 470, text=f"Player 2: {self.score2}", font=('Arial', 16), fill="red")
            
            # Create timer
            self.time_elapsed = 0
            self.timer_text = self.canvas1.create_text(80, 470, text="Time: 0", font=('Arial', 14))
            self.update_timer()
            
        def draw_maze(self, canvas, player_num):
            for row in range(len(self.maze)):
                for col in range(len(self.maze[row])):
                    x1 = col * self.cell_size
                    y1 = row * self.cell_size
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size

                    if self.maze[row][col] == "W":
                        canvas.create_rectangle(x1, y1, x2, y2, fill="black")
                    elif self.maze[row][col] == "S":
                        if player_num == 1 and not self.player1_pos:
                            self.player1_pos = [row, col]
                            color = "blue"
                            self.player1 = canvas.create_oval(x1+4, y1+4, x2-4, y2-4, fill=color)
                        elif player_num == 2 and not self.player2_pos:
                            self.player2_pos = [row, col]
                            color = "red"
                            self.player2 = canvas.create_oval(x1+4, y1+4, x2-4, y2-4, fill=color)
                    elif self.maze[row][col] == "E":
                        self.end_pos = [row, col]
                        canvas.create_rectangle(x1, y1, x2, y2, fill="green")
                    elif self.maze[row][col] == "*":
                        item = canvas.create_image(x1+10, y1+10, image=self.img2)
                        if player_num == 1:
                            self.items1.append({"pos": [row, col], "id": item})
                        else:
                            self.items2.append({"pos": [row, col], "id": item})
                        if player_num == 1:  # Only count once
                            self.total_items += 1
        
        def handle_keypress(self, event):
            # Player 1 controls (Arrow keys)
            if event.keysym in ["Up", "Down", "Left", "Right"]:
                self.move_player(1, event.keysym)
            
            # Player 2 controls (WASD)
            elif event.keysym.lower() in ["w", "a", "s", "d"]:
                # Convert WASD to arrow key equivalents
                wasd_to_arrows = {"w": "Up", "a": "Left", "s": "Down", "d": "Right"}
                self.move_player(2, wasd_to_arrows[event.keysym.lower()])
        
        def move_player(self, player_num, direction):
            if player_num == 1 and self.player1_finished:
                return
            if player_num == 2 and self.player2_finished:
                return
            
            if player_num == 1:
                row, col = self.player1_pos
                player_id = self.player1
                canvas = self.canvas1
            else:
                row, col = self.player2_pos
                player_id = self.player2
                canvas = self.canvas2
            
            new_row, new_col = row, col

            if direction == "Up":
                new_row -= 1
            elif direction == "Down":
                new_row += 1
            elif direction == "Left":
                new_col -= 1
            elif direction == "Right":
                new_col += 1

            # Check if move is valid
            if (0 <= new_row < len(self.maze) and 
                0 <= new_col < len(self.maze[0]) and 
                self.maze[new_row][new_col] != "W"):
                
                # Update player position
                if player_num == 1:
                    self.player1_pos = [new_row, new_col]
                else:
                    self.player2_pos = [new_row, new_col]
                    
                x1 = new_col * self.cell_size
                y1 = new_row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                canvas.coords(player_id, x1+4, y1+4, x2-4, y2-4)

                # Check for item collection
                items = self.items1 if player_num == 1 else self.items2
                for item in items[:]:
                    if item["pos"] == [new_row, new_col]:
                        canvas.delete(item["id"])
                        items.remove(item)
                        if player_num == 1:
                            self.score1 += 1
                            self.canvas1.itemconfig(self.score_text1, text=f"Player 1: {self.score1}")
                        else:
                            self.score2 += 1
                            self.canvas2.itemconfig(self.score_text2, text=f"Player 2: {self.score2}")

                # Check if player reached the end
                if [new_row, new_col] == self.end_pos:
                    if player_num == 1:
                        self.player1_finished = True
                    else:
                        self.player2_finished = True
                    
                    self.check_game_over()
        
        def check_game_over(self):
            if self.player1_finished and self.player2_finished:
                # Both players finished
                winner = "It's a tie!"
                if self.score1 > self.score2:
                    winner = "Player 1 wins!"
                elif self.score2 > self.score1:
                    winner = "Player 2 wins!"
                    
                message = (f"Game Over!\n"
                        f"{winner}\n"
                        f"Player 1: {self.score1}/{self.total_items}\n"
                        f"Player 2: {self.score2}/{self.total_items}\n"
                        f"Time: {self.time_elapsed} seconds")
                messagebox.showinfo("Game Over", message)
                self.master.quit()
        
        def update_timer(self):
            if not (self.player1_finished and self.player2_finished):
                self.time_elapsed += 1
                self.canvas1.itemconfig(self.timer_text, text=f"Time: {self.time_elapsed}")
                self.master.after(1000, self.update_timer)
                
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
