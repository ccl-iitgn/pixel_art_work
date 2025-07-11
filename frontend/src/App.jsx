import { Fragment, useEffect, useRef, useState } from 'react'
import './App.css'
import axios from "axios"
import Puzzle from './Puzzle'
import html2canvas from 'html2canvas';
import PuzzleSol from './PuzzleSol';
import jsPDF from 'jspdf';
import { img_data } from "./Data"
function App() {
  const [loading, setLoading] = useState(false)
  const [data, setData] = useState(null)
  const [prevImg, setPrevImg] = useState(null)
  const [file, setFile] = useState(null)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    setData(null)
    if (selectedFile) {
      setFile(selectedFile)
      setPrevImg(URL.createObjectURL(selectedFile))
    }else{
      setPrevImg(null)
      setFile(null)
    }
  }
  const downloadPDF = async (class1 = "puzzle-image", class2 = "solution-image") => {
    try {
      const element1 = document.querySelector(`.${class1}`);
      const element2 = document.querySelector(`.${class2}`);

      if (!element1 || !element2) {
        console.error("One or both elements not found.");
        return;
      }

      const canvas1 = await html2canvas(element1, { scale: 2 });
      const canvas2 = await html2canvas(element2, { scale: 2 });

      const imgData1 = canvas1.toDataURL('image/png');
      const imgData2 = canvas2.toDataURL('image/png');
      const pdfWidth = 595;
      const pdfHeight = 842;
      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'px',
        format: [pdfWidth, pdfHeight],
      });
      const addImageToPDF = (pdf, imgData, canvas) => {
        const ratio = Math.min(pdfWidth / canvas.width, pdfHeight / canvas.height);
        const imgWidth = canvas.width * ratio;
        const imgHeight = canvas.height * ratio;
        const x = (pdfWidth - imgWidth) / 2;
        const y = (pdfHeight - imgHeight) / 2;
        pdf.addImage(imgData, 'PNG', x, y, imgWidth, imgHeight);
      };

      addImageToPDF(pdf, imgData1, canvas1);
      pdf.addPage();
      addImageToPDF(pdf, imgData2, canvas2);

      pdf.save('face_puzzle.pdf');
    } catch (error) {
      console.error('PDF download failed:', error);
    }
  };
  const handleGeneratePuzzle = async () => {
    if (!file) return
    setLoading(true)
    const formData = new FormData()
    formData.append("image", file)

    try {
      const response = await axios.post("http://127.0.0.1:5002/api/gen_puzzle", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      })
      setData(response.data)
    } catch (error) {
      console.error("Error generating puzzle:", error)
      alert("Failed to generate puzzle.")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {

    return () => {
      if (prevImg) {
        URL.revokeObjectURL(prevImg)
      }
    }
  }, [prevImg])

  return (
    <Fragment>
      <header className='header-container'>
        <img src="/logo.png" alt="iitgn_logo" />
        <h1>Pixel Art Work</h1>
      </header>
      <main>
        <section className='about-puzzle-section'>
          <p>
            Uploading an image, then click "Generate" to create the Image Key for your pixel art work. This key will guide you in assembling all 300 pieces. Carefully match each piece according to the layout, ensuring the correct orientation. Once all pieces are properly connected, lift the final assembly to reveal the complete Puzzle Face.
          </p>
        </section>
        <section className='puzzle_img_section'>
          <div>
            <b>Uploaded Image</b>
            <img
              src={prevImg || "/image.png"}
              alt="Preview"
            />
          </div>
          {!data ? <div>
            <b>Generated Image</b>
            <img src='/default_tiles.png' alt='default_tiles' />
          </div> : <div>
            <b>Generated Image</b>
            <Puzzle tiles={data} />
          </div>}
        </section>
        <section className='puzzle-btns-section'>
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
          />
          <div>
            <button onClick={handleGeneratePuzzle} disabled={!file || loading}>
              {loading ? "Generating..." : "Generate Puzzle"}
            </button>
            {data && <button onClick={() => {
              downloadPDF("puzzle-face-img", "puzzle-solution")
            }}>Download</button>}
          </div>
        </section>

        {loading ? <section className='loading-section'>
          <img src="/loading.svg" alt="loading img" />
          <p>Please wait, this may take a minute.</p>
        </section> : data &&
        <section className='soution-section' style={{ marginTop: 20, display: "flex", justifyContent: "center" }}>
          <div>
            <PuzzleSol tiles={data} img_url={prevImg} />
          </div>
        </section>}
      </main>

    </Fragment>
  )
}

export default App
