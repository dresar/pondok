from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import DocumentTemplate


class DocumentTemplateForm(forms.ModelForm):
    """Form untuk create/edit template dokumen dengan Summernote"""
    
    class Meta:
        model = DocumentTemplate
        fields = [
            'nama', 'slug', 'deskripsi', 'html_template', 'css_template',
            'ukuran_kertas', 'orientasi', 'margin_top', 'margin_right', 
            'margin_bottom', 'margin_left', 'is_active', 'order'
        ]
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Nama template, contoh: Form A.1'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'URL-friendly identifier (otomatis dari nama)'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'rows': 2,
                'placeholder': 'Deskripsi singkat tentang template ini'
            }),
            'html_template': SummernoteWidget(attrs={
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
                        ['insert', ['link', 'picture']],
                        ['view', ['fullscreen', 'codeview', 'help']],
                    ],
                    'codeviewFilter': True,
                    'codeviewIframeFilter': True,
                }
            }),
            'css_template': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent font-mono text-sm',
                'rows': 15,
                'placeholder': '@page { size: A4; margin: 1.5cm; }\nbody { font-family: "Times New Roman", serif; }'
            }),
            'ukuran_kertas': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white'
            }),
            'orientasi': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white'
            }),
            'margin_top': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': '1.5cm'
            }),
            'margin_right': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': '1.5cm'
            }),
            'margin_bottom': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': '1.5cm'
            }),
            'margin_left': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': '1.5cm'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'min': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500'
            }),
        }

