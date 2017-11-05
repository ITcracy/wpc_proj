# WPC website

## Installation ##

---

  * Clone this repository
  * Run following command.

 `pip install -r requirements.txt` 
 
  * Create .env file inside wpc_website folder as below
  
  `DEBUG=True`

  `SECRET_KEY=Your-secret-key`

  `DATABASE_URL=psql://wpc-user:wpc-pass@127.0.0.1:5432/wpc_db`

  `CACHE_URL=rediscache://redis:6379/1?client_class=django_redis.client.DefaultClient&password=redis-un-githubbed-password`
  
  * Create .env file in root folder <optional>
  
  `DB_USER=wpc-user`
  
  `DB_PASSWORD=wpc-pass`
  
  `DB_NAME=wpc_db`

  * Run docker-compose up from project root
  
  `docker-compose up`
  
  * Open another terminal and run
  
  `python manage.py migrate`
  
  `python manage.py createsuperuser`
  
  `python manage.py runserver`
