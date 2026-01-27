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
    }
  ]
};
