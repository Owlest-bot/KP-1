import os
import zipfile
import yaml
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import scrolledtext

class ShellEmulator:
    def __init__(self, config_path):
        self.load_config(config_path)
        self.current_directory = "/"
        self.load_vfs()
        self.create_log_file()

    def load_config(self, config_path):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        self.username = config['username']
        self.vfs_zip_path = config['vfs_zip_path']
        self.log_file_path = config['log_file_path']

    def load_vfs(self):
        self.vfs_temp_path = "/tmp/vfs"
        if not os.path.exists(self.vfs_temp_path):
            os.makedirs(self.vfs_temp_path)
        with zipfile.ZipFile(self.vfs_zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.vfs_temp_path)

    def create_log_file(self):
        self.log_tree = ET.Element("log")

    def log_action(self, action):
        entry = ET.SubElement(self.log_tree, "action")
        entry.text = action
        entry.set("user", self.username)

    def ls(self):
        files = os.listdir(self.vfs_temp_path + self.current_directory)
        self.log_action(f"ls in {self.current_directory}")
        return "\n".join(files)

    def cd(self, directory):
        new_path = os.path.join(self.vfs_temp_path + self.current_directory, directory)
        if os.path.isdir(new_path):
            self.current_directory += directory + "/"
            self.log_action(f"cd to {self.current_directory}")
            return f"Changed directory to {self.current_directory}"
        else:
            return "No such directory"

    def rm(self, filename):
        try:
            os.remove(os.path.join(self.vfs_temp_path + self.current_directory, filename))
            self.log_action(f"removed {filename}")
            return f"Removed {filename}"
        except FileNotFoundError:
            return "File not found"

    def find(self, filename):
        for root, dirs, files in os.walk(self.vfs_temp_path):
            if filename in files:
                self.log_action(f"found {filename} in {root}")
                return os.path.join(root, filename)
        return "File not found"

    def exit(self):
        tree = ET.ElementTree(self.log_tree)
        tree.write(self.log_file_path)

class ShellGUI:
    def __init__(self, emulator):
        self.emulator = emulator
        self.root = tk.Tk()
        self.root.title("Shell Emulator")
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.entry = tk.Entry(self.root)
        self.entry.pack(padx=10, pady=5, fill=tk.X)
        self.entry.bind("<Return>", self.process_command)
        self.root.mainloop()

    def process_command(self, event):
        command = self.entry.get()
        self.entry.delete(0, tk.END)
        result = ""
        if command.startswith("ls"):
            result = self.emulator.ls()
        elif command.startswith("cd"):
            _, dir_name = command.split()
            result = self.emulator.cd(dir_name)
        elif command.startswith("rm"):
            _, file_name = command.split()
            result = self.emulator.rm(file_name)
        elif command.startswith("find"):
            _, file_name = command.split()
            result = self.emulator.find(file_name)
        elif command == "exit":
            self.emulator.exit()
            self.root.quit()
            return
        else:
            result = "Unknown command"
        self.text_area.insert(tk.END, f"{self.emulator.username}@shell: {command}\n{result}\n")

if __name__ == "__main__":
    emulator = ShellEmulator("config.yaml")
    gui = ShellGUI(emulator)