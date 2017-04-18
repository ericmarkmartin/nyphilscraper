import tkinter as tk
from nyphilscraper.Application import Application


if __name__ == '__main__':
    root = tk.Tk()
    root.title("NY Phil Archive Scraper")
    App = Application(root).pack(fill='both', expand=True)
    root.mainloop()
