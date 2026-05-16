# Retrain / Runtime Scripts

This folder contains the runtime pipeline and utilities for inference and (optionally) adaptive retraining.

## Main Entry Points

- [producer.py](file:///d:/SIEM%20Paper/SMART-SIEM/retrain%20scripts/producer.py): UDP syslog listener that publishes selected Wazuh alert messages to Kafka (`wazuh_alerts`).
- [consumer.py](file:///d:/SIEM%20Paper/SMART-SIEM/retrain%20scripts/consumer.py): Kafka consumer that:
  - normalizes incoming Wazuh JSON,
  - waits until the corresponding alert appears in Elasticsearch,
  - fetches recent history for the same `data.srcip`,
  - runs the two-stage CatBoost classifier,
  - writes predictions back to Elasticsearch.

## Model Inference

- [attack_classifier.py](file:///d:/SIEM%20Paper/SMART-SIEM/retrain%20scripts/attack_classifier.py): preprocessing + history feature aggregation + labeling using two CatBoost models.
- [features.py](file:///d:/SIEM%20Paper/SMART-SIEM/retrain%20scripts/features.py): feature lists used by the model (including history counters and MITRE technique IDs).

## Elasticsearch Utilities

- [elastic_utilities.py](file:///d:/SIEM%20Paper/SMART-SIEM/retrain%20scripts/elastic_utilities.py): connect/query/write helpers and index mappings (`catboost_ai_settings`).

## Adaptive Retraining (Optional)

- [ai_adaptive_retrain.py](file:///d:/SIEM%20Paper/SMART-SIEM/retrain%20scripts/ai_adaptive_retrain.py): scans the knowledge-base index and can train new models.
- [add_to_knowledge_base.py](file:///d:/SIEM%20Paper/SMART-SIEM/retrain%20scripts/add_to_knowledge_base.py): utilities for extending the knowledge base (if used in your workflow).

## Configuration

All runtime endpoints, credentials, and model paths are configured in [config.py](file:///d:/SIEM%20Paper/SMART-SIEM/retrain%20scripts/config.py).
