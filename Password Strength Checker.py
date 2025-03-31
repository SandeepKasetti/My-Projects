import tkinter as tk
import re

class PasswordStrengthChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Checker")
        self.root.geometry("500x400")
        
        # Create GUI components
        self.create_widgets()
    
    def create_widgets(self):
        # Password Input
        tk.Label(self.root, text="Enter Password:", font=("Arial", 12)).pack(pady=(20, 5))
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 12), width=30)
        self.password_entry.pack(pady=5)
        
        # Show/Hide Password Checkbox
        self.show_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.root, text="Show Password", 
                       variable=self.show_var, 
                       command=self.toggle_password_visibility).pack(pady=5)
        
        # Check Strength Button
        tk.Button(self.root, text="Check Strength", 
                  command=self.check_password_strength, 
                  font=("Arial", 12), 
                  bg="lightblue").pack(pady=10)
        
        # Strength Indicator
        self.strength_label = tk.Label(self.root, text="", font=("Arial", 12, "bold"))
        self.strength_label.pack(pady=10)
        
        # Detailed Feedback
        self.feedback_text = tk.Text(self.root, height=10, width=50, wrap=tk.WORD)
        self.feedback_text.pack(pady=10)
        self.feedback_text.config(state=tk.DISABLED)
    
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    def check_password_strength(self):
        """Assess password strength and provide feedback"""
        password = self.password_entry.get()
        
        # Reset previous feedback
        self.feedback_text.config(state=tk.NORMAL)
        self.feedback_text.delete('1.0', tk.END)
        
        # Strength criteria checks
        length = len(password)
        has_uppercase = bool(re.search(r'[A-Z]', password))
        has_lowercase = bool(re.search(r'[a-z]', password))
        has_number = bool(re.search(r'\d', password))
        has_special_char = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        
        # Calculate strength score
        score = 0
        feedback_lines = []
        
        # Length criteria
        if length < 8:
            feedback_lines.append("❌ Password is too short (minimum 8 characters)")
            score += length
        elif length < 12:
            feedback_lines.append("⚠️ Consider making password longer")
            score += length
        else:
            feedback_lines.append("✅ Good password length")
            score += 20
        
        # Character type checks
        if not has_uppercase:
            feedback_lines.append("❌ Add at least one uppercase letter")
        else:
            score += 20
        
        if not has_lowercase:
            feedback_lines.append("❌ Add at least one lowercase letter")
        else:
            score += 20
        
        if not has_number:
            feedback_lines.append("❌ Include at least one number")
        else:
            score += 20
        
        if not has_special_char:
            feedback_lines.append("❌ Include at least one special character")
        else:
            score += 20
        
        # Determine strength
        if score < 20:
            strength = "Very Weak"
            color = "red"
        elif score < 40:
            strength = "Weak"
            color = "orange"
        elif score < 60:
            strength = "Moderate"
            color = "yellow"
        elif score < 80:
            strength = "Strong"
            color = "green"
        else:
            strength = "Very Strong"
            color = "dark green"
        
        # Display strength and feedback
        self.strength_label.config(text=f"Strength: {strength}", fg=color)
        
        # Add feedback to text widget
        for line in feedback_lines:
            self.feedback_text.insert(tk.END, line + "\n")
        
        self.feedback_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = PasswordStrengthChecker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
