import { Fragment } from "react";
import Shade from "./Shade";
import Tile from "./Tile"
export default function Puzzle({ tiles }) {
    if (!tiles) return null;

    return (
        <Fragment>
            {/* <div
                style={{
                    display: 'grid',
                    gridTemplateRows: `repeat(20, 20px)`,
                    gridTemplateColumns: `repeat(15, 20px)`,
                    border: '1px solid black',
                    
                }}
                className="puzzle-face-img"
            >
                {tiles.map((row, inx) =>
                    row.map((tile, ind) => (
                        <Shade key={`${inx}-${ind}`} tileData={tile} />
                    ))
                )}
            </div> */}
            <div
                style={{
                    display: 'grid',
                    gridTemplateRows: `repeat(20, 10px)`,
                    gridTemplateColumns: `repeat(15, 10px)`,
                    border: '1px solid black',
                    
                }}
                className="puzzle-face-img"
            >
                {tiles.map((row, inx) =>
                    row.map((tile, ind) => (
                        <Tile key={`${inx}-${ind}`} tileData={tile} />
                    ))
                )}
            </div>
        </Fragment>
    );
}
