# Packaging and Deployment

## Python packaging
- Install in virtualenv (editable):
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```
- CLI: current entrypoint is via `python3 main.py`. A `console_scripts` shim can be added later after aligning package layout.

## Systemd services (VM191)
- Solver workers:
```bash
sudo systemctl enable --now keyhound-solver@1.service
sudo systemctl enable --now keyhound-solver@2.service
sudo systemctl enable --now keyhound-solver@3.service
sudo systemctl enable --now keyhound-solver@4.service
```
- Dashboard (HTTP 5050):
```bash
sudo systemctl enable --now keyhound-dashboard.service
```
- Throughput API (HTTP 5051):
```bash
sudo systemctl enable --now keyhound-throughput.service
```
- Checkpoints every 30 minutes:
```bash
sudo systemctl enable --now keyhound-checkpoint.timer
```

## Environment configuration
```bash
# Email alerts
export SMTP_PASSWORD='<gmail_app_password>'
export ALERT_EMAILS='sethpizzaboy@aol.com,sethpizzaboy@gmail.com,setsch0666@students.ecpi.edu'
```
For persistence across reboots, set these in the service Environment= or a systemd drop‑in file (see OPERATIONS.md).

## Firewall (UFW)
```bash
sudo ufw allow 5050/tcp
sudo ufw allow 5051/tcp
```

## Backups / checkpoints
- Automatic via `keyhound-checkpoint.timer` to `~/KeyHound/checkpoints/`.
- Manual trigger: `sudo systemctl start keyhound-checkpoint.service`.
