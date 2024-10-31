import random
import json
import tkinter as tk
from tkinter import messagebox, font
import time
import pandas as pd

# Expanded word pool for unique attribute names
word_pool = [
    "alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", "iota", "kappa",
    "lambda", "mu", "nu", "xi", "omicron", "pi", "rho", "sigma", "tau", "upsilon",
    "phi", "chi", "psi", "omega", "apple", "banana", "carrot", "date", "fig", "grape",
    "honeydew", "kiwi", "lemon", "mango", "nectarine", "orange", "papaya", "quince",
    "raspberry", "strawberry", "tangerine", "ugli", "vanilla", "watermelon", "xigua", "yam", "zucchini"
]

class JSONValue:
    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return self.value

class JSONObject:
    def __init__(self):
        self.fields = {}
        self.target_attribute = None
        self.correct_path = ""

    def parse(self, depth=2, available_keys=None, used_keys=None, used_values=None):
        if available_keys is None:
            available_keys = set(word_pool)
        if used_keys is None:
            used_keys = set()
        if used_values is None:
            used_values = set()

        num_fields = random.randint(1, 3)
        added_keys = 0

        while available_keys and added_keys < num_fields:
            name = random.choice(list(available_keys - used_keys))
            used_keys.add(name)
            available_keys.remove(name)
            added_keys += 1

            if depth > 1 and random.random() > 0.5:
                obj = JSONObject()
                obj.parse(depth - 1, available_keys, used_keys, used_values)
                self.fields[name] = obj
            else:
                possible_values = list((set(word_pool) - used_values) - {name})
                if possible_values:
                    value = random.choice(possible_values)
                    used_values.add(value)
                    self.fields[name] = JSONValue(value)

        self.set_random_target_attribute()

    def set_random_target_attribute(self):
        path = []
        current = self
        while isinstance(current, JSONObject) and current.fields:
            field_name = random.choice(list(current.fields.keys()))
            path.append(field_name)
            current = current.fields[field_name]

        self.correct_path = ".".join(path)
        self.target_attribute = current.value if isinstance(current, JSONValue) else None

    def to_dict(self):
        result = {}
        for name, value in self.fields.items():
            if isinstance(value, JSONObject):
                result[name] = value.to_dict()
            else:
                result[name] = value.to_dict()
        return result

    def get_all_keys(self):
        keys = set(self.fields.keys())
        for value in self.fields.values():
            if isinstance(value, JSONObject):
                keys.update(value.get_all_keys())
        return keys

    def verify_path(self, input_path):
        current = self
        for part in input_path.split("."):
            if isinstance(current, JSONObject) and part in current.fields:
                current = current.fields[part]
            else:
                return False
        return input_path == self.correct_path

    def format_json_unindented(self):
        def format_dict(d):
            lines = ["{"]
            for key, value in d.items():
                if isinstance(value, dict):
                    lines.append(f'"{key}":')
                    lines.append("{")
                    lines.extend(format_dict(value))
                    lines.append("}")
                else:
                    lines.append(f'"{key}": "{value}"')
            lines.append("}")
            return lines

        formatted_lines = format_dict(self.to_dict())
        return "\n".join(formatted_lines)

# GUI with Tkinter
class JSONPathExperimentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON Path Experiment")
        self.current_question = 1
        self.total_questions = 30  # 30 test cases
        self.json_object = None
        self.current_path = []
        self.indented_count = 15  # Track remaining indented cases
        self.non_indented_count = 15  # Track remaining non-indented cases
        self.custom_font = font.Font(family="Courier", size=10)

        # Time and attempt tracking
        self.start_time = None
        self.attempts = 0
        self.results = []

        self.setup_ui()
        self.setup_question()

    def setup_ui(self):
        # JSON Display Frame
        self.json_frame = tk.Frame(self.root)
        self.json_frame.pack(pady=10)

        # JSON Structure Text
        self.json_display = tk.Text(
            self.json_frame, height=20, width=80, wrap="word", font=self.custom_font
        )
        self.json_display.config(state="disabled")
        self.json_display.pack()

        # Target Attribute Display
        self.target_display_frame = tk.Frame(self.root)
        self.target_display_frame.pack(pady=10)
        self.target_display = tk.Label(
            self.target_display_frame,
            text="Target Attribute: ",
            font=("Arial", 12, "bold"),
        )
        self.target_display.pack()

        # Path Display Frame
        self.path_display_frame = tk.Frame(self.root)
        self.path_display_frame.pack(pady=10)
        self.path_display = tk.Label(
            self.path_display_frame, text="Current Path:", font=self.custom_font
        )
        self.path_display.pack()

        # Key Button Grid
        self.key_button_frame = tk.Frame(self.root)
        self.key_button_frame.pack(pady=10)

        # Action Buttons Frame
        self.action_frame = tk.Frame(self.root)
        self.action_frame.pack(pady=10)
        tk.Button(self.action_frame, text="Clear Path", command=self.clear_path).pack(
            side="left", padx=5
        )
        tk.Button(
            self.action_frame, text="Remove Last", command=self.remove_last_from_path
        ).pack(side="left", padx=5)
        tk.Button(
            self.action_frame, text="Submit Path", command=self.check_path
        ).pack(side="left", padx=5)

        # Entry for direct text input of path
        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack(pady=10)
        tk.Label(self.entry_frame, text="Enter Path: ").pack(side="left")
        self.entry_path = tk.Entry(self.entry_frame, width=50)
        self.entry_path.pack(side="left", padx=5)
        tk.Button(self.entry_frame, text="Submit", command=self.submit_entry_path).pack(side="left")

        # Bind Enter key to the check_path function
        self.root.bind("<Return>", lambda event: self.check_path())

    def setup_question(self):
        # Clear path and input field for the new question
        self.current_path = []
        self.entry_path.delete(0, tk.END)
        self.attempts = 0  # Reset attempts for each question
        self.start_time = time.time()  # Start time for the question
        available_keys = set(word_pool)
        self.json_object = JSONObject()
        self.json_object.parse(available_keys=available_keys)

        # Randomly choose between indented and non-indented, keeping a balanced count
        if self.indented_count > 0 and self.non_indented_count > 0:
            self.indented = random.choice([True, False])
        elif self.indented_count > 0:
            self.indented = True
        else:
            self.indented = False

        # Update the counts based on the choice
        if self.indented:
            self.indented_count -= 1
        else:
            self.non_indented_count -= 1

        # Display JSON Structure
        self.json_display.config(state="normal")
        self.json_display.delete("1.0", tk.END)
        json_structure = (
            json.dumps(self.json_object.to_dict(), indent=4)
            if self.indented
            else self.json_object.format_json_unindented()
        )
        self.json_display.insert(tk.END, json_structure)
        self.json_display.config(state="disabled")

        # Display Target Attribute
        target_text = f"Target Attribute: {self.json_object.target_attribute}"
        self.target_display.config(text=target_text)

        # Display Current Path
        self.update_path_display()

        # Show All Relevant Key Buttons
        self.show_all_key_buttons()

    def show_all_key_buttons(self):
        for widget in self.key_button_frame.winfo_children():
            widget.destroy()

        # Retrieve all unique keys used in the JSON structure
        json_keys = self.json_object.get_all_keys()
        columns = 6  # Number of columns for grid layout
        for i, key in enumerate(json_keys):
            button = tk.Button(
                self.key_button_frame,
                text=key,
                width=10,
                command=lambda k=key: self.add_to_path(k),
            )
            button.grid(row=i // columns, column=i % columns, padx=5, pady=5)

    def add_to_path(self, key):
        self.current_path.append(key)
        self.update_path_display()
        self.entry_path.delete(0, tk.END)  # Clear the entry field first
        self.entry_path.insert(0, ".".join(self.current_path))  # Update entry field with the current path

    def remove_last_from_path(self):
        if self.current_path:
            self.current_path.pop()
        self.update_path_display()
        self.entry_path.delete(0, tk.END)
        self.entry_path.insert(0, ".".join(self.current_path))

    def clear_path(self):
        self.current_path = []
        self.update_path_display()
        self.entry_path.delete(0, tk.END)

    def update_path_display(self):
        path_text = "Current Path: " + " > ".join(self.current_path)
        self.path_display.config(text=path_text)

    def submit_entry_path(self):
        # Submit path from the entry text field
        user_path = self.entry_path.get()
        self.verify_and_proceed(user_path)

    def check_path(self):
        # Verify current path created using buttons
        user_path = ".".join(self.current_path)
        self.verify_and_proceed(user_path)

    def verify_and_proceed(self, user_path):
        self.attempts += 1  # Increment attempt counter
        if self.json_object.verify_path(user_path):
            time_taken = time.time() - self.start_time  # Calculate time for the question
            # Save result for this question
            self.results.append({
                "Question": self.current_question,
                "Correct Path": self.json_object.correct_path,
                "User Path": user_path,
                "Attempts": self.attempts,
                "Time Taken (s)": time_taken
            })

            messagebox.showinfo("Correct", "Correct path! Moving to the next question...")
            if self.current_question < self.total_questions:
                self.current_question += 1
                self.setup_question()
            else:
                messagebox.showinfo("Experiment Complete", "Congratulations! You've completed all questions.")
                self.save_results_to_excel()  # Save data after all questions
                self.root.quit()
        else:
            messagebox.showwarning("Incorrect", "Incorrect path. Please try again.")
            self.clear_path()

    def save_results_to_excel(self):
        # Save the recorded data to an Excel file
        df = pd.DataFrame(self.results)
        df.to_excel("JSONPathExperimentResults.xlsx", index=False)
        messagebox.showinfo("Data Saved", "Results saved to JSONPathExperimentResults.xlsx")

# Initialize the app
if __name__ == "__main__":
    root = tk.Tk()
    app = JSONPathExperimentApp(root)
    root.mainloop()
