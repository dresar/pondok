"""
Views untuk Blog Management di Admin Panel
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django_htmx.http import HttpResponseClientRefresh, HttpResponseClientRedirect
from .models import BlogPost, Category, Tag
from .forms import BlogPostForm, CategoryForm, TagForm


def is_staff_user(user):
    """Check if user is staff"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def is_htmx_request(request):
    """Helper untuk check apakah request dari HTMX"""
    return request.headers.get('HX-Request') == 'true'


# ==================== BLOG POST CRUD ====================
@login_required
@user_passes_test(is_staff_user)
def blog_list(request):
    """Daftar semua blog post dengan search, filter, dan pagination"""
    # Hindari select_related('category') karena mungkin ada masalah dengan field yang sudah dihapus
    blog_queryset = BlogPost.objects.select_related('author').prefetch_related('tags').all()
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        blog_queryset = blog_queryset.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        blog_queryset = blog_queryset.filter(status=status_filter)
    
    # Filter by category
    category_filter = request.GET.get('category', '')
    if category_filter:
        blog_queryset = blog_queryset.filter(category_id=category_filter)
    
    # Ordering
    order_by = request.GET.get('order_by', '-created_at')
    if order_by:
        blog_queryset = blog_queryset.order_by(order_by)
    
    # Pagination - 18 items per page untuk desktop
    paginator = Paginator(blog_queryset, 18)
    page_number = request.GET.get('page', 1)
    blog_page = paginator.get_page(page_number)
    
    # Load categories untuk setiap post secara terpisah untuk menghindari masalah dengan select_related
    for post in blog_page:
        if post.category_id:
            try:
                post.category = Category.objects.only('id', 'name', 'slug', 'order', 'created_at').get(id=post.category_id)
            except Category.DoesNotExist:
                post.category = None
    
    # Get categories for filter - hanya ambil field yang ada
    categories = Category.objects.only('id', 'name', 'slug', 'order', 'created_at').all()
    
    context = {
        'blog_posts': blog_page,
        'search_query': search_query,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'order_by': order_by,
        'categories': categories,
    }
    
    return render(request, 'admin-panel/blog/list.html', context)


@login_required
@user_passes_test(is_staff_user)
def blog_detail(request, blog_id):
    """Detail blog post"""
    # Hindari select_related('category') karena mungkin ada masalah dengan field yang sudah dihapus
    blog_post = get_object_or_404(BlogPost.objects.select_related('author').prefetch_related('tags'), id=blog_id)
    # Load category secara terpisah jika ada
    if blog_post.category_id:
        try:
            blog_post.category = Category.objects.only('id', 'name', 'slug', 'order', 'created_at').get(id=blog_post.category_id)
        except Category.DoesNotExist:
            blog_post.category = None
    
    context = {
        'blog_post': blog_post,
    }
    return render(request, 'admin-panel/blog/detail.html', context)


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["GET", "POST"])
def blog_create(request):
    """Create blog post baru"""
    from admin_panel.models import ConvertedImage
    from django.core.files import File
    import os
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle selected_image_id dari image picker
            selected_image_id = request.POST.get('selected_image_id')
            if selected_image_id:
                try:
                    converted_image = ConvertedImage.objects.get(id=selected_image_id)
                    # Langsung gunakan path dari media/converted tanpa copy file
                    if converted_image.webp_image:
                        blog_post = form.save(commit=False)
                        # Set path langsung dari ConvertedImage (tidak copy file)
                        blog_post.featured_image = converted_image.webp_image
                        if not blog_post.author_id:
                            blog_post.author = request.user
                        blog_post.save()
                        form.save_m2m()  # Save many-to-many (tags)
                        messages.success(request, f'Artikel "{blog_post.title}" berhasil ditambahkan!')
                        
                        if is_htmx_request(request):
                            return HttpResponseClientRedirect(f'/admin-panel/blog/{blog_post.id}/')
                        return redirect('blog:detail', blog_id=blog_post.id)
                except ConvertedImage.DoesNotExist:
                    pass
            
            blog_post = form.save(commit=False)
            if not blog_post.author_id:
                blog_post.author = request.user
            blog_post.save()
            form.save_m2m()  # Save many-to-many (tags)
            messages.success(request, f'Artikel "{blog_post.title}" berhasil ditambahkan!')
            
            if is_htmx_request(request):
                return HttpResponseClientRedirect(f'/admin-panel/blog/{blog_post.id}/')
            return redirect('blog:detail', blog_id=blog_post.id)
        else:
            messages.error(request, 'Terdapat kesalahan dalam pengisian form.')
    else:
        form = BlogPostForm(initial={'author': request.user})
    
    context = {
        'form': form,
        'form_title': 'Tambah Artikel Baru',
        'submit_url': 'blog:create',
    }
    return render(request, 'admin-panel/blog/form.html', context)


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["GET", "POST"])
def blog_update(request, blog_id):
    """Update blog post"""
    from admin_panel.models import ConvertedImage
    from django.core.files import File
    import os
    
    blog_post = get_object_or_404(BlogPost, id=blog_id)
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog_post)
        if form.is_valid():
            # Handle selected_image_id dari image picker
            selected_image_id = request.POST.get('selected_image_id')
            if selected_image_id:
                try:
                    converted_image = ConvertedImage.objects.get(id=selected_image_id)
                    # Langsung gunakan path dari media/converted tanpa copy file
                    if converted_image.webp_image:
                        blog_post_obj = form.save(commit=False)
                        # Set path langsung dari ConvertedImage (tidak copy file)
                        blog_post_obj.featured_image = converted_image.webp_image
                        if not blog_post_obj.author_id:
                            blog_post_obj.author = request.user
                        blog_post_obj.save()
                        form.save_m2m()  # Save many-to-many (tags)
                        messages.success(request, f'Artikel "{blog_post_obj.title}" berhasil diupdate!')
                        
                        if is_htmx_request(request):
                            return HttpResponseClientRedirect(f'/admin-panel/blog/{blog_post_obj.id}/')
                        return redirect('blog:detail', blog_id=blog_post_obj.id)
                except ConvertedImage.DoesNotExist:
                    pass
            
            # ClearableFileInput akan handle file upload/clear secara otomatis
            blog_post = form.save(commit=False)
            if not blog_post.author_id:
                blog_post.author = request.user
            blog_post.save()
            form.save_m2m()  # Save many-to-many (tags)
            messages.success(request, f'Artikel "{blog_post.title}" berhasil diupdate!')
            
            if is_htmx_request(request):
                return HttpResponseClientRedirect(f'/admin-panel/blog/{blog_post.id}/')
            return redirect('blog:detail', blog_id=blog_post.id)
        else:
            messages.error(request, 'Terdapat kesalahan dalam pengisian form.')
            # Debug: print form errors
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Form error - {field}: {error}")
    else:
        form = BlogPostForm(instance=blog_post)
    
    context = {
        'form': form,
        'blog_post': blog_post,
        'form_title': f'Edit Artikel: {blog_post.title}',
        'submit_url': 'blog:update',
        'submit_url_kwargs': {'blog_id': blog_post.id},
    }
    return render(request, 'admin-panel/blog/form.html', context)


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def blog_delete(request, blog_id):
    """Delete blog post - menggunakan modal dari list page"""
    blog_post = get_object_or_404(BlogPost, id=blog_id)
    
    if request.method == 'DELETE' or (request.method == 'POST' and request.POST.get('_method') == 'DELETE'):
        title = blog_post.title
        blog_post.delete()
        messages.success(request, f'Artikel "{title}" berhasil dihapus!')
        
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('blog:list')
    
    # Jika GET request, redirect ke list (modal sudah ada di list page)
    return redirect('blog:list')


# ==================== STATISTICS ====================
@login_required
@user_passes_test(is_staff_user)
def blog_increment_likes(request, blog_id):
    """Increment likes count (AJAX)"""
    if request.method == 'POST':
        blog_post = get_object_or_404(BlogPost, id=blog_id)
        blog_post.increment_likes()
        return JsonResponse({'likes_count': blog_post.likes_count})
    return JsonResponse({'error': 'Invalid method'}, status=400)


@login_required
@user_passes_test(is_staff_user)
def blog_increment_shares(request, blog_id):
    """Increment shares count (AJAX)"""
    if request.method == 'POST':
        blog_post = get_object_or_404(BlogPost, id=blog_id)
        blog_post.increment_shares()
        return JsonResponse({'shares_count': blog_post.shares_count})
    return JsonResponse({'error': 'Invalid method'}, status=400)
