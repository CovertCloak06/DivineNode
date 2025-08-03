# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### ✨ Added
- `/generate` endpoint powered by the new LLM util  
- `/summarize` and `/code-complete` endpoints  
- SQLite persistence layer scaffold (`src/db.py`)

### 🛠 Changed
- CI workflows renamed from “Inexora” → “DivineNode”  
- Pre-commit now ignores `.venv/`, `build/`, `dist/`  
- Bumped Android `versionCode`/`versionName` in `app/build.gradle` to 1.0.1  

### 🐛 Fixed
- Import error in `src/serve.py` (added `Session`)  
- All lint/mypy/pre-commit errors resolved  

## [1.0.1] – 2025-08-03

### ✨ Added
- Release notes and changelog scaffolding  

### 🛠 Changed
- CI workflows display names updated  

### 🐛 Fixed
- None

## [1.0.0] – *initial release*

- First public version
