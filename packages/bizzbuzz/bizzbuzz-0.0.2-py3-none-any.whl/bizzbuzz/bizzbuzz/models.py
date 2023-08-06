from django.db import models

# table name: bizzbuzz_news
# see all news articles in DB: select * from bizzbuzz_news inside Query Console
# run 'python manage.py populate_db' to run script that populates DB for the first time
# run 'python manage.py update_db' to update DB periodically
class News(models.Model):
    title = models.TextField('Article Title')
    url = models.TextField('Article URL')
    expiration_date = models.DateTimeField(auto_now_add=True) #compare against this for deleting old rows, +7 from current date
    summary = models.TextField('Article Summary')

# make table for the preferences of each user, default means they want all news
# initially set during sign up, toggled with icons on side
# table name: bizzbuzz_preferences
class Preferences(models.Model):
    username = models.TextField('Username')
    apple = models.BooleanField(default=True)
    google = models.BooleanField(default=True)
    facebook = models.BooleanField(default=True)
    microsoft = models.BooleanField(default=True)
