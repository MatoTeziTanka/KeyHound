# KeyHound Operations

## Services (VM191 puzzle-keyhound)
- keyhound-solver@1..4.service: CPU workers (defaults to first unsolved puzzle)
- keyhound-dashboard.service: Remote stats (HTTP 5050)
- keyhound-throughput.service: Throughput API (HTTP 5051)
- keyhound-checkpoint.timer: Checkpoints every 30 minutes (runs keyhound-checkpoint.service)

## Ports
- 22: SSH
- 5050: Dashboard (HTTP)
- 5051: Throughput API (HTTP)

## Environment
- SMTP_PASSWORD: Gmail app password for lightspeedup.smtp@gmail.com
- ALERT_EMAILS: comma-separated recipients
- PUZZLE_BITS: optional; set to a specific bits value (e.g., 67). If unset or set to `auto`, KeyHound auto-selects the first unsolved target.

## Common commands
```bash
# Status
systemctl --no-pager --type=service | egrep 'keyhound-(solver@|dashboard|throughput)'
systemctl list-timers | grep keyhound

# Restart services
sudo systemctl restart keyhound-solver@1.service
sudo systemctl restart keyhound-dashboard.service
sudo systemctl restart keyhound-throughput.service

# Manual checkpoint
sudo systemctl start keyhound-checkpoint.service
ls -1 ~/KeyHound/checkpoints | tail -n 1

# Logs
journalctl -u keyhound-dashboard.service -n 100 --no-pager
journalctl -u keyhound-throughput.service -n 100 --no-pager
```

## Reboot flow
1. Reboot VM: `sudo reboot`
2. Verify services auto-start:
```bash
systemctl --no-pager --type=service | egrep 'keyhound-(solver@|dashboard|throughput)'
systemctl list-timers | grep keyhound
curl -s http://127.0.0.1:5050/api/health
```
3. Open dashboard: `http://192.168.12.191:5050`

## Backups/checkpoints
- Automatic every 30 minutes to `~/KeyHound/checkpoints/<timestamp>/`
- Manual trigger: `sudo systemctl start keyhound-checkpoint.service`
