import os
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Max
from django.contrib.auth.models import User
from .models import UploadedContent, UserProfile, AppRequest

# ১. স্প্ল্যাশ স্ক্রিন
def splash_screen(request):
    return render(request, 'splash.html')

# ২. হোম পেজ এবং সার্চ লজিক
def home(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    
    # আপনার মডেলে এখন uploaded_at ব্যবহার করা হয়েছে
    contents = UploadedContent.objects.all().order_by('-uploaded_at')

    if query:
        contents = contents.filter(title__icontains=query)
        return render(request, 'search.html', {'contents': contents, 'query': query})

    if category and category != 'all':
        contents = contents.filter(content_type=category)

    return render(request, 'home.html', {'contents': contents})

# ৩. ইউজার রেজিস্ট্রেশন
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

# ৪. ইউজার ড্যাশবোর্ড
@login_required
def dashboard(request):
    user_apps = UploadedContent.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')
    return render(request, 'dashboard.html', {'user_apps': user_apps})

# ৫. কন্টেন্ট আপলোড লজিক
@login_required
def upload_content(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        content_type = request.POST.get('content_type')
        uploaded_file = request.FILES.get('file')
        logo_file = request.FILES.get('logo')

        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            
            if not request.user.is_superuser:
                if ext != '.apk':
                    return render(request, 'upload.html', {'error': 'অন্য ইউজাররা শুধুমাত্র .apk ফাইল আপলোড করতে পারবেন।'})
                content_type = 'app'

            UploadedContent.objects.create(
                title=title, 
                description=description,
                content_type=content_type, 
                file=uploaded_file,
                logo=logo_file,
                uploaded_by=request.user
            )
            return redirect('dashboard')
    return render(request, 'upload.html')

# ৬. অ্যাপ ডিটেইলস পেজ
def app_detail(request, pk):
    item = get_object_or_404(UploadedContent, pk=pk)
    related_apps = UploadedContent.objects.exclude(pk=pk).order_by('?')[:4]
    return render(request, 'app_detail.html', {'item': item, 'related_apps': related_apps})

# ৭. ডাউনলোড ট্র্যাক ও ফাইল ডেলিভারি
def download_file(request, pk):
    item = get_object_or_404(UploadedContent, pk=pk)
    item.downloads += 1
    item.save()
    return redirect(item.file.url)

# ৮. ক্রিয়েটর অ্যানালিটিক্স
@login_required
def analytics_dashboard(request):
    user_apps = UploadedContent.objects.filter(uploaded_by=request.user).order_by('-downloads')
    total_apps = user_apps.count()
    total_downloads = user_apps.aggregate(Sum('downloads'))['downloads__sum'] or 0
    
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

# ৯. লিডারবোর্ড (টপ ডেভেলপারস)
def leaderboard(request):
    top_developers = User.objects.annotate(
        total_downloads=Sum('uploadedcontent__downloads')
    ).filter(total_downloads__gt=0).order_by('-total_downloads')[:5]
    return render(request, 'leaderboard.html', {'top_developers': top_developers})

# ১০. পাবলিক ডেভেলপার প্রোফাইল
def developer_profile_view(request, username):
    developer = get_object_or_404(User, username=username)
    dev_apps = UploadedContent.objects.filter(uploaded_by=developer).order_by('-uploaded_at')
    total_downloads = dev_apps.aggregate(Sum('downloads'))['downloads__sum'] or 0
    most_downloaded = dev_apps.order_by('-downloads').first()
    top_rated = dev_apps.order_by('-rating').first()

    return render(request, 'developer_profile.html', {
        'developer': developer,
        'dev_apps': dev_apps,
        'total_downloads': total_downloads,
        'most_downloaded': most_downloaded,
        'top_rated': top_rated,
        'app_count': dev_apps.count(),
    })

# ১০ নম্বর ফাংশনের পরে এটি যোগ করুন
def trending_apps(request):
    # সবথেকে বেশি ডাউনলোড হওয়া ১০টি অ্যাপ বাছাই করা
    top_apps = UploadedContent.objects.order_by('-downloads', '-rating')[:10]
    return render(request, 'trending.html', {'top_apps': top_apps})

# ১১. অন্যান্য স্ট্যাটিক পেজ
def faq_view(request):
    return render(request, 'faq.html')

def privacy_view(request):
    return render(request, 'privacy_policy.html')

def changelog_view(request):
    return render(request, 'change_log.html')

def customer_care(request):
    return render(request, 'customer_care.html')

# ১২. অ্যাপ রিকোয়েস্ট লজিক
def app_request_view(request):
    if request.method == "POST":
        app_name = request.POST.get('app_name')
        description = request.POST.get('description')
        user_email = request.POST.get('user_email')
        AppRequest.objects.create(app_name=app_name, description=description, user_email=user_email)
        return redirect('home')
    return render(request, 'app_request.html')

# ১৩. রেটিং আপডেট (AJAX)
@csrf_exempt
def update_rating(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        content = UploadedContent.objects.get(id=data.get('id'))
        # আপনার মডেলে যদি total_votes না থাকে তবে এটি এরর দিবে। 
        # যদি না থাকে তবে এই ফাংশনটি এড়িয়ে চলুন।
        return JsonResponse({'status': 'success'})