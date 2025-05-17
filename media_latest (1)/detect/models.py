from django.db import models

# Create your models here.



class UserReg(models.Model):
    name=models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(max_length=50,null=True, blank=True,unique=True)
    password = models.CharField(max_length=50,null=True, blank=True)


class News(models.Model):
    newstext= models.TextField()
    author = models.ForeignKey(UserReg, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    newsstatus = models.CharField(max_length=10,null=True, blank=True)
    us_behave= models.CharField(max_length=50,null=True, blank=True,default="Posts an equal mix of real and fake news")
    image = models.ImageField(upload_to='news/',null=True, blank=True)
    headline = models.CharField(max_length=254)
    category = models.CharField(max_length=50, choices=[
    ('Sports', 'Sports'),
    ('Entertainment', 'Entertainment'),
    ('Local News', 'Local News'),
    ('Technology', 'Technology'), 
    ('Business', 'Business')       
])
    news_hash = models.CharField(max_length=64, null=True, blank=True)
    status = models.BooleanField(default=False)

class FeedbackReg(models.Model):
    user=models.ForeignKey(UserReg, on_delete=models.CASCADE)
    feedbacktext=models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2,default=0,null=True, blank=True)
    
class ReportNews(models.Model):
    news=models.ForeignKey(News, on_delete=models.CASCADE)
    user=models.ForeignKey(UserReg, on_delete=models.CASCADE)
    reason_text = models.TextField(null=True, blank=True)
    report_status = (
        ('Real','real'),
        ('Fake','fake'),
    )
    report_type = models.CharField(max_length=10, choices=report_status)