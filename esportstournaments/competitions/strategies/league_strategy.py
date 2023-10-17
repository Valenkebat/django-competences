from .base import CompetitionStrategy

class LeagueStrategy(CompetitionStrategy):
    def create_match(self, competition, round_number, team1, team2):
        # Implementa la lógica específica para crear un partido de liga
        pass
    
    def determine_winner(self, match, team1_score, team2_score):
        # Implementa la lógica específica para determinar el ganador de un partido de liga
        pass