from ctypes.util import test
import tkinter as tk
import re
import json
from .api_client import fetch_test_questions

def show_code_editor_window(test_id_value,practice, jwt_token):
    editor_win = tk.Toplevel()
    editor_win.title(practice.get('title', 'Practice'))
    print(f"[DEBUG] Showing code editor for practice: {practice}")
    editor_win.geometry("800x600")



    # --- Multi-question support with pagination ---
    import os
    questions = []
    current_index = [0]  # use list for mutability in nested functions

    # Try to get test_id from lab_data.json
    test_id = None
    if os.path.exists('lab_data.json'):
        try:
            with open('lab_data.json', 'r', encoding='utf-8') as labf:
                lab_data = json.load(labf)
                lab_link = lab_data.get('link', '')
                match = re.search(r'/test/([a-zA-Z0-9]+)', lab_link)
                if match:
                    test_id = match.group(1)
        except Exception as e:
            print(f"[DEBUG] Failed to load lab_data.json: {e}")

    # Always call fetch_test_questions and update dat.json if possible
    api_success = False
    if jwt_token and test_id:
        try:
            tests_data = fetch_test_questions(test_id, jwt_token)
            if tests_data and tests_data.get('data', {}).get('_id') == test_id:
                with open('dat.json', 'w', encoding='utf-8') as f:
                    json.dump(tests_data, f, ensure_ascii=False, indent=2)
                questions = tests_data.get('data', {}).get('questions', [])
                api_success = True
        except Exception as e:
            print(f"[DEBUG] API call failed: {e}")

    # If API did not succeed, load from dat.json (like practice window)
    if not api_success and os.path.exists('dat.json'):
        try:
            with open('dat.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            questions = data.get('data', {}).get('questions', [])
        except Exception as e:
            print(f"[DEBUG] Failed to load dat.json: {e}")

    # fallback: if no questions, use the current practice as the only question
    if not questions:
        questions = [{
            'title': practice.get('title', 'No Title'),
            'description': practice.get('description', 'No question/description available.')
        }]

    # UI widgets for question display and navigation
    question_label = tk.Label(editor_win, text='', font=("Arial", 13, "bold"), wraplength=750, justify='left')
    question_label.pack(pady=5)
    question_text = tk.Text(editor_win, height=14, wrap='word', font=("Arial", 11))
    question_text.pack(pady=5, fill='x')
    question_text.config(state='disabled')

    nav_frame = tk.Frame(editor_win)
    nav_frame.pack(pady=2)
    prev_btn = tk.Button(nav_frame, text="Previous", width=10)
    next_btn = tk.Button(nav_frame, text="Next", width=10)
    page_label = tk.Label(nav_frame, text="")
    prev_btn.grid(row=0, column=0, padx=5)
    page_label.grid(row=0, column=1, padx=5)
    next_btn.grid(row=0, column=2, padx=5)

    def show_question(idx):
        q = questions[idx]
        title = q.get('title', 'No Title')
        desc = q.get('description', 'No question/description available.')
        formatted = desc.replace('####', '\n').replace('**', '').replace('\r\n', '\n').replace('\n', '\n')
        # Add public test cases display
        public_cases = []
        code_options = q.get('codeOptions', {})
        test_cases = code_options.get('testCases', [])
        for tc in test_cases:
            if tc.get('visibility') == 'public':
                inp = tc.get('input', '').strip()
                out = tc.get('output', '').strip()
                public_cases.append(f"Input:\n{inp}\nOutput:\n{out if out else '[No output provided]'}")
        if public_cases:
            formatted += '\n\n--- Public Test Cases ---\n' + '\n\n'.join(public_cases)
        question_label.config(text=f"Q{idx+1}. {title}")
        question_text.config(state='normal')
        question_text.delete('1.0', tk.END)
        question_text.insert(tk.END, formatted)
        question_text.config(state='disabled')
        page_label.config(text=f"Question {idx+1} of {len(questions)}")
        prev_btn.config(state='normal' if idx > 0 else 'disabled')
        next_btn.config(state='normal' if idx < len(questions)-1 else 'disabled')

    def goto_prev():
        if current_index[0] > 0:
            current_index[0] -= 1
            show_question(current_index[0])

    def goto_next():
        if current_index[0] < len(questions)-1:
            current_index[0] += 1
            show_question(current_index[0])

    prev_btn.config(command=goto_prev)
    next_btn.config(command=goto_next)

    # Copy current question
    def copy_question():
        q = questions[current_index[0]]
        desc = q.get('description', 'No question/description available.')
        formatted = desc.replace('####', '\n').replace('**', '').replace('\r\n', '\n').replace('\n', '\n')
        # Add public test cases display
        public_cases = []
        code_options = q.get('codeOptions', {})
        test_cases = code_options.get('testCases', [])
        for tc in test_cases:
            if tc.get('visibility') == 'public':
                inp = tc.get('input', '').strip()
                out = tc.get('output', '').strip()
                public_cases.append(f"Input:\n{inp}\nOutput:\n{out if out else '[No output provided]'}")
        if public_cases:
            formatted += '\n\n--- Public Test Cases ---\n' + '\n\n'.join(public_cases)
        editor_win.clipboard_clear()
        editor_win.clipboard_append(formatted)
        editor_win.update()
        tk.messagebox.showinfo("Copied", "Question and public test cases copied to clipboard!")

    copy_btn = tk.Button(editor_win, text="Copy Question", command=copy_question)
    copy_btn.pack(pady=2)

    # Show the initial question
    show_question(current_index[0])

    # Language selection dropdown
    lang_frame = tk.Frame(editor_win)
    lang_frame.pack(pady=2)
    lang_label = tk.Label(lang_frame, text="Select Language:", font=("Arial", 11))
    lang_label.pack(side='left', padx=5)
    language_var = tk.StringVar(value="cpp")
    lang_options = ["cpp", "java", "python", "sql"]
    lang_dropdown = tk.OptionMenu(lang_frame, language_var, *lang_options)
    lang_dropdown.pack(side='left', padx=5)

    code_label = tk.Label(editor_win, text="Your Code:", font=("Arial", 11))
    code_label.pack(pady=2)
    code_text = tk.Text(editor_win, height=12, wrap='none')
    code_text.pack(pady=5, fill='both', expand=True)

    result_label = tk.Label(editor_win, text="", font=("Arial", 11, "bold"))
    result_label.pack(pady=5)

    from .api_client import submit_test_solution
    def submit_code():
        code = code_text.get("1.0", tk.END).strip()
        if not code:
            result_label.config(text="Please enter your code.", fg="orange")
            return

        # Use test_id from the outer scope (already set above)
        test_id=test_id_value
        submission_id = None
        language = language_var.get()  # Get selected language from dropdown
        if os.path.exists('lab_data.json'):
            try:
                with open('lab_data.json', 'r', encoding='utf-8') as labf:
                    lab_data = json.load(labf)
                    lab_link = lab_data.get('link', '')
                    match = re.search(r'/test/([a-zA-Z0-9]+)', lab_link)
                    if match:
                        test_id = match.group(1)
            except Exception as e:
                print(f"[DEBUG] Failed to load lab_data.json: {e}")

        # Try to get submission_id from the currently selected question
        if os.path.exists('dat.json'):
            try:
                with open('dat.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    questions_list = data.get('data', {}).get('questions', [])
                    if questions_list and isinstance(questions_list, list):
                        # Use the current_index[0] to pick the selected question
                        selected_idx = current_index[0]
                        if 0 <= selected_idx < len(questions_list):
                            submission_id = questions_list[selected_idx].get('_id', None)
                    if not submission_id:
                        # fallback to test _id if present
                        submission_id = data.get('data', {}).get('_id', None)
            except Exception as e:
                print(f"[DEBUG] Failed to load dat.json: {e}")
        if not submission_id:
            submission_id = "43qqzzsz4"  # fallback static id

        if not test_id or not submission_id:
            result_label.config(text="Missing test_id or submission_id.", fg="red")
            return

        # Call the real API
        result_label.config(text="Submitting...", fg="blue")
        response = submit_test_solution(test_id, submission_id, jwt_token, language, code)
        if response:
            result_label.config(text="Submission successful!", fg="green")
            # Show popup with test case results
            test_case_results = response.get('data', {}).get('testCaseVsResult', {})
            total = len(test_case_results)
            passed = sum(1 for v in test_case_results.values() if v)
            failed = total - passed
            import tkinter.messagebox as messagebox
            messagebox.showinfo(
                "Test Case Results",
                f"Total Test Cases: {total}\nPassed: {passed}\nFailed: {failed}"
            )
        else:
            result_label.config(text="Submission failed.", fg="red")

    submit_btn = tk.Button(editor_win, text="Submit", command=submit_code)
    submit_btn.pack(pady=5)
