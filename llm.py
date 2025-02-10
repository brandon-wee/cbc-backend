import json
import re

class LLM:
    def __init__(self, model, system, cot=False):
        self.model = model
        self.memory = [
            ("system", system)
        ]
        self.cot = cot
            
    def get_llm_response(self, prompt, chain_of_thought=None):
        self.memory.append(("human", prompt))

        if self.cot:
            self.get_thoughts(chain_of_thought)

        response = self.model.invoke(self.memory)
        try:
            response = re.sub(r"```json|```", "", response.content).strip()
            self.memory.append(("assistant", response))
            result = json.loads(response)
            result["error"] = False
        except Exception as e:
            print(e)
            print(response)
            return {"error": True}
        
        return result
    
    def get_thoughts(self, chain_of_thought):
        self.memory.append(("human", chain_of_thought))
        response = self.model.invoke(self.memory)
        self.memory.append(response.content)
