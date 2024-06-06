<p align="center">
<img src="https://github.com/Parkomate-ParkVision/parkvision-frontend/assets/85283622/6f609ea7-b547-43cb-a771-2240ec86e914" width=400 />
</p>

# ParkVision Parking Analytics Dashboard (Backend)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
- [Installation](#installation)

## Introduction

**ParkVision** is an advanced analytics dashboard designed for monitoring parking statistics and customer segmentation. This repository contains the backend code for ParkVision, handling data processing, storage, and AI analytics.

## Features

- **Data Management**: Handles large volumes of parking and customer data.
- **AI Analytics**: Processes data using machine learning algorithms to generate insights.
- **API Services**: Provides RESTful APIs for frontend integration.
- **Email Notifications**: Sends alerts to users.
- **Dockerized Deployment**: Simplified setup and deployment using Docker.

## Technologies

- **Python**: Main programming language for backend development.
- **Django**: High-level Python web framework for rapid development.
- **PostgreSQL**: Database management system for storing and managing data.
- **Docker**: Containerization platform for consistent environments.
- **Celery**: Asynchronous task queue/job queue for running background tasks.
- **Flower**: Used as a message broker for Celery.
- **Redis**: In-memory data structure store used for backend data caching.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Docker
- Docker Compose

### Installation

1. **Clone the repository:**
```
git clone https://github.com/BE-Project-Parkomate/parkvision-backend
cd parkvision-backend
```

2. **Create env file:**
```sh
Create a .env file in the project folder with the following fields:
DB_NAME = <db_name>
DB_USER = <db_user>
DB_PASS = <db_password>
DB_HOST = <db_host>
DB_PORT = <db_port>
EMAIL = <email>
EMAIL_PASSWORD = <email_app_password>
```

3. **Build/Start docker images:**
```sh
./run.sh start-dev
```

4. **Migrate the project:**
```sh
./run.sh interactive-dev
python manage.py migrate
```

5. **Stop docker images:**
```sh
./run.sh stop-dev
```

<br>
<br>

![PARKVISION AHH BACKEND](https://github.com/Parkomate-ParkVision/parkvision-backend/assets/67187699/006ab233-521b-4b37-a25e-859020e55c69)
