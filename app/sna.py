import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Art Networks on Ghibli Style Content")
        
        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Set window size to full screen dimensions
        self.geometry(f"{screen_width}x{screen_height}")
        self.state('zoomed')  # Windows maximized state
        
        # Ghibli-inspired color palette
        self.ghibli_colors = {
            "light_cream": "#f5f0e1",
            "sky_blue": "#8ec5fc",
            "nature_green": "#a8e6cf",
            "pastel_pink": "#ffaaa5",
            "soft_yellow": "#fdffab",
            "dusty_lavender": "#d3c0f9"
        }
        
        self.configure(bg=self.ghibli_colors["light_cream"])  # Main background

        # Configure styles with Ghibli colors
        self.setup_styles()

        # Main container with background color
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, SecondPage, ImagePage1, ImagePage2, ImagePage3):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        
        # Add keyboard shortcut for full screen toggle (F11)
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)
        
        # Fullscreen flag
        self.fullscreen = False

    def setup_styles(self):
        """Set up ttk styles with Ghibli-inspired colors"""
        style = ttk.Style()
        style.theme_use("default")
        
        # Configure frame styles
        style.configure("TFrame", background=self.ghibli_colors["light_cream"])
        
        # Configure label styles
        style.configure("TLabel", 
                      background=self.ghibli_colors["light_cream"], 
                      foreground="#3e3e3e", 
                      font=("Helvetica", 12))
        
        # Title label style
        style.configure("Title.TLabel", 
                      background=self.ghibli_colors["light_cream"], 
                      foreground="#3e3e3e", 
                      font=("Helvetica", 24, "bold"))
        
        # Configure button styles
        style.configure("TButton", 
                      font=("Helvetica", 11, "bold"), 
                      background=self.ghibli_colors["nature_green"],
                      padding=8)
        
        # Button when hovered
        style.map("TButton",
                background=[('active', self.ghibli_colors["sky_blue"])])
        
        # Home button style
        style.configure("Home.TButton", 
                      font=("Helvetica", 12, "bold"),
                      background=self.ghibli_colors["pastel_pink"],
                      padding=10)

    def show_frame(self, page):
        """Raise the frame to the top"""
        frame = self.frames[page]
        frame.tkraise()
        
    def toggle_fullscreen(self, event=None):
        """Toggle between fullscreen and windowed mode"""
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)
        return "break"
        
    def end_fullscreen(self, event=None):
        """Exit fullscreen mode"""
        self.fullscreen = False
        self.attributes("-fullscreen", False)
        return "break"

class ScrollableFrame(ttk.Frame):
    """A scrollable frame for content that might exceed the window size"""
    def __init__(self, container, *args, **kwargs):
        bg_color = kwargs.pop('background', '#f5f0e1') if 'background' in kwargs else '#f5f0e1'
        super().__init__(container, *args, **kwargs)
        
        # Create a canvas with scrollbar
        self.canvas = tk.Canvas(self, bg=bg_color)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # Frame inside canvas that will contain actual widgets
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        # Configure canvas to work with scrollbar
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create window inside canvas containing the frame
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Configure scrollable area to expand with frame
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.configure_scroll_region()
        )
        
        # Configure canvas to expand with window
        self.canvas.bind("<Configure>", lambda e: self.on_canvas_configure(e))
        
        # Bind mousewheel to scroll
        self.bind_mousewheel()
    
    def configure_scroll_region(self):
        """Update scroll region to include all content"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def on_canvas_configure(self, event):
        """Resize the inner frame to match the canvas width"""
        width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=width)
        
    def bind_mousewheel(self):
        """Bind mousewheel to scrolling"""
        # Windows and MacOS
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        # Linux
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)
        
    def _on_mousewheel(self, event):
        """Handle mousewheel event"""
        if hasattr(event, 'num'):  # Linux
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")
        elif hasattr(event, 'delta'):  # Windows/MacOS
            if event.delta > 0:
                self.canvas.yview_scroll(-1, "units")
            else:
                self.canvas.yview_scroll(1, "units")

class StartPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(style="TFrame")
        
        # Create a scrollable frame for content
        scroll_frame = ScrollableFrame(self, background=controller.ghibli_colors["light_cream"])
        scroll_frame.pack(fill="both", expand=True)
        
        content_frame = scroll_frame.scrollable_frame
        
        # Styled title with background accent
        title_frame = ttk.Frame(content_frame)
        title_frame.pack(fill="x", pady=30)
        
        label = ttk.Label(title_frame, text="Welcome to Ghibli Community World", style="Title.TLabel")
        label.pack(pady=30)
        
        # Center-aligned description with custom background
        desc_frame = ttk.Frame(content_frame, style="TFrame")
        desc_frame.pack(fill="x", padx=100, pady=20)
        
        description = ttk.Label(desc_frame, text="""
        To investigate the dynamics of AI art communities, we curated and analyzed a dataset of AI-generated Studio Ghibli-style content shared across various digital platforms. The dataset captures rich metadata for each image, including the image ID, user ID, generation prompt, and engagement metrics such as likes, shares, and comments. Additional attributes include platform type (e.g., Reddit, Instagram, TikTok, Twitter), generation time, GPU usage, file size, image resolution, style accuracy score, post-generation manual edits, ethical concern flags, creation date, and the top user comment. This comprehensive dataset enables a multidimensional exploration of how AI-generated art circulates, resonates, and evolves within online spaces. In line with our problem statement, this work focuses on identifying and analyzing three distinct community structures: (1) User Engagement Communities, which group users based on interaction patterns to reveal interest clusters and potential influencers; (2) Prompt Similarity Communities, formed by semantically similar prompts to uncover thematic trends and prompt engineering insights; and (3) Image-Based Communities, where clustering is driven by a combination of style accuracy and engagement, enabling distinction between aesthetic appeal and content virality.
        """, wraplength=800, justify="center", font=("Helvetica", 12))
        description.pack(pady=10, padx=20)
        
        # Button with custom background
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=40)
        
        button = ttk.Button(button_frame, text="Uncover the Image Communities",
                            command=lambda: controller.show_frame(SecondPage))
        button.pack(pady=10)
        
        # Add fullscreen indicator and instructions
        instructions = ttk.Label(content_frame, 
                               text="Press F11 for fullscreen mode, ESC to exit fullscreen",
                               font=("Helvetica", 10, "italic"))
        instructions.pack(pady=30)

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence

class SecondPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Create a scrollable frame for content
        scroll_frame = ScrollableFrame(self, background=controller.ghibli_colors["soft_yellow"])
        scroll_frame.pack(fill="both", expand=True)
        
        content_frame = scroll_frame.scrollable_frame
        content_frame.configure(style="TFrame")
        
        # Styled title with different background
        title_frame = ttk.Frame(content_frame)
        title_frame.configure(style="TFrame")
        title_frame.pack(fill="x", pady=30)
        
        label = ttk.Label(title_frame, 
                          text="Choose the preferred realm of Ghibli Communities", 
                          style="Title.TLabel")
        label.pack(pady=30)
        
        # Center-aligned options
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=40, padx=20)
        
        # Use Grid layout for equal spacing
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        
        # Create colorful buttons
        btn1 = ttk.Button(button_frame, 
                          text="User Engagement Based\n(Louvain Algorithm)", 
                          command=lambda: controller.show_frame(ImagePage1))
        btn1.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        
        btn2 = ttk.Button(button_frame, 
                          text="Prompt Similarity Based\n(Hybrid and Leiden)", 
                          command=lambda: controller.show_frame(ImagePage2))
        btn2.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")
        
        btn3 = ttk.Button(button_frame, 
                          text="Style Accuracy and Engagement\n(K-Means Clustering)", 
                          command=lambda: controller.show_frame(ImagePage3))
        btn3.grid(row=0, column=2, padx=20, pady=10, sticky="nsew")
        
        # Add visual separator
        separator = ttk.Separator(content_frame, orient="horizontal")
        separator.pack(fill="x", padx=100, pady=30)
        
        # Add description text
        description = ttk.Label(content_frame, 
                                text="Each visualization represents a different approach to understanding\nhow AI-generated Ghibli-style content forms communities online.",
                                font=("Helvetica", 12, "italic"),
                                justify="center")
        description.pack(pady=20)
        
        # ====== ADD GIF ANIMATION ======
        self.gif_label = tk.Label(content_frame)
        self.gif_label.pack(pady=20)

        self.frames = []  # to store all frames of the gif
        gif_path = "bunny.gif"  # <<< put your gif path here

        gif = Image.open(gif_path)
        for frame in ImageSequence.Iterator(gif):
            frame = frame.resize((800, 400))  # Resize if you want
            frame_image = ImageTk.PhotoImage(frame)
            self.frames.append(frame_image)

        self.frame_index = 0
        self.animate_gif()

    def animate_gif(self):
        frame = self.frames[self.frame_index]
        self.gif_label.configure(image=frame)
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.after(100, self.animate_gif)  # Adjust speed (milliseconds)

class ImagePageTemplate(ttk.Frame):
    def __init__(self, parent, controller, image_path, description_text, bg_color="light_cream"):
        super().__init__(parent)
        self.controller = controller
        
        # Create a scrollable frame for content with themed background
        scroll_frame = ScrollableFrame(self, background=controller.ghibli_colors[bg_color])
        scroll_frame.pack(fill="both", expand=True)
        
        content_frame = scroll_frame.scrollable_frame
        
        # Page title
        label = ttk.Label(content_frame, text="Community Visualization", style="Title.TLabel")
        label.pack(pady=20)
        
        # Image frame with border
        img_frame = ttk.Frame(content_frame, style="TFrame")
        img_frame.pack(pady=20)
        
        # Load and display image
        try:
            # Create directory for images if it doesn't exist
            if not os.path.exists(image_path) and not os.path.exists("images"):
                os.makedirs("images")
                
            img = Image.open(image_path)
            img = img.resize((700, 500))  # Larger size for fullscreen
            self.photo = ImageTk.PhotoImage(img)
            
            # Canvas for image with border
            img_canvas = tk.Canvas(img_frame, width=710, height=510, 
                                 highlightbackground="#3e3e3e", highlightthickness=2,
                                 bg="white")
            img_canvas.pack()
            img_canvas.create_image(355, 255, image=self.photo)
            
        except Exception as e:
            error_label = ttk.Label(img_frame, text=f"Error loading image: {e}")
            error_label.pack(pady=20)
        
        # Text description in scrolled text widget
        text_frame = ttk.Frame(content_frame)
        text_frame.pack(padx=50, pady=20, fill="both")
        
        # Custom text widget with Ghibli styling
        scrolled_txt = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, 
                                               width=100, height=15, 
                                               font=("Georgia", 12),
                                               bg="#ffffff",
                                               fg="#3e3e3e")
        scrolled_txt.pack(fill="both", expand=True)
        scrolled_txt.insert(tk.END, description_text)
        scrolled_txt.configure(state='disabled')
        
        # Navigation buttons in a row
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=20)
        
        back_button = ttk.Button(button_frame, text="Back to Selection", 
                               style="Home.TButton",
                               command=lambda: controller.show_frame(SecondPage))
        back_button.pack(side="left", padx=10)
        
        home_button = ttk.Button(button_frame, text="Return Home", 
                               style="Home.TButton",
                               command=lambda: controller.show_frame(StartPage))
        home_button.pack(side="left", padx=10)

class ImagePage1(ImagePageTemplate):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "ubc.png", """User Community Detection and Characterization

The user clustering process resulted in eight distinct communities based on platform usage patterns and average engagement metrics (likes, shares, and comments).

Cluster 0: 219 users, mostly on Instagram (61) and TikTok (60), with high engagement: 2721.9 likes, 1023.7 shares, 484.5 comments.
Cluster 1: 56 users, primarily Twitter (17) and Reddit (15), averaging 2548.3 likes, 999.1 shares, and 566.2 comments.
Cluster 2: 33 users, similar to Cluster 1, mainly Twitter and Reddit, 2599.4 likes, 969.2 shares, 584.2 comments.
Cluster 3: 44 users, active on TikTok and Twitter, slightly lower engagement.
Cluster 4: 49 users, mostly TikTok and Reddit, with the highest average shares.
Cluster 5: 37 users, Reddit and Twitter, lowest likes but high shares.
Cluster 6: 32 users, mainly Twitter and TikTok, highest likes (2862.2).
Cluster 7: 30 users, mostly Reddit and Twitter, with strong share counts.

Overall, the clustering reveals distinct behaviors and cross-platform dynamics across the AI-generated Ghibli content community.""", "nature_green")

class ImagePage2(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Create a scrollable frame with themed background
        scroll_frame = ScrollableFrame(self, background=controller.ghibli_colors["pastel_pink"])
        scroll_frame.pack(fill="both", expand=True)
        
        content_frame = scroll_frame.scrollable_frame
        
        # Page title
        label = ttk.Label(content_frame, text="Prompt-Based Communities", style="Title.TLabel")
        label.pack(pady=20)
        
        # Main content container
        main_frame = ttk.Frame(content_frame)
        main_frame.pack(padx=40, pady=20)
        
        # Left column - first visualization
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, padx=20)
        
        # Image frame with border
        left_img_frame = ttk.Frame(left_frame)
        left_img_frame.pack(pady=10)
        
        try:
            img1 = Image.open("pbs2.png")
            img1 = img1.resize((500, 350))
            self.photo1 = ImageTk.PhotoImage(img1)
            
            # Canvas for image with border
            img_canvas1 = tk.Canvas(left_img_frame, width=510, height=360, 
                                  highlightbackground="#3e3e3e", highlightthickness=2,
                                  bg="white")
            img_canvas1.pack()
            img_canvas1.create_image(255, 180, image=self.photo1)
            
        except Exception as e:
            error_label = ttk.Label(left_img_frame, text=f"Error loading image: {e}")
            error_label.pack()
        
        # Description text
        desc1 = ttk.Label(left_frame, text="""Prompt Similarity Graph:
        
We observe distinct cluster-wise themes emerging within the prompt-based communities. 

Cluster C0 (Blue) features keywords such as anime, fantasy, Passing, Style, and Train, suggesting that this cluster revolves around fantasy or anime-themed content, potentially inspired by Studio Ghibli films like Spirited Away or Howl's Moving Castle. 

Cluster C1 (Orange) is characterized by terms like Floating, Ghibli, Iceland, Mountain, and Style, indicating a community focused on natural or dreamlike Ghibli-inspired environments. 

Meanwhile, Cluster C6 (Red) emphasizes words such as Enchanted, Exploring, tipper, ruin, and Traveler, reflecting a strong interest in fantasy exploration and narrative-rich world-building.""",
                          wraplength=500, justify="center", font=("Georgia", 11))
        desc1.pack(pady=10)
        
        # Right column - second visualization  
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, padx=20)
        
        # Image frame with border
        right_img_frame = ttk.Frame(right_frame)
        right_img_frame.pack(pady=10)
        
        try:
            img2 = Image.open("kmeans1.png") 
            img2 = img2.resize((500, 350))
            self.photo2 = ImageTk.PhotoImage(img2)
            
            # Canvas for image with border
            img_canvas2 = tk.Canvas(right_img_frame, width=510, height=360, 
                                  highlightbackground="#3e3e3e", highlightthickness=2,
                                  bg="white")
            img_canvas2.pack()
            img_canvas2.create_image(255, 180, image=self.photo2)
            
        except Exception as e:
            error_label = ttk.Label(right_img_frame, text=f"Error loading image: {e}")
            error_label.pack()
            
        # Description text
        desc2 = ttk.Label(right_frame, text="""K-Means Clustering:
        
The K-Means clustering analysis of Studio Ghibli-inspired prompts revealed distinct thematic groupings, as illustrated. 

Using TF-IDF vectorization followed by dimensionality reduction via PCA, we identified five major clusters within the prompt corpus. Cluster 0 (light blue) predominantly features general Ghibli-style scene prompts, such as villages, night scenes, and other classic Ghibli-inspired settings. 

Cluster 1 (orange) captures cozy and mystical settings, while Cluster 3 (purple) focuses on magical landscapes and hidden locations. Notably, the isolated point in Cluster 4 (lime green), representing the "time traveler exploring" prompt, stands out as thematically unique compared to traditional Ghibli imagery. 

Additionally, the "Anime-style train" prompt (dark blue) appears distanced from core Ghibli elements, demonstrating a clear semantic separation. These clustering results underscore the nuanced variations within Ghibli-inspired generative art prompts, revealing how different stylistic and thematic elements naturally organize within semantic space.""",
                          wraplength=500, justify="center", font=("Georgia", 11))
        desc2.pack(pady=10)
        
        # Navigation buttons
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=30)
        
        back_button = ttk.Button(button_frame, text="Back to Selection", 
                               style="Home.TButton",
                               command=lambda: controller.show_frame(SecondPage))
        back_button.pack(side="left", padx=10)
        
        home_button = ttk.Button(button_frame, text="Return Home", 
                               style="Home.TButton",
                               command=lambda: controller.show_frame(StartPage))
        home_button.pack(side="left", padx=10)

class ImagePage3(ImagePageTemplate):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "kmeans2.png", """The application of K-Means clustering to image and engagement features revealed distinct community groupings, as visualized. Using Principal Component Analysis (PCA) for dimensionality reduction, we identified five primary clusters with varying engagement and style accuracy characteristics. 

The analysis demonstrates notable differentiation across the embedding space, with several key regions highlighted in the visualization. The upper-center region contains prompts with "High Engagement, High Style Accuracy," indicating optimal combinations of artistic style adherence and audience response. 

Multiple regions of "Moderate Engagement and Accuracy" appear throughout the feature space, representing the majority of the dataset. The right side of the feature space features a distinct area labeled "Low Style Accuracy," predominantly represented by Cluster 1 (orange) points. 

Cluster 0 (blue) points are concentrated in the lower left quadrant, showing a consistent pattern of moderate to lower engagement metrics. Cluster 2 (green) points exhibit the highest vertical distribution, suggesting greater variance in the second principal component. 

These clustering results emphasize the complex relationship between style accuracy and audience engagement metrics in Ghibli-inspired generative art. The multidimensional nature of the data reveals that while certain prompt characteristics consistently drive higher engagement, there is significant variance in community response patterns across the feature space.""", "dusty_lavender")

if __name__ == "__main__":
    app = App()
    app.mainloop()