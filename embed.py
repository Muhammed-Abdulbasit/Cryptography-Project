from PIL import Image

def text_to_binary(text):
    """Convert text to binary."""
    binary = ''.join(format(ord(c), '08b') for c in text)
    # Add a delimiter (8 zeros) to mark the end of the message
    binary += '00000000'
    return binary

def encode_image(text, image_path, output_path="encoded_image.png"):
    """Encode text into an image."""
    # Open the image
    img = Image.open(image_path)
    
    # Convert image to RGB if not already
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Get pixel data
    width, height = img.size
    pixels = list(img.getdata())
    
    # Convert text to binary
    binary_text = text_to_binary(text)
    
    if len(binary_text) > len(pixels) * 3:
        return "Error: Message too large for the image"
    
    # Embed the binary data into the image
    new_pixels = []
    binary_index = 0
    
    for pixel in pixels:
        # Once we've embedded all the data, just add the remaining pixels unchanged
        if binary_index >= len(binary_text):
            new_pixels.append(pixel)
            continue
        
        r, g, b = pixel
        new_r, new_g, new_b = r, g, b
        
        # Modify least significant bits based on the binary message
        if binary_index < len(binary_text):
            new_r = (r & ~1) | int(binary_text[binary_index])
            binary_index += 1
        
        if binary_index < len(binary_text):
            new_g = (g & ~1) | int(binary_text[binary_index])
            binary_index += 1
        
        if binary_index < len(binary_text):
            new_b = (b & ~1) | int(binary_text[binary_index])
            binary_index += 1
        
        new_pixels.append((new_r, new_g, new_b))
    
    # Create a new image with the modified pixels
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_pixels)
    
    # Save the new image
    new_img.save(output_path, "PNG")
    
    return f"Message successfully embedded in {output_path}"

if __name__ == '__main__':
    print(encode_image("Your secret message here", "toad.png"))