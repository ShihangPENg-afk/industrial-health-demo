# Industrial Health Demo

第 7 周工业预测 Mini Demo：基于 scikit-learn 的制造质量分类项目。

## 项目结构

```
industrial-health-demo/
├── data/
│   ├── raw/                  # 原始数据
│   └── processed/            # 清洗后的训练数据（Day2）
├── scripts/
│   ├── eda.py                # 探索性数据分析
│   ├── train_model.py        # 模型训练（Day2）
│   └── sample_predict.py     # 本地预测示例（Day2）
├── app/                      # 推理 API（后续）
├── artifacts/                # 模型与指标产物（Day2）
├── docs/                     # 文档与 EDA 报告
└── tests/                    # API 测试（后续）
```

## 快速开始

```bash
pip install -r requirements.txt
python scripts/eda.py
```

运行后会在 `docs/eda_summary.md` 生成 EDA 报告。

## Day1 任务

- [x] 项目骨架与依赖
- [x] 读取 `data/raw/manufacturing_quality.csv` 并做 EDA
- [ ] 模型训练（Day2）

## 数据说明

`manufacturing_quality.csv` 包含产线传感器特征与 `target` 标签：

- `0`：合格批次
- `1`：不合格批次

特征包括温度、压力、振动、湿度、线速、刀具磨损、功率等。
