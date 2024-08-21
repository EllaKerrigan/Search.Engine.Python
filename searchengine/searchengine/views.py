from django.shortcuts import render
from search.search_engine_module import search
from search.models import Post

def index(requests):
    return render(requests, 'search/index.html')

def results(request):
    query = request.GET.get('q', '')
    print(f"Query received: {query}")  # Debug line
    results = Post.objects.filter(title__icontains=query)
    print(f"Results found: {results}")  # Debug line
    return render(request, 'search/results.html', {'query': query, 'results': results})
