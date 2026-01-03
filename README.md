# Dayflow HRMS - Hackathon Setup

## 1. Start Database Service
Before running Odoo, ensure PostgreSQL is active.

### Linux / MacOS (Standard)
```bash
sudo service postgresql start
```
*Note: On MacOS with Homebrew, you might use: `brew services start postgresql`*

### Windows
Start **PostgreSQL** service from the Services panel.

## 2. Run Odoo Server
```bash
./odoo-bin -c odoo.conf -u dayflow
```

## 3. Access
Open Browser: [http://localhost:8069](http://localhost:8069)
*   User: `admin`
*   Password: `admin`
