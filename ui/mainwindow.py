from .courses_ui import fetch_cu_courses, show_courses_window
import tkinter as tk
from tkinter import simpledialog, messagebox


# --- UI Classes ---
class TokenWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Enter JWT Token")
        self.master.geometry("400x180")
        self.token = None

        self.label = tk.Label(master, text="Please enter your JWT token:")
        self.label.pack(pady=10)

        self.token_entry = tk.Entry(master, width=50, show="*")
        self.token_entry.pack(pady=5)

        self.submit_button = tk.Button(master, text="Submit", command=self.submit_token)
        self.submit_button.pack(pady=10)

        self.status_label = tk.Label(master, text="")
        self.status_label.pack(pady=5)

    def submit_token(self):
        token = self.token_entry.get().strip()
        if not token:
            messagebox.showerror("Error", "JWT token cannot be empty.")
            return
        self.token = token
        self.status_label.config(text="Fetching CU courses...")
        self.master.after(100, self.fetch_and_show_courses)

    def fetch_and_show_courses(self):
        cu_courses = fetch_cu_courses(self.token)
        if cu_courses is not None:
            self.master.destroy()
            show_courses_window(cu_courses, jwt_token=self.token)
        else:
            self.status_label.config(text="Failed to fetch courses. Check your token.")


def main():
    root = tk.Tk()
    app = TokenWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
