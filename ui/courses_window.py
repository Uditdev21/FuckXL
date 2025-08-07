import tkinter as tk
from tkinter import messagebox

def show_courses_window(courses, jwt_token, show_course_details_window):
    win = tk.Tk()
    win.title("CU Courses")
    win.geometry("600x400")

    label = tk.Label(win, text="CU Courses", font=("Arial", 16, "bold"))
    label.pack(pady=10)

    listbox = tk.Listbox(win, width=80, height=20)
    for course in courses:
        title = course.get('title', 'No Title')
        desc = course.get('description', '')
        listbox.insert(tk.END, f"{title}: {desc[:80]}{'...' if len(desc)>80 else ''}")
    listbox.pack(pady=10)

    def on_course_select(event):
        selection = listbox.curselection()
        if selection:
            idx = selection[0]
            show_course_details_window(courses[idx], jwt_token)

    listbox.bind('<<ListboxSelect>>', on_course_select)
    win.mainloop()
