from __future__ import unicode_literals
from django.conf import settings
from django.db import models
import datetime
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
# Create your models here.
#MVC 
#Post.objects.all().published()
#Post.objects.create(user=user, title="Some time")

class PostQuerySet(models.query.QuerySet):
    def not_draft(self):
        return self.filter(draft=False)
    
    def published(self):
        return self.filter(publish__lte=datetime.datetime.now()).not_draft()

class PostManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return PostQuerySet(self.model, using=self._db)
            
    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()
        return self.get_queryset().published()


def upload_location(instance,filename):
	filebase, extension = filename.split(".")
	return "%s%s.%s" %(instance.id,instance.id,extension)

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	title = models.CharField(max_length=120)
	slug=models.SlugField(unique=True)
	height_field= models.IntegerField(default=0)
	width_field= models.IntegerField(default=0)
	draft = models.BooleanField(default=False)
	publish = models.DateField(auto_now=False, auto_now_add=False)
	image = models.ImageField(null=True,blank=True,
		                  upload_to=upload_location,
		                  width_field="width_field",
		                  height_field="height_field")
	
	content = models.TextField()
	updated = models.DateTimeField(auto_now=True,auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)

	objects = PostManager()

	def __str__(self):
	       return self.title 

	def __unicode__(self):
	       return self.title     

	def get_absolute_url(self):
		return reverse("detail",kwargs={"slug":self.slug})
	    #return "/posts/%s/" %(self.id)   

	class Meta:
		ordering = ["-timestamp","-updated"]



def create_slug(instance, new_slug=None):
	slug=slugify(instance.title)
	if new_slug is not None:
		slug=new_slug
	qs=Post.objects.filter(slug=slug).order_by("-id")
	exists= qs.exists()
	if exists:
		new_slug="%s-%s" %(slug,qs.first().id)
		return create_slug(instance,new_slug=new_slug)
	return slug
		

def pre_save_post_reciever(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_reciever,sender=Post)