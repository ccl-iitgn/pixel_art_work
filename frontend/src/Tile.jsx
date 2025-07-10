export default function Shade({ tileData }) {
    if (!tileData?.tile) return null;
    return (
        <div style={{
            width: "10px",
            height: "10px",
            background: tileData.n > 150 ? `linear-gradient(0.34turn, rgb(${tileData.tile[0]}),rgb(${tileData.tile[2]}))` : `linear-gradient(0.25turn, rgb(${tileData.tile[0]}),rgb(${tileData.tile[1]}))`,
            transform: `rotate(${-90 * tileData.rotations}deg)`
        }}>
        </div>
    );
}