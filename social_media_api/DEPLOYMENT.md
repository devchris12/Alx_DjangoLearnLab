# Deployment Guide for Social Media API

This guide covers deploying the Social Media API to production environments.

## Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database migrations up to date
- [ ] Static files collected
- [ ] Security settings reviewed
- [ ] ALLOWED_HOSTS configured
- [ ] DEBUG set to False

## Production Settings

Update `settings.py` for production:

\`\`\`python
# Security Settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Database (PostgreSQL recommended)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
\`\`\`

## Deployment Options

### Option 1: Heroku

1. **Install Heroku CLI**
   \`\`\`bash
   # Install from https://devcenter.heroku.com/articles/heroku-cli
   \`\`\`

2. **Create Heroku app**
   \`\`\`bash
   heroku create your-app-name
   \`\`\`

3. **Add PostgreSQL**
   \`\`\`bash
   heroku addons:create heroku-postgresql:hobby-dev
   \`\`\`

4. **Set environment variables**
   \`\`\`bash
   heroku config:set SECRET_KEY='your-secret-key'
   heroku config:set DEBUG=False
   \`\`\`

5. **Create Procfile**
   \`\`\`
   web: gunicorn social_media_api.wsgi
   \`\`\`

6. **Deploy**
   \`\`\`bash
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   \`\`\`

### Option 2: DigitalOcean

1. **Create a Droplet** (Ubuntu 22.04 recommended)

2. **SSH into server**
   \`\`\`bash
   ssh root@your-server-ip
   \`\`\`

3. **Install dependencies**
   \`\`\`bash
   apt update
   apt install python3-pip python3-venv nginx postgresql
   \`\`\`

4. **Setup PostgreSQL**
   \`\`\`bash
   sudo -u postgres psql
   CREATE DATABASE social_media_db;
   CREATE USER dbuser WITH PASSWORD 'password';
   GRANT ALL PRIVILEGES ON DATABASE social_media_db TO dbuser;
   \q
   \`\`\`

5. **Clone repository**
   \`\`\`bash
   cd /var/www
   git clone your-repo-url social_media_api
   cd social_media_api
   \`\`\`

6. **Setup virtual environment**
   \`\`\`bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn psycopg2-binary
   \`\`\`

7. **Configure environment variables**
   \`\`\`bash
   nano .env
   # Add your environment variables
   \`\`\`

8. **Run migrations**
   \`\`\`bash
   python manage.py migrate
   python manage.py collectstatic
   python manage.py createsuperuser
   \`\`\`

9. **Setup Gunicorn service**
   \`\`\`bash
   nano /etc/systemd/system/gunicorn.service
   \`\`\`

   \`\`\`ini
   [Unit]
   Description=gunicorn daemon
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/social_media_api
   ExecStart=/var/www/social_media_api/venv/bin/gunicorn \
             --workers 3 \
             --bind unix:/var/www/social_media_api/gunicorn.sock \
             social_media_api.wsgi:application

   [Install]
   WantedBy=multi-user.target
   \`\`\`

10. **Setup Nginx**
    \`\`\`bash
    nano /etc/nginx/sites-available/social_media_api
    \`\`\`

    \`\`\`nginx
    server {
        listen 80;
        server_name yourdomain.com;

        location = /favicon.ico { access_log off; log_not_found off; }
        
        location /static/ {
            root /var/www/social_media_api;
        }

        location /media/ {
            root /var/www/social_media_api;
        }

        location / {
            include proxy_params;
            proxy_pass http://unix:/var/www/social_media_api/gunicorn.sock;
        }
    }
    \`\`\`

11. **Enable and start services**
    \`\`\`bash
    ln -s /etc/nginx/sites-available/social_media_api /etc/nginx/sites-enabled
    systemctl start gunicorn
    systemctl enable gunicorn
    systemctl restart nginx
    \`\`\`

### Option 3: AWS Elastic Beanstalk

1. **Install EB CLI**
   \`\`\`bash
   pip install awsebcli
   \`\`\`

2. **Initialize EB**
   \`\`\`bash
   eb init -p python-3.9 social-media-api
   \`\`\`

3. **Create environment**
   \`\`\`bash
   eb create social-media-api-env
   \`\`\`

4. **Configure environment variables**
   \`\`\`bash
   eb setenv SECRET_KEY='your-secret-key' DEBUG=False
   \`\`\`

5. **Deploy**
   \`\`\`bash
   eb deploy
   \`\`\`

## Post-Deployment

1. **Test all endpoints**
   - Use Postman or curl to test API functionality
   - Verify authentication works
   - Test file uploads

2. **Setup monitoring**
   - Configure error logging
   - Setup uptime monitoring
   - Monitor database performance

3. **Setup backups**
   - Configure automated database backups
   - Backup media files regularly

4. **SSL Certificate**
   - Use Let's Encrypt for free SSL
   \`\`\`bash
   apt install certbot python3-certbot-nginx
   certbot --nginx -d yourdomain.com
   \`\`\`

## Maintenance

### Update deployment
\`\`\`bash
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
systemctl restart gunicorn
\`\`\`

### View logs
\`\`\`bash
# Gunicorn logs
journalctl -u gunicorn

# Nginx logs
tail -f /var/log/nginx/error.log
\`\`\`

## Troubleshooting

### Static files not loading
\`\`\`bash
python manage.py collectstatic --clear
systemctl restart gunicorn nginx
\`\`\`

### Database connection issues
- Check DATABASE_URL environment variable
- Verify database credentials
- Ensure database server is running

### 502 Bad Gateway
- Check Gunicorn is running: `systemctl status gunicorn`
- Check socket file exists
- Review Gunicorn logs

## Security Best Practices

1. Keep SECRET_KEY secure and unique
2. Use environment variables for sensitive data
3. Enable HTTPS/SSL
4. Regular security updates
5. Use strong database passwords
6. Implement rate limiting
7. Regular backups
8. Monitor for suspicious activity

## Performance Optimization

1. Use database connection pooling
2. Implement caching (Redis/Memcached)
3. Optimize database queries
4. Use CDN for static files
5. Enable gzip compression
6. Monitor and optimize slow queries
