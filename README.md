# Sber-Monitoring-App

## Set up & Installation.

### 1 .Clone/Fork the git repo
          
```bash
git clone https://github.com/motvy/monitoring_api.git
cd Sber-Monitoring-App

```

### 2. Install the requirements

```
pip install -r requirements.txt
```

### 3. Run the application

`python manage.py`

### 4. Test the application

`python -m pytest`

## OR

### 1 .Clone/Fork the git repo
          
```bash
git clone https://github.com/motvy/monitoring_api.git
cd Sber-Monitoring-App

```

### 2. Build a Docker Image

`docker build --tag monitoring_app .`

### 3. Run a Docker Image as a container

`docker run --name monitoring_app -p 5000:5000 monitoring_app`

### 4. Test the application

`docker exec monitoring_app pytest`
