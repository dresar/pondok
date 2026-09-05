"""
Forms untuk Blog Management dengan Summernote
"""
from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import BlogPost, Category, Tag, Testimoni, Pengumuman


class BlogPostForm(forms.ModelForm):
    """Form untuk Create dan Update Blog Post dengan Summernote"""
    
    class Meta:
        model = BlogPost
        fields = [
            'title', 'slug', 'author', 'content', 'excerpt', 'featured_image',
            'category', 'tags', 'meta_title', 'meta_description', 'meta_keywords',
            'video_file', 'status', 'published_at', 'is_featured'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Judul artikel...'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'slug-artikel (otomatis dari judul)'
            }),
            'author': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white'
            }),
            'content': SummernoteWidget(attrs={
                'summernote': {
                    'width': '100%',
                    'height': '500',
                    'toolbar': [
                        ['style', ['style']],
                        ['font', ['bold', 'italic', 'underline', 'clear']],
                        ['fontname', ['fontname']],
                        ['fontsize', ['fontsize']],
                        ['color', ['color']],
                        ['para', ['ul', 'ol', 'paragraph']],
                        ['table', ['table']],
                        ['insert', ['link', 'picture', 'video']],
                        ['view', ['fullscreen', 'codeview', 'help']],
                    ],
                }
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none',
                'rows': 3,
                'placeholder': 'Ringkasan artikel (untuk SEO dan preview)...'
            }),
            'featured_image': forms.ClearableFileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100',
                'accept': 'image/*'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white',
                'size': 5
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Meta title untuk SEO (default: judul artikel)',
                'maxlength': '200'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none',
                'rows': 3,
                'placeholder': 'Meta description untuk SEO (max 300 karakter)',
                'maxlength': '300'
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Kata kunci dipisahkan koma (contoh: pondok, pesantren, pendidikan)'
            }),
            'video_file': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100',
                'accept': 'video/*'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white'
            }),
            'published_at': forms.DateTimeInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'type': 'datetime-local'
            }, format='%Y-%m-%dT%H:%M'),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500'
            }),
        }
        labels = {
            'title': 'Judul Artikel',
            'slug': 'Slug (URL)',
            'author': 'Penulis',
            'content': 'Konten Artikel',
            'excerpt': 'Ringkasan/Excerpt',
            'featured_image': 'Gambar Utama',
            'category': 'Kategori',
            'tags': 'Tag',
            'meta_title': 'Meta Title (SEO)',
            'meta_description': 'Meta Description (SEO)',
            'meta_keywords': 'Meta Keywords (SEO)',
            'video_file': 'File Video (Upload)',
            'status': 'Status',
            'published_at': 'Tanggal Publikasi',
            'is_featured': 'Artikel Unggulan',
        }


class CategoryForm(forms.ModelForm):
    """Form untuk Category"""
    
    class Meta:
        model = Category
        fields = ['name', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
        }


class TagForm(forms.ModelForm):
    """Form untuk Tag"""
    
    class Meta:
        model = Tag
        fields = ['name', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
        }


class TestimoniForm(forms.ModelForm):
    """Form untuk Testimoni"""
    
    class Meta:
        model = Testimoni
        fields = ['nama', 'foto', 'jabatan', 'testimoni', 'rating', 'is_published']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100',
                'accept': 'image/*'
            }),
            'jabatan': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'testimoni': SummernoteWidget(attrs={
                'summernote': {
                    'width': '100%',
                    'height': '300',
                    'toolbar': [
                        ['style', ['style']],
                        ['font', ['bold', 'italic', 'underline', 'clear']],
                        ['para', ['ul', 'ol', 'paragraph']],
                        ['insert', ['link']],
                    ],
                }
            }),
            'rating': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500'
            }),
        }


class PengumumanForm(forms.ModelForm):
    """Form untuk Pengumuman"""
    
    class Meta:
        model = Pengumuman
        fields = ['judul', 'slug', 'konten', 'gambar', 'status', 'is_penting', 'published_at', 'meta_title', 'meta_description']
        widgets = {
            'judul': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'konten': SummernoteWidget(attrs={
                'summernote': {
                    'width': '100%',
                    'height': '400',
                }
            }),
            'gambar': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100',
                'accept': 'image/*'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white'
            }),
            'is_penting': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500'
            }),
            'published_at': forms.DateTimeInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'type': 'datetime-local'
            }, format='%Y-%m-%dT%H:%M'),
            'meta_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none',
                'rows': 3
            }),
        }

