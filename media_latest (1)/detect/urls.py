from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='index'),
    path('home/',home,name='home'),
    path('register/',userRegister,name='register'),
    path('login/',userLogin,name='login'),
    path('logout/',logout,name='logout'),
    path('profile/',showprofile,name='profile'),
    path('edit_profile/',editProfile,name='editprofile'),
    path('del_account/',deleteAccount,name='del_account'),
    path('analyze/',fakedetect,name='analyze'),
    path('add_news/',AddNews,name='addnews'),
    path('view_my_news/',viewMynews,name='view_my'),
    path('detailed_news/<int:nid>/',detailednews,name='detailed_news'),

    path('allnews/',allnews,name='allnews'),
    path('newsdetailed/<int:nid>/',newsdetailed,name='newsdetailed'),
    path('toggle_news_status/<int:aid>/',toggle_news_status,name='toggle_news_status'),

    path('view_all_news/',viewAllnews,name='view_all'),
    path('edit_news/<int:newsid>/',editMynews,name='editnews'),
    path('delete_news/<int:newsid>/',deleteMynews,name='deletenews'),
    path('add_feedback/',addFeedback,name='addfeedback'),
    path('view_feedback/',viewFeedback,name='view_feedback'), 
    path('edit_feedback/<int:fid>/',editFeedback,name='edit_feedback'), 
    path('delete_feedback/<int:fid>/',deleteFeedback,name='delete_feedback'),
    path('report_news/<int:nid>/',reportNews,name='report_news'),
    path('search_on_web/',checkNewsfromweb,name='search_on_web'),
    
    #admin section
    path('admin_home/',admin_home,name='admin_home'),
    path('admin_login/',adminlogin,name='admin_login'),
    path('view_users/',UserList,name='view_users'),
    path('edit_users/<int:uid>/',EditUsers,name='edit_users'),
    path('delete_users/<int:uid>/',DeleteUsers,name='delete_users'),
    path('view_news/',Newslist,name='view_news'),
    path('edit_newsad/<int:nid>/',Editnews,name='edit_newsad'),
    path('delete_newsad/<int:nid>/',Deletenews,name='delete_newsad'),
    path('view_reported_news/',viewReportedNews,name='view_reported_news'),
    path('ad_view_feedback/',adviewFeedback,name='ad_view_feedback'),
    path('ad_delete_feedback/<int:fid>/',addeleteFeedback,name='ad_delete_feedback'),
    path('adlogout/',adLogout,name='ad_logout'),
]
