import { useEffect, useState } from "react";
import Puzzle from "./Puzzle";
export default function PuzzleSol({ tiles, img_url }) {
    if (!tiles) return
    const get_bg = (num) => {
        if (num > 240) return `url(/type5.png)`
        if (num > 180) return `url(/type4.png)`
        if (num > 120) return `url(/type3.png)`
        if (num > 60) return `url(/type2.png)`
        return `url(/type1.png)`
    }
    return (
        <div className="puzzle-solution">
            <div className="puzzle-key-header-container">
                <img src="logo.png" alt="logo_img" />
                <p>
                    This key will guide you in assembling all 300 pieces. Carefully match each piece according to the layout, ensuring the correct orientation. Once all pieces are properly connected, lift the final assembly to reveal the complete Puzzle Face.
                </p>
                <img src={img_url} alt="upload_img" />
            </div>
            <div
                style={{
                    display: 'grid',
                    gridTemplateRows: `repeat(${tiles.length}, 50px)`,
                    gridTemplateColumns: `repeat(${tiles[0].length}, 50px)`,
                    border: '1px solid black',
                    color: "white",
                    fontSize: "small"
                }}
            >
                {tiles.map((row, x) => {
                    return row.map((tile, y) => {
                        return (
                            <div key={`${x}-${y}`}
                                style={{
                                    border: '1px solid black',
                                    display: "flex",
                                    alignItems: "center",
                                    justifyContent: "center",
                                    transform: `rotate(${90 * tiles[x][tiles[0].length - y - 1].rotations}deg)`,
                                    backgroundImage: get_bg(tiles[x][tiles[0].length - y - 1].n),
                                    backgroundPosition: "center",
                                    backgroundSize: "contain",
                                    fontWeight: "600",
                                    backgroundRepeat: "no-repeat"
                                }}
                            >
                                {tiles[x][tiles[0].length - y - 1].n % 60 + 1}
                            </div>
                        );
                    })

                })}
            </div>
        </div>

    );
}
