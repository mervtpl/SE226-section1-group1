import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from PIL import Image, ImageTk
import io
import fetching_data
import generate


class MovieGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("PDA-226 - AI Movie Dialogue & Scene Generator")
        self.root.geometry("1200x700")

       #grid
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=2)
        self.root.rowconfigure(5, weight=1)

        #list of 10 movies from Imdb
        self.movie_listbox = tk.Listbox(root, height=12, width=45)
        self.movie_listbox.grid(row=0, column=0, padx=10, pady=10, rowspan=4, sticky='nsew')
        self.movie_listbox.bind("<<ListboxSelect>>", self.on_movie_select)

        #movie info
        self.movie_info = tk.Text(root, width=60, height=12, wrap=tk.WORD)
        self.movie_info.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        #user inputs
        tk.Label(root, text="Number of Characters (2–4):").grid(row=1, column=1, sticky='w')
        self.num_chars_entry = ttk.Entry(root, width=10)
        self.num_chars_entry.insert(0, "2")
        self.num_chars_entry.grid(row=1, column=1, sticky='e')

        tk.Label(root, text="Max Dialogue Words (max 1500):").grid(row=2, column=1, sticky='w')
        self.max_words_entry = ttk.Entry(root, width=10)
        self.max_words_entry.insert(0, "500")
        self.max_words_entry.grid(row=2, column=1, sticky='e')

        #location
        tk.Label(root, text="Location (enter story location):").grid(row=3, column=1, sticky='nw')
        self.location_text = tk.Text(root, width=30, height=2)
        self.location_text.insert(tk.END, "New York")
        self.location_text.grid(row=3, column=1, sticky='e')

        #style
        tk.Label(root, text="Style:").grid(row=4, column=0, sticky='w', padx=10)
        self.style_options = ["Marvel", "Futuristic", "Cartoon", "Realistic"]
        self.style_dropdown = ttk.Combobox(root, values=self.style_options, state="readonly", width=22)
        self.style_dropdown.set(self.style_options[0])
        self.style_dropdown.grid(row=4, column=0, sticky='w', padx=160)

        #buttons
        self.generate_button = tk.Button(root, text="Generate Dialogue and Image", command=self.generate_all)
        self.generate_button.grid(row=4, column=1, pady=10, sticky='w')

        self.clear_button = tk.Button(root, text="Clear All", command=self.clear_inputs)
        self.clear_button.grid(row=4, column=1, pady=10, sticky='e')

        #output box
        self.dialogue_output = scrolledtext.ScrolledText(root, width=80, height=15, wrap=tk.WORD)
        self.dialogue_output.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        self.image_label = tk.Label(root)
        self.image_label.grid(row=0, column=2, rowspan=6, padx=10, pady=10, sticky='nsew')

        self.top_movies = []
        self.selected_movie = None
        self.storyline = ""
        self.populate_movies()

        # Add padding to all widgets
        for child in root.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def populate_movies(self):
        self.top_movies = fetching_data.fetch_top_10_movies()
        for title, _ in self.top_movies:
            self.movie_listbox.insert(tk.END, title)

    def on_movie_select(self, event):
        index = self.movie_listbox.curselection()
        if not index:
            return
        idx = index[0]
        title, link = self.top_movies[idx]
        summary_data = fetching_data.get_movie_summary(link)
        self.storyline = fetching_data.get_movie_storyline(title)

        self.selected_movie = {
            "title": title,
            "link": link,
            "summary": summary_data.get("summary", ""),
            "storyline": self.storyline
        }

        self.movie_info.delete("1.0", tk.END)
        self.movie_info.insert(tk.END, f"Title: {title}\n\n")
        self.movie_info.insert(tk.END, f"Summary:\n{self.selected_movie['summary']}\n\n")
        self.movie_info.insert(tk.END, f"Storyline:\n{self.storyline}")

    def generate_all(self):
        if not self.selected_movie:
            messagebox.showerror("No Movie", "Please select a movie first.")
            return

        try:
            #disabling buttons when generating
            self.generate_button.config(state=tk.DISABLED)
            self.clear_button.config(state=tk.DISABLED)
            self.dialogue_output.delete("1.0", tk.END)
            self.dialogue_output.insert(tk.END, "Generating... Please wait...")
            self.root.update()  # Force GUI update

            num_chars = int(self.num_chars_entry.get())
            max_words = int(self.max_words_entry.get())
            location = self.location_text.get("1.0", tk.END).strip()
            style = self.style_dropdown.get().strip()

            if not (2 <= num_chars <= 4):
                raise ValueError("Number of characters must be between 2 and 4.")
            if max_words <= 0 or max_words > 1500:
                raise ValueError("Dialogue length must be between 1 and 1500 words.")
            if not location or not style:
                raise ValueError("Location and style cannot be empty.")

            storyline = self.selected_movie["storyline"]

            scene_desc = generate.generate_scene_description(storyline)
            dialogue = generate.generate_dialogue(storyline, num_chars, max_words)

            self.dialogue_output.delete("1.0", tk.END)
            self.dialogue_output.insert(tk.END, f"Scene Description:\n{scene_desc}\n\n")
            self.dialogue_output.insert(tk.END, "Generated Dialogue:\n")
            self.dialogue_output.insert(tk.END, dialogue)

            img_bytes = generate.generate_image(scene_desc, location, style)
            image = Image.open(io.BytesIO(img_bytes))
            image = image.resize((400, 400))
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo

            self.ask_save_dialogue(dialogue)
            self.ask_continue()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        finally:
            # Re-enable buttons
            self.generate_button.config(state=tk.NORMAL)
            self.clear_button.config(state=tk.NORMAL)

    def clear_inputs(self):
        """Reset all input fields except movie selection"""
        self.dialogue_output.delete("1.0", tk.END)
        self.image_label.config(image=None)
        self.num_chars_entry.delete(0, tk.END)
        self.num_chars_entry.insert(0, "2")
        self.max_words_entry.delete(0, tk.END)
        self.max_words_entry.insert(0, "500")
        self.location_text.delete("1.0", tk.END)
        self.location_text.insert(tk.END, "New York")
        self.style_dropdown.set(self.style_options[0])

    def ask_continue(self):
        answer = messagebox.askyesno("Continue?", "Would you like to generate another dialogue?")
        if answer:
            self.clear_inputs()

    def ask_save_dialogue(self, dialogue):
        default_name = "dialogue.txt"
        if self.selected_movie:
            default_name = f"{self.selected_movie['title']}_dialogue.txt".replace(" ", "_")

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=default_name,
            filetypes=[("Text files", "*.txt")]
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(dialogue)


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieGenerator(root)
    root.mainloop()