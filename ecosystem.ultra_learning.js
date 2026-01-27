module.exports = {
  apps: [{
    name: 'UltraLearning',
    script: 'ultra_learning_generator.py',
    interpreter: 'python3',
    cron_restart: '0 3,15 * * *',  // 3:00 AM i 3:00 PM (2× dziennie)
    autorestart: false,
    watch: false,
    max_memory_restart: '300M',
    instances: 1
  }]
}
