import RatingPanel from "../components/RatingPanel";
import OpenGamesPanel from "../components/OpenGamesPanel";

function ChessMain() {
  return (
    <div className="container">
      <div className="header-container">
        <h1>ШАХМАТЫ</h1>
        <h2>sygma.com</h2>
      </div>
      <div className="panels">
        <div className="panel" style={{ width: "25%" }}>
          <RatingPanel />
        </div>
        <div className="panel" style={{ width: "75%" }}>
          <OpenGamesPanel />
        </div>
      </div>
    </div>
  );
}

export default ChessMain;
