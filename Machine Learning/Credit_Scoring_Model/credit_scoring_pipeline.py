
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (classification_report, roc_auc_score, roc_curve,
                             accuracy_score, precision_score, recall_score, f1_score)
import joblib

def main():
    # Load or generate data
    try:
        df = pd.read_csv("credit_data.csv")
    except FileNotFoundError:
        np.random.seed(42)
        n = 500
        data = {
            "age": np.random.randint(18, 70, n),
            "income": np.random.randint(20000, 150000, n),
            "debts": np.random.randint(0, 80000, n),
            "loan_amount": np.random.randint(1000, 50000, n),
            "credit_history_length": np.random.randint(1, 30, n),
            "previous_defaults": np.random.randint(0, 5, n),
            "payment_history": np.random.randint(50, 100, n),
        }
        df = pd.DataFrame(data)
        df["debt_to_income"] = df["debts"] / (df["income"] + 1)
        df["on_time_ratio"] = df["payment_history"] / 100
        df["creditworthy"] = (
            (df["income"] > 40000) &
            (df["debt_to_income"] < 0.4) &
            (df["previous_defaults"] < 2) &
            (df["on_time_ratio"] > 0.7)
        ).astype(int)
        df.to_csv("credit_data.csv", index=False)

    # Train/test split
    X = df.drop(columns=["creditworthy"])
    y = df["creditworthy"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Scale numeric features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000),
        "DecisionTree": DecisionTreeClassifier(random_state=42),
        "RandomForest": RandomForestClassifier(n_estimators=300, random_state=42)
    }

    metrics_rows = []
    roc_curves = {}

    for name, model in models.items():
        if name == "LogisticRegression":
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            y_proba = model.predict_proba(X_test_scaled)[:, 1]
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_proba = model.predict_proba(X_test)[:, 1]

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        roc = roc_auc_score(y_test, y_proba)

        metrics_rows.append({
            "model": name, "accuracy": acc, "precision": prec,
            "recall": rec, "f1_score": f1, "roc_auc": roc
        })

        fpr, tpr, _ = roc_curve(y_test, y_proba)
        roc_curves[name] = (fpr, tpr)

        joblib.dump(model, f"model_{name.lower()}.joblib")

    joblib.dump(scaler, "scaler.joblib")

    metrics_df = pd.DataFrame(metrics_rows).sort_values("roc_auc", ascending=False).reset_index(drop=True)
    metrics_df.to_csv("metrics.csv", index=False)

    with open("classification_reports.txt", "w") as f:
        for name, model in models.items():
            if name == "LogisticRegression":
                y_pred = model.predict(X_test_scaled)
            else:
                y_pred = model.predict(X_test)
            f.write(f"=== {name} ===\n")
            f.write(classification_report(y_test, y_pred))
            f.write("\n\n")

    plt.figure()
    for name, (fpr, tpr) in roc_curves.items():
        plt.plot(fpr, tpr, label=name)
    plt.plot([0, 1], [0, 1], linestyle="--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curves - Credit Scoring Models")
    plt.legend()
    plt.savefig("roc_curves.png", bbox_inches="tight")
    plt.close()

    print("Done. Files saved: credit_data.csv, metrics.csv, classification_reports.txt, roc_curves.png, model_*.joblib, scaler.joblib")

if __name__ == "__main__":
    main()
