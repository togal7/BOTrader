#!/bin/bash
cd /bots/BOTrader

# Backup wiedzy
tar -czf "knowledge_backup_$(date +%Y%m%d_%H%M).tar.gz" \
  ai_signals_history.json \
  ai_signals_results.json \
  user_data.json 2>/dev/null

# Commit do GitHub
git add ai_signals_history.json ai_signals_results.json user_data.json
git commit -m "Auto-backup: $(date +%Y-%m-%d\ %H:%M) - $(wc -l < ai_signals_history.json) signals"
git push https://YOUR_GITHUB_TOKEN_HERE@github.com/togal7/BOTrader.git master

# Cleanup old backups (keep last 7 days)
find . -name "knowledge_backup_*.tar.gz" -mtime +7 -delete

