import './Game.css';

const Game = () => {
  return (
    <div className="game-container">
      <div className="player-info">
        <h3>Игрок 1</h3>
        <p>Рейтинг: 1500</p>
      </div>

      <div className="chessboard">
        <div className="board">
          {/* Пример шахматной доски, можно заменить на реальную реализацию */}
          {Array.from({ length: 8 }, (_, rowIndex) => (
            <div className="row" key={rowIndex}>
              {Array.from({ length: 8 }, (_, colIndex) => (
                <div className={`square ${ (rowIndex + colIndex) % 2 === 0 ? 'light' : 'dark' }`} key={colIndex}>
                  {/* Здесь можно разместить фигуры */}
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>

      <div className="player-info">
        <h3>Игрок 2</h3>
        <p>Рейтинг: 1600</p>
      </div>

      <div className="moves-list">
        <h3>Последние ходы</h3>
        <ul>
          <li>1. e4 e5</li>
          <li>2. Nf3 Nc6</li>
          <li>3. Bb5 a6</li>
        </ul>
      </div>
    </div>
  );
};

export default Game;