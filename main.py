import os
import tarfile
import tkinter as tk
from tkinter import simpledialog, scrolledtext
import sys

class ShellEmulator:
    def __init__(self, user_name, host_name, vfs_path):
        self.user_name = user_name
        self.host_name = host_name
        self.current_dir = 'vfs/'  # Start in the vfs directory
        # Open the tar file and store it as an attribute
        self.tar = tarfile.open(vfs_path, "r")
        self.file_system = self.load_vfs()

    def load_vfs(self):
        """Load virtual file system from the tar archive."""
        fs = {}
        for member in self.tar.getmembers():
            fs[member.name] = member
        return fs

    def prompt(self):
        """Return the shell prompt."""
        return f"{self.user_name}@{self.host_name}:{self.current_dir}$ "

    def execute_command(self, command):
        """Parse and execute the entered shell command."""
        parts = command.strip().split()
        if not parts:
            return ""
        cmd, *args = parts

        if cmd == "ls":
            return self.ls()
        elif cmd == "cd":
            return self.cd(args[0] if args else "/")
        elif cmd == "head":
            return self.head(args[0] if args else "")
        elif cmd == "wc":
            return self.wc(args[0] if args else "")
        elif cmd == "exit":
            self.exit_emulator()
        else:
            return f"Command not found: {cmd}"

    def ls(self):
        """List directory contents."""
        contents = []
        if not self.current_dir.endswith('/'):
            self.current_dir += '/'

        for name in self.file_system:
            if name.startswith(self.current_dir) and name != self.current_dir:
                relative_path = name[len(self.current_dir):].strip('/')
                if '/' not in relative_path:
                    contents.append(relative_path)

        return "\n".join(contents) if contents else "Empty directory"

    def cd(self, path):
        """Change directory."""
        if path == '/':
            self.current_dir = 'vfs/'
        else:
            # Ensure new path ends with '/'
            if not path.endswith('/'):
                path += '/'
            
            # Construct the full path from the current directory
            new_path = self.current_dir + path
            
            # Check if the new path exists and is a directory
            if any(name.startswith(new_path) for name in self.file_system.keys()):
                self.current_dir = new_path
            else:
                return f"No such directory: {path.strip('/')}"
        
        return ""

    def head(self, file_name):
        """Display the first few lines of a file."""
        # Ensure the file path is relative to the current directory
        if not self.current_dir.endswith('/'):
            self.current_dir += '/'
        full_path = self.current_dir + file_name
        
        # Debugging: Show the full path being checked
        print(f"Full path: {full_path}")
        print(f"Available files: {list(self.file_system.keys())}")
        
        # Check if the file exists in the virtual file system
        if full_path not in self.file_system:
            return f"No such file: {file_name}"
        
        member = self.file_system[full_path]
        if not member.isfile():
            return f"{file_name} is not a file."
        
        # Extract the file contents
        f = self.tar.extractfile(member)
        if f is None:
            return f"Could not extract: {file_name}"
        
        content = f.read(100).decode('utf-8')
        return content


    def wc(self, file_name):
        """Word count of the file."""
        # Ensure the file path is relative to the current directory
        if not self.current_dir.endswith('/'):
            self.current_dir += '/'
        full_path = self.current_dir + file_name
        
        # Debugging: Show the full path being checked
        print(f"Full path: {full_path}")
        print(f"Available files: {list(self.file_system.keys())}")
        
        # Check if the file exists in the virtual file system
        if full_path not in self.file_system:
            return f"No such file: {file_name}"
        
        member = self.file_system[full_path]
        
        # Check if the member is a file
        if not member.isfile():
            return f"{file_name} is not a file."
        
        # Extract the file contents
        try:
            f = self.tar.extractfile(member)
            if f is None:
                return f"Could not extract: {file_name}"
            content = f.read().decode('utf-8')
        except Exception as e:
            return f"Error extracting file: {e}"
        
        # Perform word count, line count, and character count
        lines = len(content.splitlines())
        words = len(content.split())
        chars = len(content)
        
        return f"{lines} {words} {chars} {file_name}"


    def exit_emulator(self):
        """Exit the shell emulator."""
        root.quit()

class ShellGUI(tk.Frame):
    def __init__(self, emulator, master=None):
        super().__init__(master)
        self.master = master
        self.emulator = emulator
        self.create_widgets()

    def create_widgets(self):
        """Create the GUI layout."""
        self.output = scrolledtext.ScrolledText(self.master, wrap=tk.WORD)
        self.output.pack(fill=tk.BOTH, expand=True)

        self.command_entry = tk.Entry(self.master)
        self.command_entry.pack(fill=tk.X, side=tk.BOTTOM)
        self.command_entry.bind("<Return>", self.run_command)

        self.display_output(self.emulator.prompt())

    def display_output(self, text):
        """Display text in the output area."""
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def run_command(self, event):
        """Handle command execution."""
        command = self.command_entry.get()
        self.command_entry.delete(0, tk.END)
        self.display_output(command)

        output = self.emulator.execute_command(command)
        self.display_output(output)
        self.display_output(self.emulator.prompt())

def main():
    """Entry point for the shell emulator."""
    if len(sys.argv) != 4:
        print("Usage: shell_emulator.py <username> <hostname> <path_to_tar>")
        sys.exit(1)

    user_name = sys.argv[1]
    host_name = sys.argv[2]
    vfs_path = sys.argv[3]

    emulator = ShellEmulator(user_name, host_name, vfs_path)

    # Launch GUI
    global root
    root = tk.Tk()
    root.title("Shell Emulator")
    app = ShellGUI(emulator, master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
