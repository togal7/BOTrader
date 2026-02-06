module.exports = {
  apps: [
    {
      name: 'BOTrader',
      script: 'bot.py',
      interpreter: 'python3',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      env: { PYTHONUNBUFFERED: '1' }
    },
    {
      name: 'AlertWorker',
      script: 'alert_worker.py',
      interpreter: 'python3',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '300M',
      env: { PYTHONUNBUFFERED: '1' }
    },
    {
      name: 'AlertSender',
      script: 'alert_sender.py',
      interpreter: 'python3',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '200M',
      env: { PYTHONUNBUFFERED: '1' }
    },
    {
      name: 'SignalChecker',
      script: 'signal_checker.py',
      interpreter: 'python3',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '200M',
      env: { PYTHONUNBUFFERED: '1' }
    },
    {
      name: 'BOT_LEARNING',
      script: 'bot_learning.py',
      interpreter: 'python3',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '300M',
      env: { PYTHONUNBUFFERED: '1' },
      cron_restart: '0 */2 * * *'
    },
    {
      name: 'ULTRA_LEARNING',
      script: 'ultra_learning_generator.py',
      interpreter: 'python3',
      instances: 1,
      autorestart: false,
      watch: false,
      max_memory_restart: '400M',
      env: { PYTHONUNBUFFERED: '1' },
      cron_restart: '0 0,6,12,18 * * *'
    }
  ]
};
