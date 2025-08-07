import tkinter as tk
import re
from .api_client import fetch_lab_data, fetch_test_questions

def show_practices_window(module, jwt_token, show_code_editor_window):
    practices_win = tk.Toplevel()
    practices_win.title(module.get('title', 'Unit Details'))
    practices_win.geometry("600x400")

    label = tk.Label(practices_win, text=module.get('title', ''), font=("Arial", 14, "bold"))
    label.pack(pady=10)

    topics = module.get('topics', [])
    practices = []
    for topic in topics:
        if 'subTopics' in topic:
            for sub in topic['subTopics']:
                if 'Practice' in sub.get('title', '') or sub.get('topicType', '').lower() == 'lab':
                    practices.append(sub)
        elif 'Practice' in topic.get('title', '') or topic.get('topicType', '').lower() == 'lab':
            practices.append(topic)


    practices_listbox = tk.Listbox(practices_win, width=80, height=12)
    for p in practices:
        practices_listbox.insert(tk.END, p.get('title', 'Untitled Practice'))
    if not practices:
        practices_listbox.insert(tk.END, "No practices found in this unit.")
    practices_listbox.pack(pady=10)

    # Add a Text widget for all questions display
    question_text = tk.Text(practices_win, height=18, wrap='word', font=("Arial", 11))
    question_text.pack(pady=5, fill='both', expand=True)
    question_text.config(state='disabled')


    def on_practice_select(event, jwt_token=jwt_token):
        import json
        import os
        selection = practices_listbox.curselection()
        if selection and practices:
            idx = selection[0]
            # DEBUG: Print the module dict to check lab_id
            print("[DEBUG] module passed to show_practices_window:")
            print(module)
            # Save the module dict to a file for debugging
            try:
                with open('module_debug.json', 'w', encoding='utf-8') as debugf:
                    json.dump(module, debugf, ensure_ascii=False, indent=2)
                print('[DEBUG] Saved module to module_debug.json')
            except Exception as e:
                print(f'[DEBUG] Failed to save module_debug.json: {e}')
            # Fetch lab_id from the selected practice's 'data' field (URL)
            practice = practices[idx]
            lab_url = practice.get('data', '')
            lab_id = None
            if '/lab/' in lab_url:
                lab_id = lab_url.split('/lab/')[-1].split('/')[0]
            print(f"[DEBUG] lab_url: {lab_url}")
            print(f"[DEBUG] lab_id: {lab_id}")
            test_id = None
            if lab_id and jwt_token:
                lab_data = fetch_lab_data(lab_id, jwt_token)
                # Try to extract test_id from lab_data (if link present)
                lab_link = None
                if lab_data:
                    lab_link = lab_data.get('link')
                if lab_link:
                    match = re.search(r'/test/([a-zA-Z0-9]+)', lab_link)
                    if match:
                        test_id = match.group(1)
            # Always call fetch_test_questions if test_id and jwt_token
            if test_id and jwt_token:
                try:
                    fetch_test_questions(test_id, jwt_token)
                except Exception as e:
                    print(f"[DEBUG] API call failed: {e}")
            # Now display all questions from dat.json
            try:
                question_text.config(state='normal')
                question_text.delete('1.0', tk.END)
                if os.path.exists('dat.json'):
                    with open('dat.json', 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    questions = data.get('data', {}).get('questions', [])
                    if questions:
                        for i, q in enumerate(questions, 1):
                            title = q.get('title', 'No Title')
                            desc = q.get('description', 'No Description')
                            question_text.insert(tk.END, f"Q{i}. {title}\n\n{desc}\n\n{'-'*60}\n\n")
                    else:
                        question_text.insert(tk.END, "No questions found in dat.json.")
                else:
                    question_text.insert(tk.END, "dat.json not found.")
                question_text.config(state='disabled')
            except Exception as e:
                question_text.config(state='normal')
                question_text.delete('1.0', tk.END)
                question_text.insert(tk.END, f"Failed to load questions: {e}")
                question_text.config(state='disabled')
            show_code_editor_window(test_id,practices[idx], jwt_token)

    practices_listbox.bind('<<ListboxSelect>>', on_practice_select)
