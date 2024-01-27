from dataclasses import dataclass
import re
import math
 
CONFIGURATION = {
    'green': 13, 'red': 12, 'blue': 14
}

class Game:
    def __init__(self, current_game_data) -> None:
        game, turn_info = current_game_data.strip().split(":")
        x = re.findall('\d', game)
        x = int(''.join(x))
        self.game_id = x
        turns = turn_info.split(';')
        self.turns = [Turn(turn) for turn in turns]
    

    def __repr__(self) -> str:
        return f'{self.game_id}: {self.turns}'

    def config_check(self):
        for turn in self.turns:
            for current_color in turn.colors:
                if turn.colors[current_color] > CONFIGURATION[current_color]:
                    return False
        
        return True
    
    def calculate_power(self):
        max_dict = {color: -1 for color in CONFIGURATION.keys()}

        for turn in self.turns:
            for current_color in turn.colors:
                if turn.colors[current_color] > max_dict[current_color]:
                    max_dict[current_color] = turn.colors[current_color]
        
        power = math.prod(max_dict.values())
        return power

class Turn:
    def __init__(self, turn_info) -> None:
        colors_info = turn_info.split(',')
        self.colors = dict()
        for color_info in colors_info:
            count, color = color_info.strip().split(' ')
            if color in CONFIGURATION.keys():
                self.colors[color] = int(count)
    
    def __repr__(self) -> str:
        return f'Turn: {self.colors}'