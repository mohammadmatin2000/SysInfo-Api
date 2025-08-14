<h1 align="center"> 🖥️ SysInfo-Api
</h1>
<p align="center">
  
<a href="https://www.python.org" target="_blank" rel="noreferrer">
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="Python" width="40" height="40"/>
        <img src="https://cdn.worldvectorlogo.com/logos/django.svg" alt="Django" width="40" height="40"/>
    </a>
<!-- Django REST Framework -->
</a>
<!-- Django -->
    <a href="https://www.djangoproject.com/" target="_blank" rel="noreferrer">
    <a href="https://www.django-rest-framework.org/" target="_blank"> <img src="https://www.django-rest-framework.org/img/logo.png" alt="restframework" width="90" height="40"/> </a>
<!-- drf_yasg -->
    <a href="https://github.com/axnsan12/drf-yasg" target="_blank" rel="noreferrer">
        <img src="https://avatars.githubusercontent.com/u/9919?s=200&v=4" alt="drf_yasg" width="40" height="40"/>
    </a>
<!-- psutil -->
    <a href="https://github.com/giampaolo/psutil" target="_blank" rel="noreferrer">
        <img src="https://img.icons8.com/fluency/48/system-task.png" alt="psutil" width="40" height="40"/>
    </a>
<!-- Swagger -->
    <a href="https://swagger.io/" target="_blank" rel="noreferrer">
        <img src="https://www.svgrepo.com/show/354420/swagger.svg" alt="Swagger" width="40" height="40"/>
    </a>
<!-- WMI -->
    <a href="https://github.com/tjguk/wmi" target="_blank" rel="noreferrer">
        <img src="https://img.icons8.com/color/48/windows-10.png" alt="WMI" width="40" height="40"/>
    </a>
</p>

---

<p align="justify">
<strong>SysMonitor API</strong> is a Django REST Framework-based project that provides <strong>real-time</strong> hardware and system status information via API.  
It retrieves data for <strong>CPU</strong>, <strong>RAM</strong>, <strong>Disk</strong>, <strong>GPU</strong>, <strong>Battery</strong>, and <strong>System Uptime</strong> in JSON format.
</p>


---

## 📷 SysInfo
<img width="1892" height="907" alt="Screenshot 2025-08-13 233111" src="https://github.com/user-attachments/assets/b5cc51e3-6b28-4f7b-ae4c-f46d3ed97552" />

---


## 📷 SysStatus
<img width="1894" height="909" alt="Screenshot 2025-08-13 233203" src="https://github.com/user-attachments/assets/41dc6a44-2f06-4502-9593-40c28f1cb253" />


---

## 📌 Features
- 📊 CPU usage percentage (per core & total)
- 💾 RAM status (total, used, available)
- 📂 Disk usage information
- 🎮 GPU details (memory, load, temperature)
- 🔋 Battery percentage & charging status
- ⏳ System uptime
- 🌐 API documentation with Swagger & Redoc

---

## 🛠 Requirements
Install dependencies using:

```bash
pip install -r requirements.txt
```

## 🚀 How to Run

1. Clone the repository:
```bash
https://github.com/mohammadmatin2000/SysInfo-Api.git
```
2. Navigate to project directory:
```bash
cd core
```
4. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run migrations:
```bash
python manage.py migrate
```
5. Start the development server:
```bash
python manage.py runserver
```

---

<div align="center">
<h1> 📡 API Endpoints </h1>

| Endpoint        | Method | Description                  |
|-----------------|--------|------------------------------|
| `/sysmonitor/`  | GET    | Get full system status       |
| `/swagger/`     | GET    | Swagger UI documentation     |
| `/redoc/`       | GET    | Redoc documentation          |
</div>

---

<div align="center">
<h1 align="center">Thanks for visiting</h1>
<h3 align="center">I hope that you enjoy it, Let me know if you have any suggestion</h3>
</div>

---


