import random


class NicknameGenerator:
    def __init__(self) -> None:
        self.already_used_nicknames = []

    def random_unique_nickname(self):
        candidate = random.choice(self.nicknames())
        while candidate in self.already_used_nicknames:
            candidate = random.choice(self.nicknames())

        self.already_used_nicknames.append(candidate)
        return candidate


    def nicknames(self):
        return [
            "pop_vii",
            "film_star",
            "bestactor",
            "justwatchin",
            "myname",
            "not_your_name",
            "whats_poppin",
            "crazymovies",
            "popcorn420",
            "Hanswurst",
            "The_Rock",
            "Dumbledore",
            "Master123",
            "Sith66",
            "Jedi",
            "Yoda",
            "Snape",
            "sevelantis",
            "magus",
            "powerrade",
            "late_or_never",
            "chikita",
            "snickers",
            "earth_planet",
            "programmer99",
            "hackerz123",
            "chocolatee",
            "chupa_chups",
            "i_like_trains",
            "jimi_henrix",
            "jim_morrison",
            "mirosalw",
            "bozydar",
            "kebabel",
            "artur",
            "ania",
            "piwo",
            "to_moje",
            "paliwo"
        ]
