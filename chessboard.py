import chess
from agent import *
from model import models, model_behaviour

color = [chess.WHITE, chess.BLACK]

class customChessBoard:
    def __init__(self):
        self.board = chess.Board()
        self.move_list = []
        self.current_player = 0

        self.white = None
        self.black = None

    def reset(self):
        self.board = chess.Board()
        self.move_list = []
        self.current_player = 0

    def set_players(self, white, black):
        self.white = white
        self.black = black

    def next_move(self):
        if self.current_player == 0:
            piece, initial_square, final_square, comment = self.white.next_move(self.board, self.move_list[-1] if len(self.move_list) > 0 else None)
            piece = piece.upper()
        else:
            piece, initial_square, final_square, comment = self.black.next_move(self.board, self.move_list[-1] if len(self.move_list) > 0 else None)
            piece = piece.lower()

        self.move_list.append((piece, initial_square, final_square, comment))

    def play_move(self):
        self.next_move()
        piece, initial_square, final_square, _ = self.move_list[-1]
        if piece.upper() not in ["O-O", "O-O-O"]:
            piece, initial_square, final_square = chess.Piece.from_symbol(piece), chess.parse_square(initial_square), chess.parse_square(final_square)
            self.board.remove_piece_at(initial_square)
            self.board.set_piece_at(final_square, piece)
        
        else: # Castling
            is_white = self.current_player == 0
            king_symbol = "K" if is_white else "k"
            rook_symbol = "R" if is_white else "r"

            king_pos = None
            for square in chess.SQUARES:
                if self.board.piece_at(square) == chess.Piece.from_symbol(king_symbol):
                    king_pos = square
                    break
            
            if is_white:
                king_dest_k, king_dest_q = chess.G1, chess.C1
                rook_start_k, rook_dest_k = chess.H1, chess.F1
                rook_start_q, rook_dest_q = chess.A1, chess.D1
            else:
                king_dest_k, king_dest_q = chess.G8, chess.C8
                rook_start_k, rook_dest_k = chess.H8, chess.F8
                rook_start_q, rook_dest_q = chess.A8, chess.D8

            self.board.remove_piece_at(king_pos)

            if piece.upper() == 'O-O':
                self.board.set_piece_at(king_dest_k, chess.Piece.from_symbol(king_symbol))
                
                if self.board.piece_at(rook_start_k) == chess.Piece.from_symbol(rook_symbol):
                    self.board.remove_piece_at(rook_start_k)
                self.board.set_piece_at(rook_dest_k, chess.Piece.from_symbol(rook_symbol))
                
            elif piece.upper() == 'O-O-O':
                self.board.set_piece_at(king_dest_q, chess.Piece.from_symbol(king_symbol))
                
                if self.board.piece_at(rook_start_q) == chess.Piece.from_symbol(rook_symbol):
                    self.board.remove_piece_at(rook_start_q)
                self.board.set_piece_at(rook_dest_q, chess.Piece.from_symbol(rook_symbol))


        str_piece, str_initial_square, str_final_square, comment = self.move_list[-1]
        return {"board": self.board.fen(), "piece": str_piece, "initial_square": str_initial_square, "final_square": str_final_square, "comment": comment, "state": self.result(), "current_player": self.current_player}

    def result(self):
        if self.board.is_checkmate():
            return "checkmate"
        
        if self.board.is_stalemate():
            return "stalemate"
        
        if self.board.is_insufficient_material():
            return "insufficient material"
        
        if "k" not in (self.board.fen()).split(" ")[0]:
            return "no black king"
        
        if "K" not in (self.board.fen()).split(" ")[0]:
            return "no white king"
        
        return "playing"

    def play_console(self):
        while self.result() == "playing":
            gotKing = (self.board.fen()).split(" ")
            
            self.play_move()
            print(self.board)
            self.current_player = 1 - self.current_player
            self.board.turn = color[self.current_player]
        
        print("Noice")


if __name__ == "__main__":
    board = customChessBoard()
    # white = PlayerAgent()
    white = LLMAgent(color="white", model=models["gemini"], behaviour=model_behaviour["neutral"], mode="meme", cot=False)
    # black = PlayerAgent()
    black = LLMAgent(color="black", model=models["gpt-4o-mini"], behaviour=model_behaviour["neutral"], mode="meme", cot=False)
    board.set_players(white, black)
    
    board.play_console()