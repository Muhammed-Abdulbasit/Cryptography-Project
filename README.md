Steganography Project for Cryptography course

Steps for running the code:<br>

**Embedding the secret message**
1. Run the command
   ```python3 embed.py```

2. Enter the message you want to encrypt in the message

3. Enter an encryption password that would need to be used to decrypt the message

4. Enter the path to the original image. An image called toad.png is already included to use as an example, so you can just type toad.png here, but any other png image would work (jpg and jpeg will not work because they have lossy compression).

5. Enter the output image path (secret.png, for example). A new image with your secret message embedded will be created with the name of the output path you use here. If you do not put any path, the new image will simply be named encoded_image.png.

**Extracting the secret message** <br>

  6. Run the command ```python3 extract.py```

  7. Enter the path to the image with the encoded message. This will be the same as whatever you entered for step 5. If the new image is named secret.png, type that here.

  8. Enter the decryption password that you set in step 3.

<br>

After following these steps, you will see the secret message you entered in step 2. You can of course use a different image to store the secret message as long as it is a png, and you can send the image to anyone else and have them extract it using the same process. This way you can send someone an image that looks completely normal, but once they add the image to the same directory as these files and run extract.py, provided they know the password you set when embedding the message, they will be able to see your secret encrypted message.
