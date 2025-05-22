# 🎯 FastAPI + Celery Background Task System

This project demonstrates how to build a **background task processing system** using:

- **FastAPI** (for API endpoints)
- **Celery** (for async task execution)
- **Redis** (for result backend)
- **RabbitMQ** (as message broker)
- **Flower** (for task monitoring)
- **Docker Compose** (for container orchestration)
- **python-dotenv** (to manage environment variables)

---

## 🛠️ Features

- Submit tasks to generate random numbers with delay
- Track progress of tasks in real time
- Monitor tasks with Flower UI

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Docker & Docker Compose

---

### 🔧 Setup

1. Clone the repository:

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name


2. Create a .env file in the root with the following contents:

# RabbitMQ
RABBITMQ_DEFAULT_USER=guest
RABBITMQ_DEFAULT_PASS=guest

# Flower
FLOWER_PORT=5555
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
CELERY_RESULT_BACKEND=redis://redis:6379/0

# FastAPI
FASTAPI_PORT=8000
FASTAPI_COMMAND=uvicorn app.main:app --host 0.0.0.0 --port=8000 --reload

# Celery
CELERY_WORKER_COMMAND=sh -c "sleep 10 && celery -A app.celery_worker worker -Q default --loglevel=info"
FLOWER_COMMAND=sh -c "sleep 10 && celery -A app.celery_worker flower --port=${FLOWER_PORT}"


3. Start the application:

docker-compose up --build


📫 API Usage

Submit Task
    POST /submit/?count=5

    Response:
        {
        "message": "Task submitted to generate 5 random numbers",
        "task_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        }

Get Task Status
    GET /result/{task_id}


🌼 Flower Monitoring UI

Access Flower at:
📍 http://localhost:5555


📦 Tech Stack

    FastAPI
    Celery
    Redis
    RabbitMQ
    Docker + Compose
    Flower
    Python-dotenv


📁 Project Structure

.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── tasks.py
│   └── celery_worker.py
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md


✅ To Do

    Add authentication

    Add input validation

    Deploy to cloud (e.g., AWS, Render, Railway)


📄 License

    MIT License - free for personal and commercial use.

    
  