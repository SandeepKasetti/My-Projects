import tkinter as tk
from tkinter import messagebox, scrolledtext
import keyboard
import logging
from datetime import datetime
import os

class EthicalKeyLogger:
    def __init__(self, root):
        self.root = root
        self.root.title("Ethical Keylogger")
        self.root.geometry("600x500")

        # Logging configuration
        self.log_file = os.path.join(os.getcwd(), f"keylog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        logging.basicConfig(filename=self.log_file, 
                            level=logging.INFO, 
                            format='%(asctime)s: %(message)s')

        # Tracking variables
        self.is_logging = False
        self.total_keystrokes = 0

        # Create GUI
        self.create_widgets()

    def create_widgets(self):
        # Status Label
        self.status_label = tk.Label(self.root, text="Keylogger is Stopped", 
                                     font=("Arial", 12), fg="red")
        self.status_label.pack(pady=10)

        # Keystroke Count
        self.keystroke_label = tk.Label(self.root, text="Total Keystrokes: 0", 
                                        font=("Arial", 12))
        self.keystroke_label.pack(pady=5)

        # Log Display
        tk.Label(self.root, text="Log Preview:", font=("Arial", 12)).pack(pady=5)
        self.log_display = scrolledtext.ScrolledText(self.root, 
                                                     height=10, 
                                                     width=70, 
                                                     wrap=tk.WORD)
        self.log_display.pack(pady=10)
        self.log_display.config(state=tk.DISABLED)

        # Control Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Start Logging", 
                  command=self.start_logging, 
                  bg="lightgreen").pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Stop Logging", 
                  command=self.stop_logging, 
                  bg="lightcoral").pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="View Log File", 
                  command=self.view_log_file, 
                  bg="lightskyblue").pack(side=tk.LEFT, padx=5)

    def on_key_event(self, event):
        """Handle key press events"""
        try:
            # Log the key
            if len(event.name) == 1:
                logging.info(f"Key Pressed: {event.name}")
            else:
                logging.info(f"Special Key: {event.name}")

            # Update keystroke count
            self.total_keystrokes += 1
            self.keystroke_label.config(text=f"Total Keystrokes: {self.total_keystrokes}")

            # Update log preview (limit to last 10 entries)
            self.log_display.config(state=tk.NORMAL)
            current_log = self.log_display.get("1.0", tk.END).strip().split('\n')
            if len(current_log) > 10:
                current_log = current_log[-10:]
            current_log.append(f"{datetime.now().strftime('%H:%M:%S')}: {event.name}")
            self.log_display.delete("1.0", tk.END)
            self.log_display.insert(tk.END, '\n'.join(current_log))
            self.log_display.config(state=tk.DISABLED)

        except Exception as e:
            logging.error(f"Error logging key: {e}")

    def start_logging(self):
        """Start key logging"""
        if not self.is_logging:
            # Confirm ethical use
            response = messagebox.askyesno(
                "Ethical Use Confirmation", 
                "Do you have explicit permission to log keystrokes?"
            )
            
            if response:
                keyboard.on_press(self.on_key_event)
                self.is_logging = True
                self.status_label.config(text="Keylogger is Running", fg="green")
                messagebox.showinfo("Started", "Keylogging has begun.")
            else:
                messagebox.showwarning("Stopped", "Keylogging cancelled.")

    def stop_logging(self):
        """Stop key logging"""
        if self.is_logging:
            keyboard.unhook_all()
            self.is_logging = False
            self.status_label.config(text="Keylogger is Stopped", fg="red")
            messagebox.showinfo("Stopped", f"Keylogging stopped. Log saved to {self.log_file}")

    def view_log_file(self):
        """Open the log file"""
        try:
            os.startfile(self.log_file)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open log file: {e}")

def main():
    root = tk.Tk()
    app = EthicalKeyLogger(root)
    root.mainloop()

if __name__ == "__main__":
    main()
