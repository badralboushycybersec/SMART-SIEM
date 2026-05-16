# Datasets

This folder contains the CSV datasets used in SMART-SIEM experiments and the auxiliary “knowledge base” dataset.

## Key Files

- `dataset.csv`: original dataset without history/context and without SMOTE-NC.
- `ai_knowledge_base.csv`: combined dataset (training-with-history with SMOTE applied + testing-with-history without SMOTE). The default history depth used in experiments is 15 previous records.
- `dataset_with_history_*.csv`: dataset variants with different history lengths.
- `Readme.txt`: the original dataset notes shipped with this repo (kept as-is).

## Subfolders

- [training](file:///d:/SIEM%20Paper/SMART-SIEM/datasets/training): training splits (with history, SMOTE applied) for multiple history lengths.
- [testing](file:///d:/SIEM%20Paper/SMART-SIEM/datasets/testing): testing splits (with history, without SMOTE) for multiple history lengths.
