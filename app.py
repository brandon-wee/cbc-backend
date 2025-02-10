from fastapi import FastAPI
from chessboard import customChessBoard

app = FastAPI()

games = {}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/game/new")
def new_game():
    board = customChessBoard()
    games[board.game_id] = board
    return {"game_id": board.game_id}

@app.get("/game/play/{game_id}")
def next_move(game_id: int):
    return games[game_id].play_move()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)