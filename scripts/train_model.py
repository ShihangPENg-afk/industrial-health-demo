"""Train a manufacturing quality classification model."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "manufacturing_quality.csv"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
MODEL_PATH = ARTIFACTS_DIR / "model.pkl"
METRICS_PATH = ARTIFACTS_DIR / "metrics.json"
SCHEMA_PATH = ARTIFACTS_DIR / "schema.json"

# 若 CSV 中没有 `target` 列，请改为实际目标列名
TARGET_COLUMN = "target"

TEST_SIZE = 0.2
RANDOM_STATE = 42


def resolve_target_column(df: pd.DataFrame) -> str:
    if "target" in df.columns:
        return "target"
    if TARGET_COLUMN in df.columns:
        return TARGET_COLUMN
    raise ValueError(
        "未找到目标列。请确认 CSV 含 `target` 列，"
        f"或修改脚本中的 TARGET_COLUMN（当前值：{TARGET_COLUMN!r}）。"
    )


def build_preprocessor(
    numeric_features: list[str],
    categorical_features: list[str],
) -> ColumnTransformer:
    numeric_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_features),
            ("cat", categorical_pipeline, categorical_features),
        ]
    )


def main() -> None:
    if not RAW_PATH.exists():
        raise FileNotFoundError(
            f"未找到数据文件：{RAW_PATH}。请先将 CSV 放到 data/raw/ 下。"
        )

    df = pd.read_csv(RAW_PATH)
    target_col = resolve_target_column(df)

    before_rows = len(df)
    df = df.dropna(subset=[target_col]).copy()
    dropped_rows = before_rows - len(df)
    if dropped_rows:
        print(f"已删除 target 为空的行：{dropped_rows} 行")

    feature_cols = [col for col in df.columns if col != target_col]
    numeric_features = df[feature_cols].select_dtypes(include="number").columns.tolist()
    categorical_features = [
        col for col in feature_cols if col not in numeric_features
    ]

    X = df[feature_cols]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    model = Pipeline(
        [
            (
                "preprocessor",
                build_preprocessor(numeric_features, categorical_features),
            ),
            (
                "classifier",
                RandomForestClassifier(random_state=RANDOM_STATE),
            ),
        ]
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    f1_macro = f1_score(y_test, y_pred, average="macro")
    report = classification_report(y_test, y_pred, output_dict=True)

    print(f"Target column: {target_col}")
    print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1 macro: {f1_macro:.4f}")
    print("\nClassification report:")
    print(classification_report(y_test, y_pred))

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    METRICS_PATH.write_text(
        json.dumps(
            {
                "accuracy": accuracy,
                "f1_macro": f1_macro,
                "classification_report": report,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    schema = {
        "target_column": target_col,
        "feature_columns": feature_cols,
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
        "classes": sorted(y.unique().tolist()),
        "model_type": "RandomForestClassifier",
        "test_size": TEST_SIZE,
        "random_state": RANDOM_STATE,
    }
    SCHEMA_PATH.write_text(
        json.dumps(schema, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"\n✅ 模型已保存：{MODEL_PATH}")
    print(f"✅ 指标已保存：{METRICS_PATH}")
    print(f"✅ Schema 已保存：{SCHEMA_PATH}")


if __name__ == "__main__":
    main()
