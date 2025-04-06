from flask import Flask, render_template, request, redirect, url_for
import os
from embed import encode_image
from extract import decode_image

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads/"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "image" not in request.files:
            return "No image uploaded."

        image = request.files["image"]
        message = request.form["message"]
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], "cover.png")
        image.save(image_path)

        output_path = os.path.join(app.config["UPLOAD_FOLDER"], "encoded_image.png")
        encode_image(message, image_path, output_path)

        return render_template("result.html", image="encoded_image.png")

    return render_template("index.html")


@app.route("/decode")
def decode():
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], "encoded_image.png")
    message = decode_image(image_path)
    return f"Decoded message: {message}"


if __name__ == "__main__":
    app.run(debug=True)
