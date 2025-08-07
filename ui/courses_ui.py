import requests
import json
import tkinter as tk
from tkinter import messagebox

# Import modular UI components
from course_details_window import show_course_details_window
from practices_window import show_practices_window
from code_editor_window import show_code_editor_window

def fetch_cu_courses(jwt_token):
    API_URL = "https://bytexl.app/api/courses?includeMetrics=true"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(API_URL, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                cu_courses = [course for course in data if str(course.get('title', '')).strip().startswith('CU')]
            elif isinstance(data, dict) and 'courses' in data:
                cu_courses = [course for course in data['courses'] if str(course.get('title', '')).strip().startswith('CU')]
            else:
                cu_courses = []
            return cu_courses
        else:
            return None
    except Exception as e:
        print(f"Error fetching courses: {e}")
        return None

def show_courses_window(courses, jwt_token=None):
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
            show_course_details_window(courses[idx], jwt_token, lambda module, jwt: show_practices_window(module, jwt, show_code_editor_window))

    listbox.bind('<<ListboxSelect>>', on_course_select)
    win.mainloop()




