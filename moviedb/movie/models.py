from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#single line use charField
#multiple lines use textField
class Movie(models.Model):
	name = models.CharField(max_length=50)
	runtime = models.IntegerField(null=True, blank=True)
	storyline = models.TextField(null=True, blank=True)
	def __str__(self):
		return self.name

class Crew(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField(max_length=100, blank=True)
	crew_type = models.IntegerField()
	def __str__(self):
		return self.name

class Produce(models.Model):
	mid = models.ForeignKey(Movie)
	cid = models.ForeignKey(Crew)
	def __str__(self):
		return self.cid.name+" produce "+self.mid.name

class Genre(models.Model):
	name = models.CharField(max_length=50)
	def __str__(self):
		return self.name

class BelongTo(models.Model):
	mid = models.ForeignKey(Movie)
	gid = models.ForeignKey(Genre)
	def __str__(self):
		return self.mid.name+" belong to "+self.gid.name

class ReleaseInfo(models.Model):
	mid = models.ForeignKey(Movie)
	date = models.DateField()
	area = models.CharField(max_length = 50)

	class Meta:
		unique_together = ('id', 'mid')
	def __str__(self):
		return self.mid.name+" "+str(self.date)+" "+self.area

class Review(models.Model):
	uid = models.ForeignKey(User)
	mid = models.ForeignKey(Movie)
	date = models.DateTimeField()
	content = models.TextField(max_length = 5000, blank = True)
	rating = models.IntegerField()

class Watch(models.Model):
	uid = models.ForeignKey(User)
	mid = models.ForeignKey(Movie)

class Favorite(models.Model):
	uid = models.ForeignKey(User)
	mid = models.ForeignKey(Movie)

class Post(models.Model):
	user = models.ForeignKey(User)
	content = models.TextField(max_length = 5000, blank = True)
	date = models.DateTimeField()

class Topic(Post):
	title = models.CharField(max_length = 100)

class Comment(Post):
	post_belong = models.ForeignKey(Topic)

