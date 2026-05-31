from src.ml.clustering import train_clustering_model
from src.ml.forecasting import train_forecasting_model

DATASET_PATH = "data/processed/ml_input/part-00000*.csv"

def run_training():

    print("=" * 50)
    print("TRAINING CLUSTERING")
    print("=" * 50)

    train_clustering_model(DATASET_PATH)

    print("\n")

    print("=" * 50)
    print("TRAINING FORECASTING")
    print("=" * 50)

    train_forecasting_model(DATASET_PATH)

    print("\nALL TRAINING FINISHED")

if __name__ == "__main__":
    run_training()