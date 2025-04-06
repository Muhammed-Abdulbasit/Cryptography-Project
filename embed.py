from PIL import Image
import hashlib
import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

def encrypt_message(message, password):
    """Encrypt the message using AES-256 with the provided password."""
    # Create a key from the password
    key = hashlib.sha256(password.encode()).digest()
    
    # Generate a random IV (Initialization Vector)
    iv = os.urandom(16)
    
    # Create a cipher with the key and IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Pad the message to make its length a multiple of the block size
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()
    
    # Encrypt the padded message
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    # Combine IV and encrypted data
    result = iv + encrypted_data
    
    # Calculate checksum (SHA-256) for integrity verification
    checksum = hashlib.sha256(result).digest()
    
    # Combine checksum with encrypted data and return as base64
    final_data = checksum + result
    return base64.b64encode(final_data).decode()

def text_to_binary(text):
    """Convert text to binary."""
    binary = ''.join(format(ord(c), '08b') for c in text)
    # Add a delimiter (8 zeros) to mark the end of the message
    binary += '00000000'
    return binary

def encode_image(message, password, image_path, output_path="encoded_image.png"):
    """Encode encrypted message into an image."""
    # Encrypt the message first
    encrypted_message = encrypt_message(message, password)
    
    # Open the image
    img = Image.open(image_path)
    
    # Convert image to RGB if not already
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Get pixel data
    pixels = list(img.getdata())
    
    # Convert encrypted text to binary
    binary_text = text_to_binary(encrypted_message)
    
    if len(binary_text) > len(pixels) * 3:
        return "Error: Message too large for the image"
    
    # Clear the entire image's LSBs first to remove any old messages
    cleared_pixels = []
    for pixel in pixels:
        r, g, b = pixel
        # Clear the LSB of each channel
        cleared_r = r & ~1
        cleared_g = g & ~1
        cleared_b = b & ~1
        cleared_pixels.append((cleared_r, cleared_g, cleared_b))
    
    # Now embed the binary data into the image
    new_pixels = []
    binary_index = 0
    
    for pixel in cleared_pixels:
        # Once we've embedded all the data, just add the remaining pixels unchanged
        if binary_index >= len(binary_text):
            new_pixels.append(pixel)
            continue
        
        r, g, b = pixel
        new_r, new_g, new_b = r, g, b
        
        # Modify least significant bits based on the binary message
        if binary_index < len(binary_text):
            new_r = r | int(binary_text[binary_index])  # LSB already cleared
            binary_index += 1
        
        if binary_index < len(binary_text):
            new_g = g | int(binary_text[binary_index])  # LSB already cleared
            binary_index += 1
        
        if binary_index < len(binary_text):
            new_b = b | int(binary_text[binary_index])  # LSB already cleared
            binary_index += 1
        
        new_pixels.append((new_r, new_g, new_b))
    
    # Create a new image with the modified pixels
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_pixels)
    
    # Save the new image
    new_img.save(output_path, "PNG")
    
    return f"Message successfully encrypted and embedded in {output_path}"

if __name__ == '__main__':
    message = input("Enter the secret message to hide: ")
    password = input("Enter the encryption password: ")
    image_path = input("Enter the path to the original image: ")
    output_path = input("Enter the output image path (default: encoded_image.png): ") or "encoded_image.png"
    print(encode_image(message, password, image_path, output_path))