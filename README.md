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
│   ├── train_model.py        # 模型训练（Day2/Day3）
│   ├── start_mlflow_ui.sh    # 启动 MLflow UI（Day3）
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

### 模型训练与 MLflow

```bash
python scripts/train_model.py
```

训练完成后会写入：

- `artifacts/`：模型与指标文件
- `mlflow.db`：本地 MLflow 实验记录（SQLite，已加入 `.gitignore`）

启动 MLflow UI 查看实验：

```bash
bash scripts/start_mlflow_ui.sh
```

默认地址：<http://127.0.0.1:5001>。可通过环境变量修改 host/port：

```bash
MLFLOW_UI_HOST=0.0.0.0 MLFLOW_UI_PORT=5001 bash scripts/start_mlflow_ui.sh
```

## Day1 任务

- [x] 项目骨架与依赖
- [x] 读取 `data/raw/manufacturing_quality.csv` 并做 EDA
- [x] 模型训练（Day2）
- [x] MLflow 实验记录（Day3）

## Docker 部署（Day5）

使用 Docker 启动推理 API（需已存在 `artifacts/` 模型产物）：

```bash
docker compose up --build -d
```

或使用 Makefile：

```bash
make docker-up
```

验证服务：

```bash
curl http://127.0.0.1:8010/health
curl http://127.0.0.1:8010/model-info
python scripts/sample_predict.py
```

一键验收：

```bash
make docker-verify
```

查看日志与停止：

```bash
docker compose logs -f industrial-health-api
docker compose down
```

镜像仅包含 `app/`、`artifacts/`、`scripts/` 与运行依赖，不会打包 `.venv`、`.env`、`mlflow.db`、`mlruns/` 及训练数据目录。

## 数据说明

`manufacturing_quality.csv` 包含产线传感器特征与 `target` 标签：

- `0`：合格批次
- `1`：不合格批次

特征包括温度、压力、振动、湿度、线速、刀具磨损、功率等。
