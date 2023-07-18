from trueskill import Rating

class Player:
    def __init__(self, name, rank):
        self.name = name
        self.rank = rank
        self.rating = Rating()
        self.comparisons = 0

    def update_rating(self, new_rating):
        self.rating = new_rating
        self.comparisons += 1

    def __str__(self):
        return f'Player: {self.name}, Rank: {self.rank}, Rating: {self.rating}, Comparisons: {self.comparisons}'

    def __repr__(self):
        return self.__str__()
    