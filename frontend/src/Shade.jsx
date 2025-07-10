import { get_tile } from "./get_tile"
export default function Shade({ tileData }) {
    if (!tileData?.tile) return null;
    return (
        // <div style={{
        //     display: 'grid',
        //     gridTemplateRows: 'repeat(2, 10px)',
        //     gridTemplateColumns: 'repeat(2, 10px)',
        //     border: '1px solid black',
        // }}>
        //     <div style={{ ...style, backgroundColor: `rgb(${tileData.tile[0]})` }}></div>
        //     <div style={{ ...style, backgroundColor: `rgb(${tileData.tile[1]})` }}></div>
        //     <div style={{ ...style, backgroundColor: `rgb(${tileData.tile[3]})` }}></div>
        //     <div style={{ ...style, backgroundColor: `rgb(${tileData.tile[2]})` }}></div>
        // </div>
        // 
        <img width={20} src={get_tile(tileData["tile"])} alt="tiles" />
    );
}
