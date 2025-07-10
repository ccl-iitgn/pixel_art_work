# 🧩 Pixel Art Work

**Pixel Art Work** is an interactive web application that allows users to upload an image and transform it into a pixelated version using a predefined set of 300 puzzle tiles. The tool generates a key that can be used to assemble the pixelated artwork using physical or printed tiles. It’s ideal for creating artistic puzzles, educational tools, or handmade mosaics.

Users can download the pixelated image, the solution key, and the individual tile cutouts—enabling a full offline puzzle experience.

---



## 🔧 Features

- Upload any image and convert it into a 15x20 grid pixel puzzle.
- Pixelation is done using a fixed set of 300 predesigned tile pieces.
- Generates:
  - Pixelated reference image.
  - Puzzle key with correct tile positions and rotations.
  - Downloadable cutout sheets for printing and assembling.
- Currently uses a linear programming (LP) solver to ensure optimal tile placement.

---

## 🧪 How to Run

```bash
# Clone the repository
git clone https://github.com/ccl-iitgn/pixel_art_work.git
cd pixel_art_work

# ---------------------
# Frontend Setup
# ---------------------
cd frontend
npm install
npm run dev
# → Frontend runs at http://localhost:5173/

# ---------------------
# Backend Setup
# ---------------------
cd ../backend
pip install -r requirements.txt
python app.py
# → Backend runs at http://localhost:5002/
