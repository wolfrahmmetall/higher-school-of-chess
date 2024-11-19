function RatingPanel() {
  const ratings = [
    { name: "Игрок 1", elo: 1500 },
    { name: "Игрок 2", elo: 1600 },
    { name: "Игрок 3", elo: 1700 },
  ];

  return (
    <div>
      <h3>Рейтинг шахматистов</h3>
      <ul>
        {ratings.map((player) => (
          <li key={player.name}>
            {player.name}: {player.elo}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default RatingPanel;
