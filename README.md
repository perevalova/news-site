

# News project
Test project

## Installation

#### 1. Install dependencies:

```bash
pip install -r requirements.txt
```

#### 2. Make migrations:


```bash
python manage.py migrate
```

#### 3. Create .env file with secret information:

For example:
SECRET_KEY=your_data 

#### 4. Start redis server:

```bash
 redis-server
```

#### 5. Start celery:

```bash
 celery -A news_project worker -l info
```

#### 6. Run server:

```bash
python manage.py runserver
```
