from PIL import Image

def binary_to_text(binary):
    """Convert binary to text."""
    text = ""
    # Process 8 bits at a time (one character)
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        # Check if we've reached the delimiter
        if byte == '00000000':
            break
        # Convert binary to character and add to text
        text += chr(int(byte, 2))
    return text

def decode_image(image_path):
    """Extract hidden text from an image."""
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
    
    # Convert binary to text
    message = binary_to_text(binary_message)
    return message

if __name__ == '__main__':
    print(decode_image("encoded_image.png"))