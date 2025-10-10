from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import ContactMessage, Product
from .forms import ContactForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required




def home(request):
    
    featured_products = Product.objects.filter(is_featured=True)[:8]
    return render(request, 'store/home.html', {'featured_products': featured_products})


def product_list(request):
    qs = Product.objects.order_by('-created_at')
    paginator = Paginator(qs, 9)  
    page_num = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_num)
    return render(request, 'store/product_list.html', {'page_obj': page_obj})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

def about(request):
    return render(request, 'store/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_text = request.POST.get('message')

      
        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message_text
        )

       
        messages.success(request, '✅ Your message has been sent successfully!')

        
        return redirect('contact')

    return render(request, 'store/contact.html')
