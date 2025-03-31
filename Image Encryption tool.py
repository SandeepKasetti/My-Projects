import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

class ImageEncryptionTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryption Tool")
        self.root.geometry("500x400")

        # Key for encryption/decryption
        self.encryption_key = 123

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Input Image Selection
        tk.Button(self.root, text="Select Image", command=self.select_image, 
                  font=("Arial", 12), bg="lightblue").pack(pady=10)

        # Encryption Method Selection
        tk.Label(self.root, text="Select Encryption Method:", 
                 font=("Arial", 12)).pack(pady=5)
        
        self.method_var = tk.StringVar(value="Pixel Swap")
        methods = ["Pixel Swap", "Mathematical Operation"]
        for method in methods:
            tk.Radiobutton(self.root, text=method, variable=self.method_var, 
                           value=method, font=("Arial", 10)).pack(anchor="w", padx=50)

        # Encryption Buttons
        tk.Button(self.root, text="Encrypt Image", command=self.encrypt_image, 
                  font=("Arial", 12), bg="lightgreen").pack(pady=10)
        
        tk.Button(self.root, text="Decrypt Image", command=self.decrypt_image, 
                  font=("Arial", 12), bg="lightyellow").pack(pady=10)

    def select_image(self):
        """Open file dialog to select an image"""
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff")]
        )
        if self.image_path:
            messagebox.showinfo("Image Selected", f"Image loaded: {self.image_path}")

    def encrypt_image(self):
        """Encrypt the selected image"""
        try:
            # Read the image
            image = cv2.imread(self.image_path)
            
            if image is None:
                messagebox.showerror("Error", "Could not read the image.")
                return

            # Choose encryption method
            if self.method_var.get() == "Pixel Swap":
                encrypted_image = self.pixel_swap_encryption(image)
            else:
                encrypted_image = self.mathematical_encryption(image)

            # Save encrypted image
            output_path = self.image_path.rsplit('.', 1)[0] + '_encrypted.png'
            cv2.imwrite(output_path, encrypted_image)
            
            messagebox.showinfo("Success", f"Image encrypted and saved to {output_path}")

        except Exception as e:
            messagebox.showerror("Encryption Error", str(e))

    def decrypt_image(self):
        """Decrypt the selected image"""
        try:
            # Read the image
            image = cv2.imread(self.image_path)
            
            if image is None:
                messagebox.showerror("Error", "Could not read the image.")
                return

            # Choose decryption method (reverse of encryption)
            if self.method_var.get() == "Pixel Swap":
                decrypted_image = self.pixel_swap_decryption(image)
            else:
                decrypted_image = self.mathematical_decryption(image)

            # Save decrypted image
            output_path = self.image_path.rsplit('.', 1)[0] + '_decrypted.png'
            cv2.imwrite(output_path, decrypted_image)
            
            messagebox.showinfo("Success", f"Image decrypted and saved to {output_path}")

        except Exception as e:
            messagebox.showerror("Decryption Error", str(e))

    def pixel_swap_encryption(self, image):
        """Encrypt image by swapping pixel values"""
        encrypted = image.copy()
        height, width = image.shape[:2]
        
        # Swap pixels based on a pattern
        for y in range(0, height, 2):
            for x in range(0, width, 2):
                # Swap adjacent pixels
                if x + 1 < width and y + 1 < height:
                    encrypted[y, x], encrypted[y, x+1] = encrypted[y, x+1], encrypted[y, x]
                    encrypted[y, x+1], encrypted[y+1, x+1] = encrypted[y+1, x+1], encrypted[y, x+1]
        
        return encrypted

    def pixel_swap_decryption(self, image):
        """Decrypt image by reversing pixel swap"""
        return self.pixel_swap_encryption(image)  # Swap is symmetric

    def mathematical_encryption(self, image):
        """Encrypt image using mathematical operation"""
        encrypted = image.copy().astype(np.float32)
        
        # Apply mathematical transformation
        encrypted = (encrypted * self.encryption_key) % 256
        
        return encrypted.astype(np.uint8)

    def mathematical_decryption(self, image):
        """Decrypt image using inverse mathematical operation"""
        decrypted = image.copy().astype(np.float32)
        
        # Reverse the mathematical transformation
        decrypted = (decrypted * pow(self.encryption_key, -1, 256)) % 256
        
        return decrypted.astype(np.uint8)

def main():
    root = tk.Tk()
    app = ImageEncryptionTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()
