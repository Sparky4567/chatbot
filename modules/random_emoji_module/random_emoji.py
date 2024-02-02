import emoji 
import random

class Random_Emoji:
    def __init__(self):
        self.emoji_list = emoji.EMOJI_DATA

    def pick_random(self):
        new_list = []

        for e in self.emoji_list:
            new_list.append(e[0])
        try:
            random_emoji = random.choice(new_list)
            return random_emoji
        except Exception as e:
            return ""