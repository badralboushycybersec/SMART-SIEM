# SMART-SIEM

SMART-SIEM is a research repository for building and evaluating a machine-learning–assisted correlation/classification pipeline on top of Wazuh SIEM alerts. The core idea is to enrich an incoming alert with recent “context” (history) from Elasticsearch, then run a two-stage CatBoost classifier:

- Stage 1: NORMAL vs ATTACK
- Stage 2: If ATTACK, predict the attack class (MITRE technique IDs such as T1212, T1068, …)

This repository contains datasets, experiment notebooks, and Python scripts that connect Wazuh/Kafka/Elasticsearch to run inference and (optionally) retrain models.

## Repository Structure

- [datasets](file:///d:/SIEM%20Paper/SMART-SIEM/datasets): CSV datasets used for training/testing, including variants with different history lengths.
- [jupyter notbooks](file:///d:/SIEM%20Paper/SMART-SIEM/jupyter%20notbooks): Jupyter notebooks for dataset creation and experiments (folder name is intentionally spelled as in the repo).
- [retrain scripts](file:///d:/SIEM%20Paper/SMART-SIEM/retrain%20scripts): Runtime pipeline (producer/consumer) and retraining utilities.

Each folder contains its own README.md with more details.

## How The Pipeline Works

1. A UDP listener receives Wazuh alert messages and publishes selected events to Kafka ([producer.py](file:///d:/SIEM%20Paper/SMART-SIEM/retrain%20scripts/producer.py)).
2. A Kafka consumer receives those messages, normalizes the JSON, and waits until the corresponding record is available in Elasticsearch ([consumer.py](file:///d:/SIEM%20Paper/SMART-SIEM/retrain%20scripts/consumer.py)).
3. The consumer queries Elasticsearch for recent history for the same `data.srcip`, adds history-based features, and runs inference using two CatBoost models ([attack_classifier.py](file:///d:/SIEM%20Paper/SMART-SIEM/retrain%20scripts/attack_classifier.py)).
4. The predicted outputs are written back to an Elasticsearch index (default: `wazuh-ai-correlation`).

## Requirements

The scripts are plain Python files (not a packaged module). You will need a working Python environment plus services:

- Python 3.x
- Kafka (and a topic configured for Wazuh alerts)
- Elasticsearch (used for context lookup + writing prediction results)

Python dependencies (as used by the scripts):

```bash
pip install pandas numpy scikit-learn catboost kafka-python elasticsearch
```

## Configuration

Edit [config.py](file:///d:/SIEM%20Paper/SMART-SIEM/retrain%20scripts/config.py) to match your environment:

- `kafka_bootstrap_server`, `kafka_topic`, `consumer_client_id`
- `elasticsearch_ip`, `elasticsearch_port`, `elasticsearch_user`, `elasticsearch_password`
- `index_name` (destination index for predicted results)
- `Wazuh_broadcasting_port` (UDP port the producer listens on)
- `path_model_1`, `path_model_2` (paths to CatBoost model binaries)

Note: this repo references `../models/*.bin` but a `models/` directory is not present here. You need to provide trained CatBoost model files at the configured paths.

## Running

From the [retrain scripts](file:///d:/SIEM%20Paper/SMART-SIEM/retrain%20scripts) folder:

```bash
python producer.py
```

In a separate terminal:

```bash
python consumer.py
```

The consumer expects that Wazuh alerts are indexed into Elasticsearch (it queries `wazuh-alerts-*`) and will write predictions into `index_name`.

## Retraining (Optional)

The retraining utilities are in:

- [ai_adaptive_retrain.py](file:///d:/SIEM%20Paper/SMART-SIEM/retrain%20scripts/ai_adaptive_retrain.py): scans the “knowledge base” index and can train new CatBoost models.

The current code has model saving commented out; review and enable saving only if you intend to overwrite your deployed models.
