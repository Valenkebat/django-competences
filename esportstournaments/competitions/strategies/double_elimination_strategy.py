from .base import CompetitionStrategy
from ...matches.models import Match

class DoubleEliminationStrategy(CompetitionStrategy):
    def create_match(self, competition, round_number, team1, team2):
        # Comprueba si es una partida en la ronda inicial o en una ronda posterior
        if round_number == 1:
            # En la ronda inicial, simplemente crea un partido normal
            match = Match.objects.create(
                competition=competition,
                round_number=round_number,
                team1=team1,
                team2=team2,
            )
        else:
            # En rondas posteriores, se crea un partido que sigue las reglas de doble eliminación
            # Esto puede requerir lógica adicional para determinar qué equipos deben enfrentarse
            # en función de los resultados anteriores
            # Aquí se asume que "previous_match" es el partido anterior en la ronda
            previous_match = Match.objects.get(competition=competition, round_number=round_number - 1)
            winner_team = previous_match.winner
            loser_team = previous_match.team1 if previous_match.team2 == winner_team else previous_match.team2
            
            match = Match.objects.create(
                competition=competition,
                round_number=round_number,
                team1=winner_team,
                team2=loser_team,
            )

        return match
    
    def determine_winner(self, match, team1_score, team2_score):
        # Implementa la lógica específica para determinar el ganador de un partido de liga
        pass