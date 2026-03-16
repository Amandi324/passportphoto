from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image
import io
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/remove-bg', methods=['POST'])
def remove_bg():

    if 'image' not in request.files:
        return {"error": "No image uploaded"}

    file = request.files['image']

    input_image = Image.open(file.stream)

    output = remove(input_image)

    img_io = io.BytesIO()
    output.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
