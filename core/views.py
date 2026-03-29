from django.shortcuts import render, redirect
from .models import UploadedContent
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

def splash_screen(request):
    return render(request, 'splash.html')

def home(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    contents = UploadedContent.objects.all().order_by('-created_at')

    if query:
        contents = contents.filter(title__icontains=query)
    if category and category != 'all':
        contents = contents.filter(content_type=category)

    return render(request, 'home.html', {'contents': contents})

@csrf_exempt
def update_rating(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        content_id = data.get('id')
        new_score = int(data.get('score'))
        content = UploadedContent.objects.get(id=content_id)
        
        current_total_score = content.rating * content.total_votes
        content.total_votes += 1
        content.rating = (current_total_score + new_score) / content.total_votes
        content.save()
        return JsonResponse({'status': 'success', 'new_rating': round(content.rating, 1)})

@login_required
def upload_content(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        content_type = request.POST.get('content_type')
        uploaded_file = request.FILES.get('file')

        if uploaded_file:
            UploadedContent.objects.create(
                title=title, description=description,
                content_type=content_type, file=uploaded_file,
                uploaded_by=request.user
            )
            return JsonResponse({'status': 'success'})
    return render(request, 'upload.html')