from llm import LLM
from prompt import Prompts

class PlayerAgent:
    def __init__(self):
        pass

    def next_move(self, board, previous_move):
        print(previous_move)

        piece = input("Enter piece: ")
        initial_square = input("Enter initial square: ")
        final_square = input("Enter final square: ")
        comment = input("Enter comment: ")

        return piece, initial_square, final_square, comment
    
class LLMAgent:
    def __init__(self, color,  model, behaviour, mode="meme", cot=False, help=False):
        system = Prompts.SYSTEM_PROMPT.format(color=color, behaviour=behaviour, mode=Prompts.MODES[mode], json_schema=Prompts.JSON_SCHEMA, castle_json=Prompts.CASTLE_JSON)
        self.llm = LLM(model, system, cot)
        self.behaviour = behaviour
        self.cot = cot
        self.color = color
        self.mode = mode
        self.help = help

    def next_move(self, board, previous_move):
        if self.cot:
            chain_of_thought = Prompts.CHAIN_OF_THOUGHT.format(color=self.color, fen=board)
            thoughts = self.llm.get_thoughts(chain_of_thought)
            print(thoughts)
        else:
            thoughts = "You will now generate a move based on your own thoughts."
        
        try:
            prompt = Prompts.LLM_MOVE_RESPONSE.format(piece=previous_move[0], initial_square=previous_move[1], final_square=previous_move[2])
        except:
            prompt = "You are the first to move. Good luck!"
        
        result = self.llm.get_llm_response(prompt)
        print(result)
        if result["error"]:
            return None, None, None, None
        
        piece = result["piece"]
        initial_square = result["initial_square"]
        final_square = result["final_square"]
        comment = result["comment"]
        
        return piece, initial_square, final_square, comment

