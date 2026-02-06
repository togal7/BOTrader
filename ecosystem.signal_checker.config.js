module.exports = {
  apps: [{
    name: 'SignalChecker',
    script: 'signal_results_checker.py',
    interpreter: 'python3',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '500M',
    error_file: './logs/signal_checker_error.log',
    out_file: './logs/signal_checker_out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss',
    env: {
      PYTHONUNBUFFERED: '1'
    }
  }]
};
