"""
CRUD Views untuk Category, Tag, Testimoni, Pengumuman - Semua dalam 1 file
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django_htmx.http import HttpResponseClientRefresh, HttpResponseClientRedirect
from .models import Category, Tag, Testimoni, Pengumuman
from .forms import CategoryForm, TagForm, TestimoniForm, PengumumanForm


def is_staff_user(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def is_htmx_request(request):
    return request.headers.get('HX-Request') == 'true'


# ==================== CATEGORY CRUD ====================
@login_required
@user_passes_test(is_staff_user)
def category_list(request):
    """List semua kategori dengan form untuk modal"""
    categories = Category.objects.all().order_by('order', 'name')
    search = request.GET.get('search', '')
    if search:
        categories = categories.filter(name__icontains=search)
    
    paginator = Paginator(categories, 20)
    page = paginator.get_page(request.GET.get('page', 1))
    
    # Prepare form for modal
    category_id = request.GET.get('edit', None)
    form = None
    category = None
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        form = CategoryForm(instance=category)
    else:
        form = CategoryForm()
    
    return render(request, 'admin-panel/blog/category_list.html', {
        'categories': page,
        'search': search,
        'form': form,
        'category': category,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def category_form(request, category_id=None):
    """Create/Update category - Handle POST from modal"""
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        form = CategoryForm(request.POST, instance=category)
    else:
        form = CategoryForm(request.POST)
    
    if form.is_valid():
        form.save()
        messages.success(request, f'Kategori berhasil {"diupdate" if category_id else "ditambahkan"}!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('blog:category_list')
    
    # If form invalid, redirect back to list
    return redirect('blog:category_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def category_delete(request, category_id):
    """Delete category"""
    category = get_object_or_404(Category, id=category_id)
    name = category.name
    category.delete()
    messages.success(request, f'Kategori "{name}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('blog:category_list')


# ==================== TAG CRUD ====================
@login_required
@user_passes_test(is_staff_user)
def tag_list(request):
    """List semua tag dengan form untuk modal"""
    tags = Tag.objects.all().order_by('order', 'name')
    search = request.GET.get('search', '')
    if search:
        tags = tags.filter(name__icontains=search)
    
    paginator = Paginator(tags, 20)
    page = paginator.get_page(request.GET.get('page', 1))
    
    # Prepare form for modal
    tag_id = request.GET.get('edit', None)
    form = None
    tag = None
    if tag_id:
        tag = get_object_or_404(Tag, id=tag_id)
        form = TagForm(instance=tag)
    else:
        form = TagForm()
    
    return render(request, 'admin-panel/blog/tag_list.html', {
        'tags': page,
        'search': search,
        'form': form,
        'tag': tag,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def tag_form(request, tag_id=None):
    """Create/Update tag - Handle POST from modal"""
    if tag_id:
        tag = get_object_or_404(Tag, id=tag_id)
        form = TagForm(request.POST, instance=tag)
    else:
        form = TagForm(request.POST)
    
    if form.is_valid():
        form.save()
        messages.success(request, f'Tag berhasil {"diupdate" if tag_id else "ditambahkan"}!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('blog:tag_list')
    
    # If form invalid, redirect back to list
    return redirect('blog:tag_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def tag_delete(request, tag_id):
    """Delete tag"""
    tag = get_object_or_404(Tag, id=tag_id)
    name = tag.name
    tag.delete()
    messages.success(request, f'Tag "{name}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('blog:tag_list')


# ==================== TESTIMONI CRUD ====================
@login_required
@user_passes_test(is_staff_user)
def testimoni_list(request):
    """List semua testimoni dengan form untuk modal"""
    testimoni = Testimoni.objects.all().order_by('order', '-created_at')
    search = request.GET.get('search', '')
    if search:
        testimoni = testimoni.filter(Q(nama__icontains=search) | Q(jabatan__icontains=search))
    
    paginator = Paginator(testimoni, 20)
    page = paginator.get_page(request.GET.get('page', 1))
    
    # Prepare form for modal
    testimoni_id = request.GET.get('edit', None)
    form = None
    testimoni_obj = None
    if testimoni_id:
        testimoni_obj = get_object_or_404(Testimoni, id=testimoni_id)
        form = TestimoniForm(instance=testimoni_obj)
    else:
        form = TestimoniForm()
    
    return render(request, 'admin-panel/blog/testimoni_list.html', {
        'testimoni': page,
        'search': search,
        'form': form,
        'testimoni_obj': testimoni_obj,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def testimoni_form(request, testimoni_id=None):
    """Create/Update testimoni - Handle POST from modal"""
    from admin_panel.models import ConvertedImage
    from django.core.files import File
    import os
    
    if testimoni_id:
        testimoni = get_object_or_404(Testimoni, id=testimoni_id)
        form = TestimoniForm(request.POST, request.FILES, instance=testimoni)
    else:
        form = TestimoniForm(request.POST, request.FILES)
    
    if form.is_valid():
        # Handle selected_image_id dari image picker
        selected_image_id = request.POST.get('selected_image_id')
        if selected_image_id:
            try:
                converted_image = ConvertedImage.objects.get(id=selected_image_id)
                # Langsung gunakan path dari media/converted tanpa copy file
                if converted_image.webp_image:
                    testimoni_obj = form.save(commit=False)
                    # Set path langsung dari ConvertedImage (tidak copy file)
                    testimoni_obj.foto = converted_image.webp_image
                    testimoni_obj.save()
                    messages.success(request, f'Testimoni berhasil {"diupdate" if testimoni_id else "ditambahkan"}!')
                    if is_htmx_request(request):
                        return HttpResponseClientRefresh()
                    return redirect('blog:testimoni_list')
            except ConvertedImage.DoesNotExist:
                pass
        
        form.save()
        messages.success(request, f'Testimoni berhasil {"diupdate" if testimoni_id else "ditambahkan"}!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('blog:testimoni_list')
    
    # If form invalid, redirect back to list
    return redirect('blog:testimoni_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def testimoni_delete(request, testimoni_id):
    """Delete testimoni"""
    testimoni = get_object_or_404(Testimoni, id=testimoni_id)
    name = testimoni.nama
    testimoni.delete()
    messages.success(request, f'Testimoni "{name}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('blog:testimoni_list')


# ==================== PENGUMUMAN CRUD ====================
@login_required
@user_passes_test(is_staff_user)
def pengumuman_list(request):
    """List semua pengumuman dengan form untuk modal"""
    pengumuman = Pengumuman.objects.all().order_by('-is_penting', '-published_at', '-created_at')
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    
    if search:
        pengumuman = pengumuman.filter(judul__icontains=search)
    if status:
        pengumuman = pengumuman.filter(status=status)
    
    paginator = Paginator(pengumuman, 20)
    page = paginator.get_page(request.GET.get('page', 1))
    
    # Prepare form for modal
    pengumuman_id = request.GET.get('edit', None)
    form = None
    pengumuman_obj = None
    if pengumuman_id:
        pengumuman_obj = get_object_or_404(Pengumuman, id=pengumuman_id)
        form = PengumumanForm(instance=pengumuman_obj)
    else:
        form = PengumumanForm()
    
    return render(request, 'admin-panel/blog/pengumuman_list.html', {
        'pengumuman': page,
        'search': search,
        'status': status,
        'form': form,
        'pengumuman_obj': pengumuman_obj,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def pengumuman_form(request, pengumuman_id=None):
    """Create/Update pengumuman - Handle POST from modal"""
    from admin_panel.models import ConvertedImage
    from django.core.files import File
    import os
    
    if pengumuman_id:
        pengumuman = get_object_or_404(Pengumuman, id=pengumuman_id)
        form = PengumumanForm(request.POST, request.FILES, instance=pengumuman)
    else:
        form = PengumumanForm(request.POST, request.FILES)
    
    if form.is_valid():
        # Handle selected_image_id dari image picker
        selected_image_id = request.POST.get('selected_image_id')
        if selected_image_id:
            try:
                converted_image = ConvertedImage.objects.get(id=selected_image_id)
                # Langsung gunakan path dari media/converted tanpa copy file
                if converted_image.webp_image:
                    pengumuman_obj = form.save(commit=False)
                    # Set path langsung dari ConvertedImage (tidak copy file)
                    pengumuman_obj.gambar = converted_image.webp_image
                    pengumuman_obj.save()
                    messages.success(request, f'Pengumuman berhasil {"diupdate" if pengumuman_id else "ditambahkan"}!')
                    if is_htmx_request(request):
                        return HttpResponseClientRefresh()
                    return redirect('blog:pengumuman_list')
            except ConvertedImage.DoesNotExist:
                pass
        
        form.save()
        messages.success(request, f'Pengumuman berhasil {"diupdate" if pengumuman_id else "ditambahkan"}!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('blog:pengumuman_list')
    
    # If form invalid, redirect back to list
    return redirect('blog:pengumuman_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def pengumuman_delete(request, pengumuman_id):
    """Delete pengumuman"""
    pengumuman = get_object_or_404(Pengumuman, id=pengumuman_id)
    judul = pengumuman.judul
    pengumuman.delete()
    messages.success(request, f'Pengumuman "{judul}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('blog:pengumuman_list')

