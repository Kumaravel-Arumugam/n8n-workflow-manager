# Job Market Analysis Engine

**Workflow ID:** GDeQD6XpAGoHASTo
**Created:** Jan 2026
**Status:** active

## Purpose
Analyzes job market data from PostgreSQL, generates skill/experience charts, and sends reports via Telegram with AI narration.

## Inputs
- `telegram_chat_id`: Target chat for report
- `role_name`: Job role to analyze

## Outputs
- Text report with market insights
- 4 charts (Skills, Experience Distribution, Categories, Demand Curve)

## Version History
- v8 (current): Fixed role naming, improved captions
- v7: Fixed regex escaping
- v6: Added experience demand curve
- v1-v5: Initial development
