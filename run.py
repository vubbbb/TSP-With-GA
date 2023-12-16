import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import chardet

class TSPApp:
    def __init__(self, master):
        self.master = master
        self.master.title("TSP Configuration")


        self.ct_label = ttk.Label(master, text="Number of Cities (CT):")
        self.ct_label.grid(row=0, column=0, padx=10, pady=5)
        self.ct_entry = ttk.Entry(master)
        self.ct_entry.grid(row=0, column=1, padx=10, pady=5)

        self.max_gen_label = ttk.Label(master, text="Max Generations:")
        self.max_gen_label.grid(row=1, column=0, padx=10, pady=5)
        self.max_gen_entry = ttk.Entry(master)
        self.max_gen_entry.grid(row=1, column=1, padx=10, pady=5)

        # self.max_gen_label = ttk.Label(master, text="Max Generations:")
        # self.max_gen_label.grid(row=2, column=0, padx=10, pady=5)
        # self.max_gen_entry = ttk.Entry(master)
        # self.max_gen_entry.grid(row=2, column=1, padx=10, pady=5)

        self.run_button = ttk.Button(master, text="Run", command=self.run_main)
        self.run_button.grid(row=2, column=0, columnspan=2, pady=10)

    def run_main(self):
        try:
            ct_value = int(self.ct_entry.get().strip())
            max_gen_value = int(self.max_gen_entry.get().strip())

            if ct_value <= 0:
                raise ValueError("Values must be positive integers.")
            
            elif max_gen_value <= 0 and max_gen_value != -1:
                raise ValueError("Values must be positive integers.")
            elif max_gen_value == -1:
                max_gen_value = 99999999999

            # Detect file encoding
            with open("main.py", "rb") as file:
                result = chardet.detect(file.read())

            file_encoding = result["encoding"]

            # Write the new values to the main.py file
            with open("main.py", "r", encoding=file_encoding, errors="replace") as file:
                lines = file.readlines()

            # Update the lines containing CT and max_generation
            for i in range(len(lines)):
                if "CT =" in lines[i]:
                    lines[i] = f"CT = {ct_value}\n"
                elif "max_generation =" in lines[i]:
                    lines[i] = f"max_generation = {max_gen_value}\n"

            # Write the updated lines back to the file
            with open("main.py", "w", encoding=file_encoding, errors="replace") as file:
                file.writelines(lines)

            # Run the main.py file
            # subprocess.run(["python", "main.py"])
            subprocess.run(["python", "main.py"])

        except ValueError as e:
            messagebox.showerror("Error", str(e))



if __name__ == "__main__":
    root = tk.Tk()
    app = TSPApp(root)
    root.mainloop()

