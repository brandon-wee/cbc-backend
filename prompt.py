class Prompts:
    SYSTEM_PROMPT = ' '.join([
        "You are currently playing a game of chess."
        "You have the {color} pieces, and it is your turn to move.",
        "You must also comment on your move. You must comment with the following behavior: {behaviour}",
        "{mode}\n",
        "If you want to castle, return the following JSON object with your own comment: {castle_json}.",
        "Otherwise, you are required to give your move in the JSON format:\n",
        "{json_schema}",
        "\nJust reply with the JSON object, do not include any other information in your reply. Also, remember you are given a JSON schema! Not a JSON object. You must create a JSON object that follows the rules defined by the schema.",
        "Return only the raw JSON object, with no markdown formatting, backticks, or extra text.",
        "You can only select a piece in the following format: K, Q, R, B, N, P. Upper case for white pieces, lower case for black pieces.",
        "You need not specify that you are capturing a piece using the 'x' notation. The system will automatically detect this.",
    ])
    
    CHAIN_OF_THOUGHT = ' '.join([
        "THIS IS THE SYSTEM TALKING TO YOU.",
        "You are now required to generate a chain of thoughts to help you make your move.",
        "You have the {color} pieces, and it is your turn to move.",
        "The current board state is stored with the FEN notation: {fen}",
        "You will now think about which move to make. To help you make your decision, you will generate a chain of thoughts.",
        "You will answer the following questions to generate your chain of thoughts (you can stop answering questions earlier if you want to):",
        "\n1. Think about which pieces see each other, and what these interactions mean.",
        "\n2. Do you have a piece that can give a check? If so, determine whether this check will improve your position.",
        "\n3. Do you have a piece that can capture a piece? If so, determine whether this capture will improve your position.",
        "\n4. Do you have a piece that can attack a piece? If so, determine whether this attack will improve your position.",
        "\n5. If you have no pieces that can give a check, capture a piece, or attack a piece, then you should move a piece to a square that improves your position.",
        "\nJust ideate and write down your thoughts in a clear and structured way. You can write as much as you want. However, try to ideate in a paragraph format.",
    ])

    CHECK = ''.join([
        "You are currently in check. You must make a move that will remove this check.",
        "You have the following options:",
        "{options}"
    ])

    MODES = {
        "strict": "The game is in strict mode. You are only allowed to make the moves that are listed below. {legal_moves}",
        "meme": "The game is in meme mode. You will not be given a list of moves and instead must make a move yourself based on only the information given to you so far."
    }

    JSON_SCHEMA = """
{
    "type": "object",
    "properties": {
        "piece": {
            "type": "string",
            "description": "The piece you want to move. Must be a valid piece symbol. You must only use the following symbols: K, Q, R, B, N, P. Upper case for white pieces, lower case for black pieces."
        },
        "initial_square": {
            "type": "string",
            "description": "The square the piece is currently on. Must be a valid square."
        },
        "final_square": {
            "type": "string",
            "description": "The square you want to move the piece to. Must be a valid square."
        },
        "comment": {
            "type": "string",
            "description": "A comment on your move. Must be a string. Follow the behavior specified above."
        }
    },
    "required": ["piece", "initial_square", "final_square", "comment"]
}
"""
    
    LLM_MOVE_RESPONSE = "I will move my {piece} from {initial_square} to {final_square}."
    CASTLE_JSON = """{'piece': 'O-O', "initial_square": 'e1', "final_square": 'g1', 'comment': 'Your own comments'} or {'piece': 'O-O-O', "initial_square": 'e1', "final_square": 'c1', 'comment': 'Your own comments'} or
{'piece': 'O-O', "initial_square": 'e8', "final_square": 'g8', 'comment': 'Your own comments'} or {'piece': 'O-O-O', "initial_square": 'e8', "final_square": 'c8', 'comment': 'Your own comments'}"""