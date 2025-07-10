from flask import Flask, render_template,request
from main import create_puzzle
from flask_cors import CORS
import tempfile
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])
app.secret_key = 'face_puzzle'


@app.route('/api/gen_puzzle', methods=["POST"])
def gen_puzzle():
    image=request.files['image']
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:
        image.save(temp.name)
        temp_path = temp.name
    print(image)
    puzzle_img_data=create_puzzle(temp_path)
    return puzzle_img_data


if __name__ == "__main__":
    print("Starting Puzzle Face Creator Flask App...")
    app.run(debug=True, port=5002, host='0.0.0.0')