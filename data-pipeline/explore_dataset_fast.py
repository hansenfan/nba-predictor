import pandas as pd
import numpy as np
import sqlite3
import os
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class NBADatasetExplorer:
    def __init__(self, data_path="../data"):
        self.data_path = Path(data_path)
        self.csv_path = self.data_path / "csv"
        self.sqlite_path = self.data_path / "nba.sqlite"
        self.dataframes = {}

    def load_all_csv_files(self):
        """Load all CSV files from the archive/csv directory, skipping large files"""
        print("Loading CSV files...")
        large_files = ['play_by_play.csv']  # Skip these large files

        for csv_file in self.csv_path.glob("*.csv"):
            if csv_file.name in large_files:
                print(f"Skipping large file: {csv_file.name}")
                continue

            try:
                df = pd.read_csv(csv_file)
                self.dataframes[csv_file.stem] = df
                print(f"Loaded {csv_file.stem}: {df.shape[0]} rows, {df.shape[1]} columns")
            except Exception as e:
                print(f"Error loading {csv_file}: {e}")

    def explore_sqlite_database(self):
        """Explore the SQLite database structure"""
        if not self.sqlite_path.exists():
            print("SQLite database not found")
            return

        print("\nExploring SQLite database...")
        conn = sqlite3.connect(self.sqlite_path)

        # Get table names
        tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
        print(f"Tables in database: {tables['name'].tolist()}")

        # Show schema for each table
        for table in tables['name']:
            schema = pd.read_sql_query(f"PRAGMA table_info({table})", conn)
            print(f"\n{table} table schema:")
            print(schema[['name', 'type', 'notnull']].to_string(index=False))

            # Show sample data
            sample = pd.read_sql_query(f"SELECT * FROM {table} LIMIT 3", conn)
            print(f"\nSample data from {table}:")
            print(sample.to_string(index=False))

        conn.close()

    def analyze_player_data(self):
        """Analyze player-related datasets"""
        print("\n=== PLAYER DATA ANALYSIS ===")

        if 'player' in self.dataframes:
            df = self.dataframes['player']
            print(f"Player dataset: {df.shape}")
            if 'is_active' in df.columns:
                print(f"Active players: {df['is_active'].sum()}")
                print(f"Inactive players: {(df['is_active'] == 0).sum()}")

        if 'common_player_info' in self.dataframes:
            df = self.dataframes['common_player_info']
            print(f"\nDetailed player info: {df.shape}")

            # Position analysis
            if 'position' in df.columns:
                position_counts = df['position'].value_counts()
                print("\nPosition distribution:")
                print(position_counts)

            # Height analysis
            if 'height' in df.columns:
                print(f"\nHeight statistics:")
                print(df['height'].describe())

            # Experience analysis
            if 'season_exp' in df.columns:
                print(f"\nSeason experience statistics:")
                print(df['season_exp'].describe())

    def analyze_game_data(self):
        """Analyze game-related datasets"""
        print("\n=== GAME DATA ANALYSIS ===")

        if 'game_info' in self.dataframes:
            df = self.dataframes['game_info']
            print(f"Game info dataset: {df.shape}")

            # Date range
            if 'game_date' in df.columns:
                df['game_date'] = pd.to_datetime(df['game_date'])
                print(f"Date range: {df['game_date'].min()} to {df['game_date'].max()}")
                print(f"Total games: {len(df)}")

                # Games per year
                df['year'] = df['game_date'].dt.year
                games_per_year = df['year'].value_counts().sort_index()
                print(f"\nGames per year (last 10 years):")
                print(games_per_year.tail(10))

        if 'game_summary' in self.dataframes:
            df = self.dataframes['game_summary']
            print(f"\nGame summary dataset: {df.shape}")
            print(f"Columns: {list(df.columns)}")

    def analyze_draft_data(self):
        """Analyze draft-related datasets"""
        print("\n=== DRAFT DATA ANALYSIS ===")

        if 'draft_history' in self.dataframes:
            df = self.dataframes['draft_history']
            print(f"Draft history dataset: {df.shape}")

            # Draft years
            if 'season' in df.columns:
                year_counts = df['season'].value_counts().sort_index()
                print(f"\nDrafts per year (last 10 years):")
                print(year_counts.tail(10))

            # Draft rounds
            if 'round_number' in df.columns:
                round_counts = df['round_number'].value_counts().sort_index()
                print(f"\nPicks per round:")
                print(round_counts)

        if 'draft_combine_stats' in self.dataframes:
            df = self.dataframes['draft_combine_stats']
            print(f"\nDraft combine stats: {df.shape}")
            print(f"Columns: {list(df.columns)}")

    def analyze_team_data(self):
        """Analyze team-related datasets"""
        print("\n=== TEAM DATA ANALYSIS ===")

        for key in ['team', 'team_details', 'team_history']:
            if key in self.dataframes:
                df = self.dataframes[key]
                print(f"\n{key} dataset: {df.shape}")
                print(f"Columns: {list(df.columns)}")

    def create_data_overview(self):
        """Create a comprehensive overview of all datasets"""
        print("\n=== DATASET OVERVIEW ===")

        overview_data = []
        for name, df in self.dataframes.items():
            overview_data.append({
                'Dataset': name,
                'Rows': len(df),
                'Columns': len(df.columns),
                'Size (MB)': round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
                'Missing Values': df.isnull().sum().sum(),
                'Duplicate Rows': df.duplicated().sum()
            })

        overview_df = pd.DataFrame(overview_data)
        print(overview_df.to_string(index=False))

        return overview_df

    def find_relationships(self):
        """Find relationships between different datasets"""
        print("\n=== DATASET RELATIONSHIPS ===")

        # Check for common ID columns
        id_columns = {}
        for name, df in self.dataframes.items():
            for col in df.columns:
                if 'id' in col.lower() or 'person' in col.lower():
                    if col not in id_columns:
                        id_columns[col] = []
                    id_columns[col].append(name)

        print("Common ID columns across datasets:")
        for col, datasets in id_columns.items():
            if len(datasets) > 1:
                print(f"{col}: {datasets}")

    def generate_summary_report(self):
        """Generate a comprehensive summary report"""
        print("\n" + "="*50)
        print("NBA DATASET EXPLORATION SUMMARY (FAST VERSION)")
        print("="*50)

        # Load all data
        self.load_all_csv_files()

        # Create overview
        overview = self.create_data_overview()

        # Analyze specific data types
        self.analyze_player_data()
        self.analyze_game_data()
        self.analyze_draft_data()
        self.analyze_team_data()

        # Find relationships
        self.find_relationships()

        # Explore SQLite database
        self.explore_sqlite_database()

        print("\n" + "="*50)
        print("EXPLORATION COMPLETE")
        print("="*50)

        return overview

if __name__ == "__main__":
    explorer = NBADatasetExplorer()
    overview = explorer.generate_summary_report()
