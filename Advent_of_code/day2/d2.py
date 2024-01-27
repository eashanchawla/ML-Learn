from game import *
import re

with open('./d2.txt', 'r') as f:
    data = f.readlines()

data = [Game(current_game_data) for current_game_data in data]
# final_sum = 0
# for current_game in data:
#     if current_game.config_check():
#         final_sum += current_game.game_id

# print(final_sum)

# part 2
total_power=0
for current_game in data:
    total_power += current_game.calculate_power()

print(total_power)