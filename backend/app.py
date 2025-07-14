import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from flask import Flask, request, send_file, send_from_directory
from flask_cors import CORS
from Solution import create_puzzle
import tempfile

app = Flask(
    __name__,
    static_folder='../frontend/dist',
    static_url_path='/'
)
CORS(app, origins=["http://localhost:5173", "https://pixel-art-work.vercel.app"])
app.secret_key = 'face_puzzle'

@app.route('/api/gen_puzzle', methods=["POST"])
def gen_puzzle():
    image = request.files['image']
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:
        image.save(temp.name)
        temp_path = temp.name
    puzzle_img_data = create_puzzle(temp_path)
    return puzzle_img_data 
@app.route('/<path:path>', methods=["GET"])
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def fallback(path):
    return send_file(os.path.join(app.static_folder, 'index.html'))

if __name__ == "__main__":
    print("Starting Puzzle Face Creator Flask App...")
    app.run(debug=True, port=5002, host='0.0.0.0')
