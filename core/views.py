import os
import json
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import UploadedContent
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def splash_screen(request):
    return render(request, 'splash.html')

# হোম পেজ (ফিল্টার ও সার্চ ঠিক রাখা হয়েছে)
def home(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    contents = UploadedContent.objects.all().order_by('-created_at')

    if query:
        contents = contents.filter(title__icontains=query)
    if category and category != 'all':
        contents = contents.filter(content_type=category)

    return render(request, 'home.html', {'contents': contents})

# নতুন ইউজার রেজিস্ট্রেশন
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# আপলোড লজিক (সুপার-ইউজার বনাম সাধারণ ইউজার)
@login_required
def upload_content(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        content_type = request.POST.get('content_type')
        uploaded_file = request.FILES.get('file')

        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            
            # তুমি (Superuser) সব পারবে, অন্যরা শুধু APK
            if not request.user.is_superuser:
                if ext != '.apk':
                    return render(request, 'upload.html', {'error': 'অন্য ইউজাররা শুধুমাত্র .apk ফাইল আপলোড করতে পারবেন।'})
                content_type = 'app'

            UploadedContent.objects.create(
                title=title, description=description,
                content_type=content_type, file=uploaded_file,
                uploaded_by=request.user
            )
            return redirect('home')
    return render(request, 'upload.html')

# রেটিং লজিক (আগেরটাই আছে)
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