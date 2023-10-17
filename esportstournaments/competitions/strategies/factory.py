from ..models import Competition, SingleEliminationCompetition, DoubleEliminationCompetition, LeagueCompetition

class CompetitionFactory:
    @staticmethod
    def create_competition(name, competition_type):
        competition = Competition(name=name)
        
        if competition_type == 'single_elimination':
            return SingleEliminationCompetition.objects.create(competition=competition)
        elif competition_type == 'double_elimination':
            return DoubleEliminationCompetition.objects.create(competition=competition)
        elif competition_type == 'league':
            return LeagueCompetition.objects.create(competition=competition)
        else:
            raise ValueError("Tipo de competencia no válido")