import tkinter as tk

def show_course_details_window(course, jwt_token, show_practices_window):
    detail_win = tk.Toplevel()
    detail_win.title(course.get('title', 'Course Details'))
    detail_win.geometry("600x400")

    label = tk.Label(detail_win, text=course.get('title', ''), font=("Arial", 14, "bold"))
    label.pack(pady=10)

    desc = course.get('description', '')
    desc_label = tk.Label(detail_win, text=desc, wraplength=550, justify='left')
    desc_label.pack(pady=5)

    units_label = tk.Label(detail_win, text="Units/Modules:", font=("Arial", 12, "bold"))
    units_label.pack(pady=5)

    modules = course.get('modules', [])
    units_listbox = tk.Listbox(detail_win, width=80, height=10)
    for module in modules:
        units_listbox.insert(tk.END, module.get('title', 'Untitled Unit'))
    units_listbox.pack(pady=5)

    def on_unit_select(event):
        selection = units_listbox.curselection()
        if selection:
            idx = selection[0]
            show_practices_window(modules[idx], jwt_token)

    units_listbox.bind('<<ListboxSelect>>', on_unit_select)
