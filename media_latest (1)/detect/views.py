from django.shortcuts import render,redirect,HttpResponse
from .models import *
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util
import torch
from transformers import pipeline
MODEL = "jy46604790/Fake-News-Bert-Detect"
clf = pipeline("text-classification", model=MODEL, tokenizer=MODEL)
from sentence_transformers import SentenceTransformer
import requests
from bs4 import BeautifulSoup
from torch.nn import functional as F
import time
from fake_useragent import UserAgent
import logging
from dataclasses import dataclass
from typing import List, Optional

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class NewsArticle:
    headline: str
    source: str
    url: Optional[str] = None
    publish_date: Optional[str] = None
    similarity_score: float = 0.0

# Initialize SBERT model
sbert_model = SentenceTransformer('distilbert-base-nli-mean-tokens')

def get_sbert_embedding(text):
    try:
        return sbert_model.encode(text, convert_to_tensor=True)
    except Exception as e:
        logger.error(f"Error generating embedding: {str(e)}")
        return None

def scrape_news_from_multiple_sources(query):
    sources = [
        {
            'name': 'Bing News',
            'url': f"https://www.bing.com/news/search?q={query}",
            'headline_selector': '.news-card-body',
            'source_selector': '.source',
            'link_selector': '.news-card-body a',
            'date_selector': '.source time'
        },
        {
            'name': 'Google News',
            'url': f"https://news.google.com/search?q={query}&hl=en-US",
            'headline_selector': '.ipQwMb',
            'source_selector': '.vr1PYe',
            'link_selector': '.VDXfz',
            'date_selector': '.SVJrMe'
        }
    ]
    
    news_articles = []
    ua = UserAgent()
    
    for source_config in sources:
        try:
            headers = {
                "User-Agent": ua.random,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }
            
            response = requests.get(
                source_config['url'],
                headers=headers,
                timeout=10
            )
            
            response.raise_for_status()
            time.sleep(2)
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Find all news items
            headlines = []
            for item in soup.select(source_config['headline_selector']):
                try:
                    headline = item.get_text().strip()
                    if headline and len(headline) > 10:
                        headlines.append({
                            'headline': headline,
                            'source': source_config['name']
                        })
                except Exception as e:
                    logger.error(f"Error processing news item: {str(e)}")
                    continue
            
            # Add headlines with their source
            news_articles.extend(headlines)
            logger.info(f"Found {len(headlines)} headlines from {source_config['name']}")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching from {source_config['name']}: {str(e)}")
            continue
            
    return news_articles

def check_news_similarity(user_news, news_articles):
    if not news_articles:
        return False, None, []
        
    try:
        user_embedding = get_sbert_embedding(user_news)
        if user_embedding is None:
            return False, None, []
            
        max_similarity = 0
        most_similar_headline = None
        similar_headlines = []
        
        for article in news_articles:
            headline = article['headline']
            headline_embedding = get_sbert_embedding(headline)
            if headline_embedding is None:
                continue
                
            similarity = F.cosine_similarity(
                user_embedding.unsqueeze(0),
                headline_embedding.unsqueeze(0)
            ).item()
            
            if similarity > 0.6:  # Threshold for similarity
                similar_headlines.append(f"{headline} (Source: {article['source']}, Match: {round(similarity * 100, 1)}%)")
            
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_headline = headline
        
        is_similar = max_similarity > 0.6
        return is_similar, most_similar_headline, similar_headlines
        
    except Exception as e:
        logger.error(f"Error in similarity check: {str(e)}")
        return False, None, []

def checkNewsfromweb(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    msg = ""
    related_headlines = []
    
    try:
        user_id = request.session['user_id']
        user = UserReg.objects.get(id=user_id)
        
        if request.method == 'POST':
            user_news = request.POST.get('user_news', '').strip()
            
            if not user_news:
                msg = "Please enter a news headline to verify"
            else:
                news_articles = scrape_news_from_multiple_sources(user_news)
                
                if news_articles:
                    is_similar, most_similar, similar_headlines = check_news_similarity(user_news, news_articles)
                    related_headlines = similar_headlines
                    
                    if is_similar:
                        msg = "✅ REAL NEWS - Similar headlines found in trusted sources"
                    else:
                        msg = "⚠️ POTENTIALLY FAKE - No similar headlines found in trusted sources"
                else:
                    msg = "⚠️ Unable to verify - No related news found online"
                    
    except UserReg.DoesNotExist:
        return redirect('login')
    except Exception as e:
        logger.error(f"Error in checkNewsfromweb: {str(e)}")
        msg = "❌ An error occurred while verifying the news"
        
    return render(request, 'check_news.html', {
        'msg': msg,
        'related_headlines': related_headlines
    })
def index(request):
    return render(request, 'index.html')

def home(request):
    if 'user_id' in request.session:
        uid=request.session['user_id']
        try:
            user=UserReg.objects.get(id=uid)
            return render(request, 'home.html')

        except:
            return redirect('login')
    return redirect('login')
def userRegister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user=UserReg(name=username,email=email,password=password)
        user.save()
        
        return redirect('login')
    return render(request, 'register.html')


def userLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = UserReg.objects.get(email=email, password=password)
            if user:
                request.session['user_id'] = user.id
                return redirect('home')
            else:
                return redirect('login')
        except Exception as e:
            print(e)
            alert="<script>alert('invalid email or password'); window.location.href='/login/';</script>"
            return HttpResponse(alert)
    return render(request, 'login.html')

def showprofile(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = UserReg.objects.get(id=user_id)
        
        # Query all news by the user
        user_news = News.objects.filter(author=user)
        
        if not user_news.exists():
            user_behavior = "No news uploaded yet"
        else:
            # Count real and fake news posted by the user
            real_count = user_news.filter(newsstatus="Real").count()
            fake_count = user_news.filter(newsstatus="Fake").count()
            
            # Determine behavior based on counts
            if real_count > fake_count:
                user_behavior = "Mostly posts real news"
            elif fake_count > real_count:
                user_behavior = "Mostly posts fake news"
            else:
                user_behavior = "Posts an equal mix of real and fake news"
        
        # Pass the behavior message to the template
        return render(request, 'profile.html', {
            'user': user,
            'user_behavior': user_behavior,
        })
    else:
        return redirect('login')
    
def editProfile(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = UserReg.objects.get(id=user_id)
        print(user)
        
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            user.name = username
            user.email = email
            user.password = password
            user.save()
            
            return redirect('profile')
        
        return render(request, 'edit_profile.html', {'user':user})
    else:
        return redirect('login')
    
def deleteAccount(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = UserReg.objects.get(id=user_id)
        
        user.delete()
        del request.session['user_id']
        
        return redirect('index')
    else:
        return redirect('login')
    
    
def fakedetect(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        result = clf(text)
        
        if result[0]['label'] == 'LABEL_0':
            message = 'This is a Fake News.'
            score = result[0]['score']
        else:
            message = 'This is a Real News.'
            score = result[0]['score']
        
        return render(request, 'fakedetect.html', {'text': text, 'result': message, 'score': score})
    
    return render(request, 'fakedetect.html')

import hashlib    

def AddNews(request):
    news_hash=""
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = UserReg.objects.get(id=user_id)
        user_news = News.objects.filter(author=user)
        user_behavior=""
        if not user_news.exists():
            user_behavior = "No news uploaded yet"
        else:
            real_count = user_news.filter(newsstatus="Real").count()
            fake_count = user_news.filter(newsstatus="Fake").count()
            if real_count > fake_count:
                user_behavior = "Mostly posts real news"
            elif fake_count > real_count:
                user_behavior = "Mostly posts fake news"
            else:
                user_behavior = "Posts an equal mix of real and fake news"
        if request.method == 'POST':
            headline = request.POST.get('headline')
            category = request.POST.get('category')
            newstext = request.POST.get('newstext')
            image = request.FILES.get('image')
            result = clf(newstext)
            print(result)
            if result[0]['label'] == 'LABEL_0':
                message = 'Fake'
            else:
                message = 'Real'
                hash_input = f"{headline}{newstext}{category}{user.id}".encode()
                news_hash = hashlib.sha256(hash_input).hexdigest()
                print("Hash Value",news_hash)
            nes = News(headline=headline, newstext=newstext, category=category, author=user,newsstatus=message,us_behave=user_behavior,image=image, news_hash=news_hash)
            nes.save()
            return redirect('view_my')
        return render(request, 'add_news.html')
    else:
        return redirect('login')
    
def viewMynews(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = UserReg.objects.get(id=user_id)
        news = News.objects.filter(author=user)
        return render(request, 'view_mynews.html', {'news': news})
    else:
        return redirect('login')
    
def viewAllnews(request):
    if 'user_id' in request.session:
        user_id=request.session['user_id']
        news = News.objects.filter(status=True).order_by('-created_at')
        return render(request, 'view_allnews.html', {'news': news,'uid':user_id})
    else:
        return redirect('login')
    
def detailednews(request,nid):
    if 'user_id' in request.session:
        user_id=request.session['user_id']
        news = News.objects.get(id=nid)
        return render(request, 'detailed_news.html', {'news': news,'uid':user_id})
    else:
        return redirect('login')
    
    
def editMynews(request,newsid):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = UserReg.objects.get(id=user_id)
        news = News.objects.get(id=newsid)
        
        if request.method == 'POST':
            headline = request.POST.get('headline')
            category = request.POST.get('category')
            newstext = request.POST.get('newstext')
            image = request.FILES.get('image')
            result = clf(newstext)
            print(result)
            if result[0]['label'] == 'LABEL_0':
                message = 'Fake'
            else:
                message = 'Real'
            news.headline = headline
            news.category = category
            news.newstext = newstext
            news.newsstatus = message
            if image:
                news.image = image
            news.save()
            return redirect('home')
        
        return render(request, 'edit_mynews.html', {'news': news})
    else:
        return redirect('login')
    
def deleteMynews(request, newsid):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = UserReg.objects.get(id=user_id)
        news = News.objects.get(id=newsid,author=user)
        news.delete()
        return redirect('home')
    else:
        return redirect('login')
    
def addFeedback(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = UserReg.objects.get(id=user_id)
        if request.method == 'POST':
            feedback = request.POST.get('feedback')
            rating = request.POST.get('rating')
            FeedbackReg(user=user, feedbacktext=feedback,rating=rating).save()
            return redirect('home')
        return render(request, 'add_feedback.html')
    return redirect('login')

def viewFeedback(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = UserReg.objects.get(id=user_id)
        feedback = FeedbackReg.objects.filter(user=user)
        return render(request, 'view_feedback.html', {'feedback': feedback})
    else:
        return redirect('login')
    
def editFeedback(request,fid):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = UserReg.objects.get(id=user_id)
        feedback = FeedbackReg.objects.get(user=user,id=fid)
        
        if request.method == 'POST':
            feedback.feedbacktext = request.POST.get('feedback')
            rating = request.POST.get('rating')
            feedback.rating = rating
            feedback.save()
            return redirect('home')
        
        return render(request, 'edit_feedback.html', {'feedback': feedback})
    else:
        return redirect('login')
    
def deleteFeedback(request,fid):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = UserReg.objects.get(id=user_id)
        feedback = FeedbackReg.objects.get(user=user, id=fid)
        feedback.delete()
        return redirect('home')
    else:
        return redirect('login')
    
def reportNews(request,nid):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = UserReg.objects.get(id=user_id)
        news = News.objects.get(id=nid)
        if request.method == 'POST':
            reason = request.POST.get('reason')
            report_type = request.POST.get('report_type')
            r_news=ReportNews(user=user,news=news,reason_text=reason,report_type=report_type)
            r_news.save()
            return redirect('home')
        return render(request, 'report_news.html', {'news': news})
    else:
        return redirect('login')
    
def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    
    return redirect('index')
    
#admin section


def admin_home(request):
    if 'admin_email' in request.session:
        user=UserReg.objects.all().count()
        news=News.objects.all().count()
        feedbacks=FeedbackReg.objects.all().count()
        return render(request, 'admin_home.html', {'user_count': user,'news_count': news,'feed_count':feedbacks })
    else:
        return redirect('admin_login')
def adminlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email == 'admin@gmail.com' and password == 'admin123':
            request.session['admin_email'] = email
            return redirect('admin_home')
        else:
            # Pass an error flag to the template
            return render(request, 'admin_login.html', {'error': 'Invalid email or password'})

    return render(request, 'admin_login.html')

def UserList(request):
    if 'admin_email' in request.session:
        users = UserReg.objects.all()
        return render(request, 'admin_user_list.html', {'users': users})
    else:
        return redirect('admin_login')
    
def EditUsers(request,uid):
    if 'admin_email' in request.session:
        user = UserReg.objects.get(id=uid)
        
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            user.name = username
            user.email = email
            user.password = password
            user.save()
            
            return redirect('admin_user_list')
        
        return render(request, 'admin_edit_user.html', {'user': user})
    else:
        return redirect('admin_login')
def DeleteUsers(request,uid):
    if 'admin_email' in request.session:
        user = UserReg.objects.get(id=uid)
        user.delete()
        return redirect('view_users')
    else:
        return redirect('admin_login')
    
def Newslist(request):
    if 'admin_email' in request.session:
        news = News.objects.all().order_by('-created_at')
        return render(request, 'admin_news_list.html', {'news': news})
    else:
        return redirect('admin_login')
    
def toggle_news_status(request,aid):
    try:
        ap=News.objects.get(id=aid)
        if ap.status==False:
            ap.status=True
            ap.save()
            return redirect('view_news')
        else:
            ap.status=False
            ap.save()
            return redirect('view_news')
    except:
        return redirect('view_news')
    
def Editnews(request,nid):
    if 'admin_email' in request.session:
        news = News.objects.get(id=nid)
        if request.method == 'POST':
            headline = request.POST.get('headline')
            category = request.POST.get('category')
            newstext = request.POST.get('newstext')
            status=request.POST.get('status')
            image=request.FILES.get('image')
            news.headline = headline
            news.category = category
            news.newstext = newstext
            news.newsstatus = status
            if image:
                news.image = image
            news.save()
            
            return redirect('view_news')
        
        return render(request, 'admin_edit_news.html', {'news': news})
    else:
        return redirect('admin_login')
def Deletenews(request,nid):
    if 'admin_email' in request.session:
        news = News.objects.get(id=nid)
        news.delete()
        return redirect('view_news')
    else:
        return redirect('admin_login')
    
def viewReportedNews(request):
    if 'admin_email' in request.session:
        reported_news = ReportNews.objects.all()
        return render(request, 'admin_reported_news.html', {'reported_news': reported_news})
    else:
        return redirect('admin_login')
    
def adviewFeedback(request):
    if 'admin_email' in request.session:
        feedback = FeedbackReg.objects.all()
        return render(request, 'admin_view_feedback.html', {'feedback': feedback})
    else:
        return redirect('admin_login')
def addeleteFeedback(request,fid):
    if 'admin_email' in request.session:
        feedback = FeedbackReg.objects.get(id=fid)
        feedback.delete()
        return redirect('ad_view_feedback')
    else:
        return redirect('admin_login')
    
def  adLogout(request):
    if 'admin_email' in request.session:
        del request.session['admin_email']
    
    return redirect('admin_login')

def allnews(request):
    news = News.objects.filter(status=True).order_by('-created_at')
    return render(request, 'allnews.html', {'news': news})
    
def newsdetailed(request,nid):
    news = News.objects.get(id=nid)
    return render(request, 'newsdetailed.html', {'news': news})