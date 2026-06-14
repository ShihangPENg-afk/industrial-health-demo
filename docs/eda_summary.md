# Manufacturing Quality EDA Summary

- Source file: `data/raw/manufacturing_quality.csv`
- Task: manufacturing quality classification (`target`)

## Dataset Shape

- Rows: **800**
- Columns: **9**

## Column Types

| Column | Dtype |
| --- | --- |
| batch_id | `str` |
| temperature_c | `float64` |
| pressure_bar | `float64` |
| vibration_mm_s | `float64` |
| humidity_pct | `float64` |
| line_speed_mpm | `float64` |
| tool_wear_pct | `float64` |
| power_kw | `float64` |
| target | `int64` |

## Missing Values

| Column | Missing Count | Missing % |
| --- | ---: | ---: |
| temperature_c | 6 | 0.75% |
| pressure_bar | 6 | 0.75% |

## Target Distribution (`target`)

| Target | Count | Percentage |
| --- | ---: | ---: |
| 0 | 624 | 78.00% |
| 1 | 176 | 22.00% |

## Numeric Feature Statistics

| Column | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| temperature_c | 794 | 71.874 | 4.438 | 58.660 | 68.769 | 71.961 | 74.783 | 85.112 |
| pressure_bar | 794 | 5.172 | 0.612 | 3.011 | 4.780 | 5.193 | 5.566 | 7.107 |
| vibration_mm_s | 800 | 2.053 | 0.806 | -0.351 | 1.523 | 2.108 | 2.584 | 4.431 |
| humidity_pct | 800 | 48.293 | 7.007 | 27.969 | 43.347 | 48.070 | 53.268 | 69.417 |
| line_speed_mpm | 800 | 119.824 | 14.770 | 78.758 | 109.612 | 119.457 | 129.499 | 166.328 |
| tool_wear_pct | 800 | 48.656 | 25.632 | 5.083 | 26.811 | 48.116 | 70.674 | 94.974 |
| power_kw | 800 | 18.459 | 2.167 | 11.657 | 16.926 | 18.495 | 19.916 | 25.631 |
| target | 800 | 0.220 | 0.415 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 |
