from PIL import Image
import hashlib
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.padding import PKCS7

def binary_to_text(binary):
    """Convert binary to text."""
    text = ""
    # Process 8 bits at a time (one character)
    for i in range(0, len(binary), 8):
        if i + 8 > len(binary):  # Ensure we have a full byte
            break
            
        byte = binary[i:i+8]
        # Check if we've reached the delimiter
        if byte == '00000000':
            break
        # Convert binary to character and add to text
        text += chr(int(byte, 2))
    return text

def decrypt_message(encrypted_base64, password):
    """Decrypt the message using AES-256 with the provided password."""
    try:
        # Decode from base64
        encrypted_data = base64.b64decode(encrypted_base64)
        
        # Extract checksum (first 32 bytes)
        original_checksum = encrypted_data[:32]
        data_with_iv = encrypted_data[32:]
        
        # Verify checksum
        calculated_checksum = hashlib.sha256(data_with_iv).digest()
        if calculated_checksum != original_checksum:
            return "Error: Message integrity check failed. The data may have been corrupted."
        
        # Extract IV (next 16 bytes) and ciphertext
        iv = data_with_iv[:16]
        ciphertext = data_with_iv[16:]
        
        # Create a key from the password
        key = hashlib.sha256(password.encode()).digest()
        
        # Create a cipher with the key and IV
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        
        # Decrypt the ciphertext
        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Unpad the decrypted data
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        unpadded_data = unpadder.update(decrypted_padded) + unpadder.finalize()
        
        # Return the decrypted message
        return unpadded_data.decode()
    except Exception as e:
        return f"Decryption error: {str(e)}. Make sure the password is correct."

def decode_image(image_path, password):
    """Extract hidden text from an image and decrypt it."""
    # Open the image
    img = Image.open(image_path)
    
    # Ensure image is in RGB mode
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Get pixel data
    pixels = list(img.getdata())
    
    # Extract the binary message
    binary_message = ""
    for pixel in pixels:
        r, g, b = pixel
        # Extract the least significant bit from each color channel
        binary_message += str(r & 1)
        binary_message += str(g & 1)
        binary_message += str(b & 1)
        
        # Check if we've found our delimiter (8 zeros) every 8 bits
        if len(binary_message) >= 8 and binary_message[-8:] == '00000000':
            break
    
    # Convert binary to encrypted text
    encrypted_message = binary_to_text(binary_message)
    
    # Decrypt the message
    if encrypted_message:
        decrypted_message = decrypt_message(encrypted_message, password)
        return decrypted_message
    else:
        return "No hidden message found in the image."

if __name__ == '__main__':
    image_path = input("Enter the path to the encoded image: ")
    password = input("Enter the decryption password: ")
    print("Extracted message:", decode_image(image_path, password))