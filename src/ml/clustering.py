import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib

MODEL_PATH = "models/kmeans_traffic.pkl"

def train_clustering_model(csv_path):

    df = pd.read_csv(csv_path)

    features = df[[
        "car",
        "motorcycle",
        "bus",
        "truck",
        "person",
        "total"
    ]]

    scaler = StandardScaler()

    X = scaler.fit_transform(features)

    kmeans = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )

    kmeans.fit(X)

    df["cluster"] = kmeans.labels_

    cluster_summary = (
        df.groupby("cluster")["total"]
        .mean()
        .sort_values()
    )

    print("\nCluster Summary:")
    print(cluster_summary)

    joblib.dump({
        "model": kmeans,
        "scaler": scaler
    }, MODEL_PATH)

    print(f"\nModel saved: {MODEL_PATH}")

    return df

if __name__ == "__main__":

    result = train_clustering_model(
        "data/processed/ml_input/part-00000*.csv"
    )

    print(result.head())