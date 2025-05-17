import tkinter as tk
from GUI import MovieGenerator

def main():
    root = tk.Tk()
    app = MovieGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()


