import pandas as pd
import numpy as np
from pathlib import Path
import warnings

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

import joblib
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")

class NBAPredictor:
    def __init__(self, data_path="../data"):
        self.data_path = Path(__file__).parent.parent.parent / "data"
        self.features_path = Path(__file__).parent.parent / "features"
        self.models_path = Path(__file__).parent
        self.models_path.mkdir(exist_ok=True)

    def load_enhanced_data(self):
        print("Loading enhanced features...")
        games = pd.read_csv(self.features_path / "enhanced_features.csv")
        games["game_date"] = pd.to_datetime(games["game_date"])
        return games

    def prepare_features(self, games):
        print("Preparing features for ML...")

        feature_columns = [
            'total_points', 'fg_pct_diff', 'fg3_pct_diff',
            'reb_diff', 'ast_diff', 'tov_diff', 'stl_diff', 'blk_diff',
            'q1_diff', 'q2_diff', 'q3_diff', 'q4_diff', 'paint_diff', 'fb_diff',
            'active_players_diff', 'avg_exp_diff', 'guards_diff',
            'rolling_ppg', 'rolling_win_rate', 'h2h_win_rate', 'h2h_games_played',
            'home_days_rest', 'away_days_rest', 'home_efficiency', 'away_efficiency',
            'efficiency_diff', 'game_pace', 'season_win_rate_diff', 'season_ppg_diff',
            'month', 'day_of_week', 'is_weekend', 'is_playoff_month'
        ]

        available_features = [col for col in feature_columns if col in games.columns]
        print(f"Using {len(available_features)} features: {available_features}")

        X = games[available_features].copy()
        y = games["home_win"]

        missing_mask = X.isnull().any(axis=1) | y.isnull()
        X = X[~missing_mask]
        y = y[~missing_mask]

        print(f"Dataset shape: {X.shape}")
        print(f"Target distribution: {y.value_counts().to_dict()}")

        return X, y, available_features

    def train_models(self, X, y):
        print("Training models...")

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        models = {
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000)
        }

        results = {}

        for name, model in models.items():
            print(f"Training {name}...")

            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]

            accuracy = accuracy_score(y_test, y_pred)
            cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')

            results[name] = {
                'model': model,
                'accuracy': accuracy,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'y_pred': y_pred,
                'y_pred_proba': y_pred_proba,
                'feature_importance': self.get_feature_importance(model, X.columns) if hasattr(model, 'feature_importances_') else None
            }

            print(f"{name} - Accuracy: {accuracy:.3f}, CV: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")

        return results, X_test, y_test

    def get_feature_importance(self, model, feature_names):
        if hasattr(model, 'feature_importances_'):
            importance = model.feature_importances_
            return dict(zip(feature_names, importance))
        return None

    def save_best_model(self, results):
        best_model_name = max(results.keys(), key=lambda k: results[k]['accuracy'])
        best_model = results[best_model_name]['model']

        model_file = self.models_path / "nba_predictor_model.pkl"
        joblib.dump(best_model, model_file)

        print(f"Saved best model ({best_model_name}) to {model_file}")
        return best_model_name

    def create_model_report(self, results, X_test, y_test):
        print("Creating model report...")

        report_file = self.models_path / "model_report.txt"
        with open(report_file, 'w') as f:
            f.write("NBA Game Prediction Model Report\n")
            f.write("================================\n\n")

            for name, result in results.items():
                f.write(f"{name}:\n")
                f.write(f"  Accuracy: {result['accuracy']:.3f}\n")
                f.write(f"  Cross-validation: {result['cv_mean']:.3f} (+/- {result['cv_std'] * 2:.3f})\n")
                f.write(f"  Classification Report:\n")
                f.write(classification_report(y_test, result['y_pred']))
                f.write("\n")

                if result['feature_importance']:
                    f.write("  Top 10 Features:\n")
                    sorted_features = sorted(result['feature_importance'].items(),
                                          key=lambda x: x[1], reverse=True)[:10]
                    for feature, importance in sorted_features:
                        f.write(f"    {feature}: {importance:.4f}\n")
                f.write("\n" + "="*50 + "\n\n")

    def create_feature_importance_plot(self, results):
        print("Creating feature importance plot...")

        best_model_name = max(results.keys(), key=lambda k: results[k]['accuracy'])
        best_result = results[best_model_name]

        if best_result['feature_importance']:
            sorted_features = sorted(best_result['feature_importance'].items(),
                                  key=lambda x: x[1], reverse=True)[:15]

            features, importances = zip(*sorted_features)

            plt.figure(figsize=(12, 8))
            plt.barh(range(len(features)), importances)
            plt.yticks(range(len(features)), features)
            plt.xlabel('Feature Importance')
            plt.title(f'Top 15 Features - {best_model_name}')
            plt.gca().invert_yaxis()
            plt.tight_layout()

            plot_file = self.models_path / "feature_importance.png"
            plt.savefig(plot_file, dpi=300, bbox_inches='tight')
            plt.close()

            print(f"Saved feature importance plot to {plot_file}")

    def run(self):
        try:
            games = self.load_enhanced_data()

            X, y, feature_names = self.prepare_features(games)

            results, X_test, y_test = self.train_models(X, y)

            best_model_name = self.save_best_model(results)

            self.create_model_report(results, X_test, y_test)
            self.create_feature_importance_plot(results)

            print(f"\n🎉 Model training complete!")
            print(f"Best model: {best_model_name}")
            print(f"Best accuracy: {results[best_model_name]['accuracy']:.3f}")

            return results, best_model_name

        except Exception as e:
            import traceback
            traceback.print_exc()
            raise


if __name__ == "__main__":
    predictor = NBAPredictor()
    results, best_model = predictor.run()
