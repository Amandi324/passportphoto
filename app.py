import os
import io
from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/remove-bg", methods=["POST"])
def remove_bg():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]

    try:
        # Lazy import to ensure server starts instantly
        from rembg import remove, new_session   
        
        # CRITICAL FIX FOR RENDER FREE TIER:
        # We use 'u2netp' (a lightweight model, ~4MB) instead of the default 'u2net' (~170MB).
        # The default model will exceed Render's 512MB RAM limit and crash the server.
        session = new_session("u2netp") 

        input_image = Image.open(file.stream)
        output = remove(input_image, session=session)

        img_io = io.BytesIO()
        output.save(img_io, "PNG")
        img_io.seek(0)

        return send_file(img_io, mimetype="image/png")
        
    except Exception as e:
        # If it fails, print the error to your Render Logs for easier debugging
        print(f"Server Error during background removal: {e}")
        return jsonify({"error": "Failed to process image. Check server logs."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
