### Hexlet tests and linter status:
[![Actions Status](https://github.com/Goglich/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Goglich/python-project-52/actions)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Goglich_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Goglich_python-project-52)

### Production Build:
([Product](https://python-project-52-p25m.onrender.com/))


### Requirements
```
- Python 3.11+
- PostgreSQL 15+
- [uv](https://github.com/astral-sh/uv) package manager
```


### Installation  & Launching
1. Clone the repo:
```bash
git clone https://github.com/Goglich/python-project-52.git
cd python-project-52
```
2. Install dependencies:
```bash
make install
```
3. Create `.env` file in the root directory:
```bash
SECRET_KEY=your_secret_key
DEBUG=True  # Set to False in production
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
```
Replace username, password, dbname, and your_secret_key with your own values.

4. Build & Run the application:
```bash
make build
make start
```