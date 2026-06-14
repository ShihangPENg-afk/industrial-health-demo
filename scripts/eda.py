"""Exploratory data analysis for manufacturing quality classification."""

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "manufacturing_quality.csv"
OUTPUT_PATH = PROJECT_ROOT / "docs" / "eda_summary.md"
TARGET_COLUMN = "target"


def load_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def build_summary(df: pd.DataFrame) -> str:
    lines: list[str] = [
        "# Manufacturing Quality EDA Summary",
        "",
        f"- Source file: `{RAW_DATA_PATH.relative_to(PROJECT_ROOT)}`",
        "- Task: manufacturing quality classification (`target`)",
        "",
        "## Dataset Shape",
        "",
        f"- Rows: **{len(df):,}**",
        f"- Columns: **{len(df.columns):,}**",
        "",
        "## Column Types",
        "",
        "| Column | Dtype |",
        "| --- | --- |",
    ]

    for column, dtype in df.dtypes.items():
        lines.append(f"| {column} | `{dtype}` |")

    missing = df.isna().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame(
        {"Missing Count": missing, "Missing %": missing_pct}
    )
    missing_df = missing_df[missing_df["Missing Count"] > 0].sort_values(
        "Missing Count", ascending=False
    )

    lines.extend(["", "## Missing Values", ""])
    if missing_df.empty:
        lines.append("No missing values detected.")
    else:
        lines.extend(
            [
                "| Column | Missing Count | Missing % |",
                "| --- | ---: | ---: |",
            ]
        )
        for column, row in missing_df.iterrows():
            lines.append(
                f"| {column} | {int(row['Missing Count'])} | {row['Missing %']:.2f}% |"
            )

    target_counts = df[TARGET_COLUMN].value_counts(dropna=False).sort_index()
    lines.extend(
        [
            "",
            f"## Target Distribution (`{TARGET_COLUMN}`)",
            "",
            "| Target | Count | Percentage |",
            "| --- | ---: | ---: |",
        ]
    )
    for value, count in target_counts.items():
        pct = count / len(df) * 100
        lines.append(f"| {value} | {count:,} | {pct:.2f}% |")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    describe = df[numeric_cols].describe().T
    describe = describe.rename(
        columns={
            "count": "Count",
            "mean": "Mean",
            "std": "Std",
            "min": "Min",
            "25%": "25%",
            "50%": "50%",
            "75%": "75%",
            "max": "Max",
        }
    )

    lines.extend(
        [
            "",
            "## Numeric Feature Statistics",
            "",
            "| Column | Count | Mean | Std | Min | 25% | 50% | 75% | Max |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for column, row in describe.iterrows():
        lines.append(
            "| {column} | {count:.0f} | {mean:.3f} | {std:.3f} | {min:.3f} | "
            "{p25:.3f} | {p50:.3f} | {p75:.3f} | {max:.3f} |".format(
                column=column,
                count=row["Count"],
                mean=row["Mean"],
                std=row["Std"],
                min=row["Min"],
                p25=row["25%"],
                p50=row["50%"],
                p75=row["75%"],
                max=row["Max"],
            )
        )

    lines.append("")
    return "\n".join(lines)


def print_summary(df: pd.DataFrame) -> None:
    print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
    print("\nColumn types:")
    print(df.dtypes.to_string())

    missing = df.isna().sum()
    print("\nMissing values:")
    if missing.sum() == 0:
        print("No missing values detected.")
    else:
        print(missing[missing > 0].to_string())

    print(f"\nTarget distribution ({TARGET_COLUMN}):")
    print(df[TARGET_COLUMN].value_counts(dropna=False).sort_index().to_string())

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    print("\nNumeric feature statistics:")
    print(df[numeric_cols].describe().to_string())


def main() -> None:
    df = load_data(RAW_DATA_PATH)
    print_summary(df)

    summary = build_summary(df)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(summary, encoding="utf-8")
    print(f"\nEDA summary saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
