import os
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import UploadedContent
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Max
from .models import UploadedContent, UserProfile
from django.contrib.auth.models import User

def splash_screen(request):
    return render(request, 'splash.html')

# হোম পেজ এবং সার্চ পেজ লজিক
def home(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    # views.py এর ভেতরে যেখানে এই লাইনটি আছে
contents = UploadedContent.objects.all().order_by('-uploaded_at') # created_at এর বদলে uploaded_at দিন

    # যদি ইউজার সার্চ বক্সে কিছু লিখে সার্চ করে:
    if query:
        contents = contents.filter(title__icontains=query)
        # তাকে নতুন search.html পেজে পাঠানো হবে
        return render(request, 'search.html', {'contents': contents, 'query': query})

    # যদি ইউজার কোনো ক্যাটাগরি ফিল্টার করে:
    if category and category != 'all':
        contents = contents.filter(content_type=category)

    # সাধারণ অবস্থায় হোম পেজ দেখাবে
    return render(request, 'home.html', {'contents': contents})

# নতুন ইউজার রেজিস্ট্রেশন
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # রেজিস্ট্রেশন সফল হলে এখন ড্যাশবোর্ডে যাবে
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# লগ-ইন হওয়ার পরের পেজ (Dashboard)
@login_required
def dashboard(request):
    # ইউজার নিজে যে অ্যাপগুলো আপলোড করেছে, সেগুলো তার ড্যাশবোর্ডে দেখাবে
    user_apps = UploadedContent.objects.filter(uploaded_by=request.user).order_by('-created_at')
    return render(request, 'dashboard.html', {'user_apps': user_apps})

# আপলোড লজিক (লোগো আপলোড সহ)
@login_required
def upload_content(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        content_type = request.POST.get('content_type')
        uploaded_file = request.FILES.get('file')
        logo_file = request.FILES.get('logo') # লোগো রিসিভ করা হচ্ছে

        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            
            # তুমি (Superuser) সব পারবে, অন্যরা শুধু APK
            if not request.user.is_superuser:
                if ext != '.apk':
                    return render(request, 'upload.html', {'error': 'অন্য ইউজাররা শুধুমাত্র .apk ফাইল আপলোড করতে পারবেন।'})
                content_type = 'app'

            UploadedContent.objects.create(
                title=title, 
                description=description,
                content_type=content_type, 
                file=uploaded_file,
                logo=logo_file, # ডাটাবেসে লোগো সেভ করা হচ্ছে
                uploaded_by=request.user
            )
            return redirect('dashboard') # আপলোডের পর ড্যাশবোর্ডে ফিরে যাবে
    return render(request, 'upload.html')

# অ্যাপের ডিটেইলস পেজ
def app_detail(request, pk):
    item = get_object_or_404(UploadedContent, pk=pk)
    related_apps = UploadedContent.objects.exclude(pk=pk).order_by('?')[:4]
    return render(request, 'app_detail.html', {'item': item, 'related_apps': related_apps})

# রেটিং লজিক 
@csrf_exempt
def update_rating(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        content = UploadedContent.objects.get(id=data.get('id'))
        new_score = int(data.get('score'))
        current_total = content.rating * content.total_votes
        content.total_votes += 1
        content.rating = (current_total + new_score) / content.total_votes
        content.save()
        return JsonResponse({'status': 'success', 'new_rating': round(content.rating, 1)})

# কাস্টমার কেয়ার পেজ
def customer_care(request):
    return render(request, 'customer_care.html')

# ডাউনলোড ট্র্যাক করার ফাংশন
def download_file(request, pk):
    item = get_object_or_404(UploadedContent, pk=pk)
    
    # ডাউনলোডের সংখ্যা ১ বাড়িয়ে ডাটাবেসে সেভ করা
    item.downloads += 1
    item.save()
    
    # কাউন্ট হওয়ার পর ইউজারকে আসল ফাইলে পাঠিয়ে দেওয়া
    return redirect(item.file.url)

# ক্রিয়েটর অ্যানালিটিক্স ড্যাশবোর্ড
@login_required
def analytics_dashboard(request):
    # ইউজারের আপলোড করা সব অ্যাপ খুঁজে আনা (বেশি ডাউনলোড হওয়াগুলো ওপরে থাকবে)
    user_apps = UploadedContent.objects.filter(uploaded_by=request.user).order_by('-downloads')
    
    total_apps = user_apps.count()
    
    # মোট ডাউনলোডের যোগফল বের করা
    total_downloads = user_apps.aggregate(Sum('downloads'))['downloads__sum'] or 0
    
    # গড় রেটিং হিসাব করা
    avg_rating = 0
    if total_apps > 0:
        avg_rating = round(sum(app.rating for app in user_apps) / total_apps, 1)

    context = {
        'user_apps': user_apps,
        'total_apps': total_apps,
        'total_downloads': total_downloads,
        'avg_rating': avg_rating
    }
    return render(request, 'analytics.html', context)

# টপ ট্রেন্ডিং (সেরা ১০টি অ্যাপ)
def trending_apps(request):
    # প্রথমে ডাউনলোড এবং তারপর রেটিংয়ের ওপর ভিত্তি করে সেরা ১০টি অ্যাপ বাছাই করা
    top_apps = UploadedContent.objects.order_by('-downloads', '-rating')[:10]
    
    return render(request, 'trending.html', {'top_apps': top_apps})

# পাবলিক ডেভেলপার প্রোফাইল
def developer_profile(request, username):
    # নির্দিষ্ট ইউজারকে খুঁজে বের করা
    developer = get_object_or_404(User, username=username)
    
    # সেই ইউজারের আপলোড করা সব অ্যাপ
    dev_apps = UploadedContent.objects.filter(uploaded_by=developer).order_by('-created_at')
    
    total_apps = dev_apps.count()
    total_downloads = dev_apps.aggregate(Sum('downloads'))['downloads__sum'] or 0
    
    context = {
        'developer': developer,
        'dev_apps': dev_apps,
        'total_apps': total_apps,
        'total_downloads': total_downloads
    }
    return render(request, 'developer_profile.html', context)

from django.shortcuts import render, redirect
from .models import AppRequest

def faq_view(request):
    return render(request, 'faq.html')

def privacy_view(request):
    return render(request, 'privacy_policy.html')

def changelog_view(request):
    return render(request, 'change_log.html')

def app_request_view(request):
    if request.method == "POST":
        app_name = request.POST.get('app_name')
        description = request.POST.get('description')
        user_email = request.POST.get('user_email')
        AppRequest.objects.create(app_name=app_name, description=description, user_email=user_email)
        return redirect('home')
    return render(request, 'app_request.html')

def developer_profile_view(request, username):
    # ১. ডেভেলপারকে খুঁজে বের করা
    developer = get_object_or_404(User, username=username)
    
    # ২. ডেভেলপারের সব অ্যাপ নিয়ে আসা
    dev_apps = UploadedContent.objects.filter(uploaded_by=developer).order_by('-created_at')
    
    # ৩. স্ট্যাটাস ক্যালকুলেশন
    total_downloads = dev_apps.aggregate(Sum('downloads'))['downloads__sum'] or 0
    
    # ৪. সেরা অ্যাপ (Most Downloaded)
    most_downloaded = dev_apps.order_by('-downloads').first()
    
    # ৫. সেরা রেটিং পাওয়া অ্যাপ
    top_rated = dev_apps.order_by('-rating').first()

    return render(request, 'developer_profile.html', {
        'developer': developer,
        'dev_apps': dev_apps,
        'total_downloads': total_downloads,
        'most_downloaded': most_downloaded,
        'top_rated': top_rated,
        'app_count': dev_apps.count(),
    })