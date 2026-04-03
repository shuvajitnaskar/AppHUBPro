import os
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.contrib.auth.models import User
from .models import UploadedContent, UserProfile, AppRequest

# ১. স্প্ল্যাশ স্ক্রিন
def splash_screen(request):
    return render(request, 'splash.html')

# ২. হোম পেজ (সার্চ এবং ক্যাটাগরি সহ)
def home(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    contents = UploadedContent.objects.all().order_by('-uploaded_at')

    if query:
        contents = contents.filter(title__icontains=query)
        return render(request, 'search.html', {'contents': contents, 'query': query})

    if category and category != 'all':
        contents = contents.filter(content_type=category)

    return render(request, 'home.html', {'contents': contents})

# ৩. রেজিস্ট্রেশন
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# ৪. ড্যাশবোর্ড
@login_required
def dashboard(request):
    user_apps = UploadedContent.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')
    return render(request, 'dashboard.html', {'user_apps': user_apps})

# ৫. কন্টেন্ট আপলোড
@login_required
def upload_content(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        content_type = request.POST.get('content_type')
        
        file_url = request.POST.get('file_url')
        logo_url = request.POST.get('logo_url')

        if title and file_url and logo_url:
            try:
                new_content = UploadedContent.objects.create(
                    title=title, 
                    description=description,
                    content_type=content_type, 
                    file=file_url, 
                    logo=logo_url,
                    uploaded_by=request.user
                )
                new_content.save()
                return JsonResponse({'status': 'success', 'message': 'Upload successful'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        else:
             return JsonResponse({'status': 'error', 'message': 'Missing data or URLs'}, status=400)
             
    return render(request, 'upload.html')

# ৬. অ্যাপ ডিটেইলস
def app_detail(request, pk):
    item = get_object_or_404(UploadedContent, pk=pk)
    related_apps = UploadedContent.objects.exclude(pk=pk).order_by('?')[:4]
    return render(request, 'app_detail.html', {'item': item, 'related_apps': related_apps})

# ৭. ডাউনলোড সিস্টেম (FIXED: Supports Google Drive, Mega, Cloudinary and Old Local Files)
def download_file(request, pk):
    item = get_object_or_404(UploadedContent, pk=pk)
    item.downloads += 1
    item.save()
    
    # ডেটাবেস থেকে ফাইলের লিংকটা স্ট্রিং হিসেবে বের করে নেওয়া
    file_path = str(item.file).strip()
    
    # যদি লিংকটি http বা https দিয়ে শুরু হয়
    if file_path.startswith('http://') or file_path.startswith('https://'):
        return redirect(file_path)
        
    # যদি ইউজার লিংকের শুরুতে https:// দিতে ভুলে যায়, কিন্তু ড্রাইভের লিংক দেয়
    elif 'drive.google.com' in file_path or 'mega.nz' in file_path or 'cloudinary' in file_path:
        return redirect('https://' + file_path)
        
    # যদি এটি পুরনো কোনো লোকাল ফাইল হয় (যা আগে আপলোড করা হয়েছিল)
    elif hasattr(item.file, 'url'):
        try:
            return redirect(item.file.url)
        except:
            pass
            
    # যদি কোনো লিংকই কাজ না করে বা ফাঁকা থাকে, তবে হোম পেজে ফেরত পাঠাবে
    return redirect('home')

# ৮. অ্যানালিটিক্স
@login_required
def analytics_dashboard(request):
    user_apps = UploadedContent.objects.filter(uploaded_by=request.user)
    total_downloads = user_apps.aggregate(Sum('downloads'))['downloads__sum'] or 0
    return render(request, 'analytics.html', {
        'user_apps': user_apps,
        'total_apps': user_apps.count(),
        'total_downloads': total_downloads
    })

# ৯. ট্রেন্ডিং অ্যাপস
def trending_apps(request):
    top_apps = UploadedContent.objects.order_by('-downloads', '-rating')[:10]
    return render(request, 'trending.html', {'top_apps': top_apps})

# ১০. লিডারবোর্ড
def leaderboard(request):
    top_developers = User.objects.annotate(
        total_downloads=Sum('uploadedcontent__downloads')
    ).filter(total_downloads__gt=0).order_by('-total_downloads')[:5]
    return render(request, 'leaderboard.html', {'top_developers': top_developers})

# ১১. ডেভেলপার প্রোফাইল
def developer_profile(request, username):
    developer = get_object_or_404(User, username=username)
    dev_apps = UploadedContent.objects.filter(uploaded_by=developer).order_by('-uploaded_at')
    return render(request, 'developer_profile.html', {'developer': developer, 'dev_apps': dev_apps})

# ১২. অন্যান্য স্ট্যাটিক পেজ
def faq_view(request): return render(request, 'faq.html')
def privacy_view(request): return render(request, 'privacy_policy.html')
def changelog_view(request): return render(request, 'change_log.html')
def customer_care(request): return render(request, 'customer_care.html')

# ১৩. অ্যাপ রিকোয়েস্ট
def app_request_view(request):
    if request.method == "POST":
        AppRequest.objects.create(
            app_name=request.POST.get('app_name'),
            description=request.POST.get('description'),
            user_email=request.POST.get('user_email')
        )
        return redirect('home')
    return render(request, 'app_request.html')

# ১৪. রেটিং (AJAX)
@csrf_exempt
def update_rating(request):
    return JsonResponse({'status': 'success'})