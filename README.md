# News project
Test project

## What was implemented

- Posts on moderation
- Comments for posts
- When adding a comment for a post, author of post receive an email notification
- User can subscribe to blogs of other users
- User can mark posts in the feed as read.
- When adding a post to the feed, subscribers receive an email notification with a link to a new post.

### Using

- Python 3.7
- Django 2.2
- Celery 4.3
- Redis 3.3
- Ckeditor 5.8

## Installation

#### 1. Run docker:

```bash
docker-compose up
```

#### 2. Create .env file with secret information:

For example:
SECRET_KEY=your_data 