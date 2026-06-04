from django.shortcuts import render

def create_offer_request(request):
    return render(request, 'create_offer_request.html')

def discover_page(request):
    return render(request, 'discover_page.html')

def offer_request_detail(request):
    return render(request, 'offer_request_detail.html')

def offer_request_feed(request):
    return render(request, 'offer_request_feed.html')

def search_results(request):
    return render(request, 'search_results.html')
