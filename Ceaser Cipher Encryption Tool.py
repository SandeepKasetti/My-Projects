import tkinter as tk
from tkinter import messagebox, scrolledtext

def caesar_cipher_encrypt(message, shift):
    """
    Encrypt a message using Caesar cipher algorithm.
    
    Args:
    message (str): The text to be encrypted
    shift (int): Number of positions to shift letters
    
    Returns:
    str: Encrypted message
    """
    encrypted_message = ""
    
    for char in message:
        if char.isalpha():
            # Determine the case (upper or lower)
            is_upper = char.isupper()
            
            # Convert to 0-25 range
            char_code = ord(char.lower()) - ord('a')
            
            # Apply shift and wrap around the alphabet
            shifted_code = (char_code + shift) % 26
            
            # Convert back to character
            new_char = chr(shifted_code + ord('a'))
            
            # Restore original case
            if is_upper:
                new_char = new_char.upper()
            
            encrypted_message += new_char
        else:
            # Non-alphabetic characters remain unchanged
            encrypted_message += char
    
    return encrypted_message

def caesar_cipher_decrypt(encrypted_message, shift):
    """
    Decrypt a message using Caesar cipher algorithm.
    
    Args:
    encrypted_message (str): The text to be decrypted
    shift (int): Number of positions to shift letters back
    
    Returns:
    str: Decrypted message
    """
    # Decryption is just encryption with negative shift
    return caesar_cipher_encrypt(encrypted_message, -shift)

def encrypt_text():
    """
    Encrypt the input text using the selected shift value
    """
    # Get input text and remove any leading/trailing whitespace
    text = input_text.get("1.0", tk.END).strip()
    
    # Validate input
    if not text:
        messagebox.showwarning("Warning", "Please enter text to encrypt.")
        return
    
    try:
        # Get shift value
        shift = int(shift_var.get())
        
        # Perform encryption
        encrypted_text = caesar_cipher_encrypt(text, shift)
        
        # Clear previous output and display encrypted text
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, encrypted_text)
        output_text.config(state=tk.DISABLED)
        
        # Show success message
        messagebox.showinfo("Encryption", "Text encrypted successfully!")
    
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid shift value (integer).")

def decrypt_text():
    """
    Decrypt the input text using the selected shift value
    """
    # Get input text and remove any leading/trailing whitespace
    text = input_text.get("1.0", tk.END).strip()
    
    # Validate input
    if not text:
        messagebox.showwarning("Warning", "Please enter text to decrypt.")
        return
    
    try:
        # Get shift value
        shift = int(shift_var.get())
        
        # Perform decryption
        decrypted_text = caesar_cipher_decrypt(text, shift)
        
        # Clear previous output and display decrypted text
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, decrypted_text)
        output_text.config(state=tk.DISABLED)
        
        # Show success message
        messagebox.showinfo("Decryption", "Text decrypted successfully!")
    
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid shift value (integer).")

# Create main window
root = tk.Tk()
root.title("Caesar Cipher Encryption/Decryption")
root.geometry("600x500")

# Input Text Label and Textbox
tk.Label(root, text="Enter Text:", font=("Arial", 12)).pack(pady=(10, 5))
input_text = scrolledtext.ScrolledText(root, height=5, width=70, wrap=tk.WORD)
input_text.pack(padx=10, pady=5)

# Shift Value Label and Entry
tk.Label(root, text="Shift Value (1-25):", font=("Arial", 12)).pack(pady=(10, 5))
shift_var = tk.StringVar(value="3")  # Default shift value
shift_entry = tk.Entry(root, textvariable=shift_var, font=("Arial", 12), width=10)
shift_entry.pack(pady=5)

# Encryption and Decryption Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Encrypt", command=encrypt_text, 
          font=("Arial", 12), bg="lightblue", width=10).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Decrypt", command=decrypt_text, 
          font=("Arial", 12), bg="lightgreen", width=10).pack(side=tk.LEFT, padx=5)

# Output Text Label and Textbox
tk.Label(root, text="Result:", font=("Arial", 12)).pack(pady=(10, 5))
output_text = scrolledtext.ScrolledText(root, height=5, width=70, wrap=tk.WORD, state=tk.DISABLED)
output_text.pack(padx=10, pady=5)

# Start the GUI event loop
root.mainloop()
