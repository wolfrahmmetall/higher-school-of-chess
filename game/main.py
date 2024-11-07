from chess_game import ChessGame

print("Hello! Enter game time (min): ")
game_time = int(input())
print("Enter increment (s): ")
increment = int(input())
game = ChessGame(game_time, increment)
game.start_game()
print(game.result)


