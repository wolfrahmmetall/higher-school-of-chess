function OpenGamesPanel() {
  const openGames = [
    { id: 1, opponent: "Игрок 4", elo: 1550 },
    { id: 2, opponent: "Игрок 5", elo: 1650 },
  ];

  const joinGame = (id: number) => {
    console.log(`Присоединиться к игре с ID: ${id}`);
  };

  return (
    <div>
      <h3>Открытые игры</h3>
      <ul>
        {openGames.map((game) => (
          <li key={game.id}>
            {game.opponent} (ELO: {game.elo})
            <button onClick={() => joinGame(game.id)}>Присоединиться</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default OpenGamesPanel;
