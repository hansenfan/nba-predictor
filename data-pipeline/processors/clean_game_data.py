import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class GameDataCleaner:
    def __init__(self, data_path="../data"):
        self.data_path = Path(__file__).parent.parent.parent / "data"
        self.csv_path = self.data_path / "csv"
        self.output_path = Path(__file__).parent.parent / "data" / "processed"
        self.output_path.mkdir(exist_ok=True, parents=True)

    def load_game_data(self):
        game_info = pd.read_csv(self.csv_path / "game_info.csv")
        game_summary = pd.read_csv(self.csv_path / "game_summary.csv")
        teams = pd.read_csv(self.csv_path / "team.csv")

        try:
            line_score = pd.read_csv(self.csv_path / "line_score.csv")
        except:
            line_score = None

        return game_info, game_summary, teams, line_score

    def clean_game_data(self, game_info, game_summary, teams, line_score=None):
        games = game_info.merge(game_summary, on='game_id', how='left', suffixes=('', '_summary'))

        games['game_date'] = pd.to_datetime(games['game_date'])

        games = games[games['game_date'].dt.year >= 2010]
        games = games[games['game_date'].dt.year <= 2023]

        initial_count = len(games)
        games = games.drop_duplicates(subset=['game_id'])

        games['attendance'] = games['attendance'].fillna(0)
        games['game_time'] = games['game_time'].fillna('Unknown')

        games = games.merge(teams, left_on='home_team_id', right_on='id', how='left')
        games = games.rename(columns={'full_name': 'home_team_name', 'abbreviation': 'home_team_abbr'})

        games = games.merge(teams, left_on='visitor_team_id', right_on='id', how='left')
        games = games.rename(columns={'full_name': 'away_team_name', 'abbreviation': 'away_team_abbr'})

        if line_score is not None:
            home_scores = line_score[line_score['team_id_home'].notna()].copy()
            away_scores = line_score[line_score['team_id_away'].notna()].copy()

            games = games.merge(home_scores[['game_id', 'pts_home']], on='game_id', how='left')
            games = games.merge(away_scores[['game_id', 'pts_away']], on='game_id', how='left')

        games['season'] = games['game_date'].dt.year
        games['month'] = games['game_date'].dt.month
        games['day_of_week'] = games['game_date'].dt.dayofweek

        games['is_weekend'] = games['day_of_week'].isin([5, 6]).astype(int)
        games['is_playoff_month'] = games['month'].isin([4, 5, 6]).astype(int)

        if 'pts_home' in games.columns and 'pts_away' in games.columns:
            games['home_win'] = (games['pts_home'] > games['pts_away']).astype(int)
            games['total_points'] = games['pts_home'] + games['pts_away']
            games['point_difference'] = games['pts_home'] - games['pts_away']

        games['home_team_id'] = games['home_team_id'].astype(str)
        games['visitor_team_id'] = games['visitor_team_id'].astype(str)

        games['is_rivalry'] = games.apply(
            lambda x: self._check_rivalry(x['home_team_abbr'], x['away_team_abbr']), axis=1
        )

        return games

    def _check_rivalry(self, home_team, away_team):
        rivalries = [
            ('LAL', 'BOS'), ('LAL', 'LAC'), ('BOS', 'PHI'),
            ('NYK', 'BOS'), ('CHI', 'DET'), ('GSW', 'LAC')
        ]
        return int((home_team, away_team) in rivalries or (away_team, home_team) in rivalries)

    def validate_data(self, games):
        missing_dates = games['game_date'].isnull().sum()
        missing_teams = games['home_team_id'].isnull().sum()
        missing_away_teams = games['visitor_team_id'].isnull().sum()

        season_counts = games['season'].value_counts().sort_index()
        team_counts = games['home_team_abbr'].value_counts().head(10)

        if 'home_win' in games.columns:
            win_rate = games['home_win'].mean()

        return games

    def create_summary_stats(self, games):
        summary = {
            'total_games': len(games),
            'date_range': f"{games['game_date'].min()} to {games['game_date'].max()}",
            'seasons': games['season'].nunique(),
            'teams': games['home_team_abbr'].nunique(),
            'missing_attendance': games['attendance'].isnull().sum(),
            'weekend_games': games['is_weekend'].sum(),
            'playoff_month_games': games['is_playoff_month'].sum(),
            'rivalry_games': games['is_rivalry'].sum() if 'is_rivalry' in games.columns else 0
        }

        if 'home_win' in games.columns:
            summary['home_win_rate'] = games['home_win'].mean()

        return summary

    def save_clean_data(self, games):
        output_file = self.output_path / "clean_games.csv"
        games.to_csv(output_file, index=False)

        summary_file = self.output_path / "data_summary.txt"
        with open(summary_file, 'w') as f:
            f.write("NBA Game Data Summary\n")
            f.write("====================\n")
            f.write(f"Total games: {len(games)}\n")
            f.write(f"Date range: {games['game_date'].min()} to {games['game_date'].max()}\n")
            f.write(f"Seasons: {games['season'].nunique()}\n")
            f.write(f"Teams: {games['home_team_abbr'].nunique()}\n")

    def run(self):
        try:
            game_info, game_summary, teams, line_score = self.load_game_data()
            clean_games = self.clean_game_data(game_info, game_summary, teams, line_score)
            clean_games = self.validate_data(clean_games)
            summary = self.create_summary_stats(clean_games)
            self.save_clean_data(clean_games)
            return clean_games, summary
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise

if __name__ == "__main__":
    cleaner = GameDataCleaner()
    clean_games, summary = cleaner.run()
