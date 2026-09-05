/**
 * Image Picker JavaScript - Reusable Component
 * Untuk memilih gambar dari ConvertedImage gallery
 */

let imagePickerConfig = {
    currentPage: 1,
    searchQuery: '',
    selectedImageId: null,
    selectedImageUrl: null,
    callback: null, // Callback function ketika gambar dipilih
    targetInputId: null, // ID input field yang akan diisi dengan URL gambar
    targetPreviewId: null, // ID element untuk preview gambar
};

/**
 * Buka image picker modal
 * @param {Object} options - Konfigurasi
 * @param {Function} options.onSelect - Callback ketika gambar dipilih
 * @param {String} options.targetInputId - ID input field untuk URL gambar
 * @param {String} options.targetPreviewId - ID element untuk preview
 */
function openImagePicker(options = {}) {
    imagePickerConfig.callback = options.onSelect || null;
    imagePickerConfig.targetInputId = options.targetInputId || null;
    imagePickerConfig.targetPreviewId = options.targetPreviewId || null;
    imagePickerConfig.currentPage = 1;
    imagePickerConfig.searchQuery = '';
    
    const modal = document.getElementById('image-picker-modal');
    if (modal) {
        // Pastikan modal di atas semua elemen termasuk sidebar
        modal.style.zIndex = '10000';
        modal.style.position = 'fixed';
        modal.style.top = '0';
        modal.style.left = '0';
        modal.style.right = '0';
        modal.style.bottom = '0';
        
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden'; // Prevent background scroll
        
        // Pastikan modal content juga di atas
        const modalContent = modal.querySelector('div.bg-white');
        if (modalContent) {
            modalContent.style.zIndex = '10001';
            modalContent.style.position = 'relative';
        }
        
        loadImages();
    }
}

/**
 * Tutup image picker modal
 */
function closeImagePicker() {
    const modal = document.getElementById('image-picker-modal');
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = ''; // Restore scroll
        // Reset z-index
        modal.style.zIndex = '';
    }
    // Reset
    imagePickerConfig.selectedImageId = null;
    imagePickerConfig.selectedImageUrl = null;
}

/**
 * Load images dari API
 */
function loadImages(page = null) {
    if (page !== null) {
        imagePickerConfig.currentPage = page;
    }
    
    const gallery = document.getElementById('image-picker-gallery');
    const loading = document.getElementById('image-picker-loading');
    const empty = document.getElementById('image-picker-empty');
    const pagination = document.getElementById('image-picker-pagination');
    
    // Show loading
    gallery.innerHTML = '';
    loading.classList.remove('hidden');
    empty.classList.add('hidden');
    pagination.classList.add('hidden');
    
    // Build URL
    const url = new URL('/admin-panel/tools/converted-images/search/', window.location.origin);
    url.searchParams.append('page', imagePickerConfig.currentPage);
    url.searchParams.append('per_page', '20');
    if (imagePickerConfig.searchQuery) {
        url.searchParams.append('search', imagePickerConfig.searchQuery);
    }
    
    // Fetch images
    fetch(url.toString(), {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        loading.classList.add('hidden');
        
        if (data.images && data.images.length > 0) {
            // Render images
            gallery.innerHTML = data.images.map(img => `
                <div class="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-all overflow-hidden group cursor-pointer image-picker-item"
                     data-image-id="${img.id}"
                     data-image-url="${img.gambar_url}"
                     onclick="selectImage(${img.id}, '${img.gambar_url}', '${img.judul.replace(/'/g, "\\'")}')">
                    <div class="relative aspect-video bg-gray-100 overflow-hidden">
                        <img src="${img.gambar_url}" alt="${img.judul}" 
                             class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
                        <div class="absolute top-2 right-2">
                            <span class="px-2 py-1 text-xs font-semibold rounded-full bg-green-600 text-white">
                                WebP
                            </span>
                        </div>
                        <div class="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-all flex items-center justify-center opacity-0 group-hover:opacity-100">
                            <span class="bg-white text-gray-900 px-3 py-1 rounded-lg text-xs font-semibold">
                                <i class="fas fa-check mr-1"></i>Pilih
                            </span>
                        </div>
                    </div>
                    <div class="p-3">
                        <h4 class="font-semibold text-gray-900 text-xs line-clamp-1" title="${img.judul}">
                            ${img.judul}
                        </h4>
                        <p class="text-xs text-gray-500 mt-1">${img.dimensions} • ${img.file_size} KB</p>
                    </div>
                </div>
            `).join('');
            
            // Show pagination if needed
            if (data.total_pages > 1) {
                pagination.classList.remove('hidden');
                document.getElementById('image-picker-page-info').textContent = 
                    `Halaman ${data.page} dari ${data.total_pages} (${data.total_count} gambar)`;
                document.getElementById('image-picker-prev').disabled = !data.has_previous;
                document.getElementById('image-picker-next').disabled = !data.has_next;
            } else {
                pagination.classList.add('hidden');
            }
        } else {
            empty.classList.remove('hidden');
        }
    })
    .catch(error => {
        console.error('Error loading images:', error);
        loading.classList.add('hidden');
        gallery.innerHTML = `
            <div class="col-span-full text-center py-12 text-red-500">
                <i class="fas fa-exclamation-circle text-4xl mb-4"></i>
                <p>Gagal memuat gambar. Silakan coba lagi.</p>
            </div>
        `;
    });
}

/**
 * Search images
 */
function searchImages(query) {
    imagePickerConfig.searchQuery = query;
    imagePickerConfig.currentPage = 1;
    loadImages();
}

/**
 * Load next/prev page
 */
function loadImagesPage(direction) {
    if (direction === 'next') {
        imagePickerConfig.currentPage++;
    } else if (direction === 'prev') {
        imagePickerConfig.currentPage--;
    }
    loadImages();
}

/**
 * Select image
 */
function selectImage(imageId, imageUrl, imageTitle) {
    imagePickerConfig.selectedImageId = imageId;
    imagePickerConfig.selectedImageUrl = imageUrl;
    
    // JANGAN set value pada file input (tidak bisa di-set secara programmatic)
    // Gunakan hidden input untuk menyimpan image ID
    const hiddenInputId = 'selected_image_id';
    let hiddenInput = document.getElementById(hiddenInputId);
    
    if (!hiddenInput) {
        // Buat hidden input jika belum ada
        hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.id = hiddenInputId;
        hiddenInput.name = hiddenInputId;
        
        // Cari form terdekat dan tambahkan hidden input
        const form = document.querySelector('form[method="post"]') || document.querySelector('form');
        if (form) {
            form.appendChild(hiddenInput);
        }
    }
    
    // Set image ID ke hidden input
    hiddenInput.value = imageId;
    
    // Clear file input jika ada (untuk menghindari konflik)
    if (imagePickerConfig.targetInputId) {
        const fileInput = document.getElementById(imagePickerConfig.targetInputId);
        if (fileInput && fileInput.type === 'file') {
            // File input tidak bisa di-set value, jadi kita clear dengan membuat input baru
            // Atau biarkan kosong, view akan handle selected_image_id
        }
    }
    
    // Update preview if provided
    if (imagePickerConfig.targetPreviewId) {
        const preview = document.getElementById(imagePickerConfig.targetPreviewId);
        if (preview) {
            if (preview.tagName === 'IMG') {
                preview.src = imageUrl;
                preview.style.display = 'block';
            } else {
                preview.innerHTML = `<img src="${imageUrl}" alt="${imageTitle}" class="w-full h-auto rounded-lg">`;
                preview.style.display = 'block';
            }
        }
    }
    
    // Call callback if provided
    if (imagePickerConfig.callback && typeof imagePickerConfig.callback === 'function') {
        imagePickerConfig.callback(imageId, imageUrl, imageTitle);
    }
    
    // Close modal
    closeImagePicker();
}

// Close modal dengan ESC key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const modal = document.getElementById('image-picker-modal');
        if (modal && !modal.classList.contains('hidden')) {
            closeImagePicker();
        }
    }
});

// Prevent modal close when clicking inside
document.getElementById('image-picker-modal')?.addEventListener('click', function(e) {
    if (e.target === this) {
        closeImagePicker();
    }
});

