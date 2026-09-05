// Sejarah Gallery Slideshow
document.addEventListener('DOMContentLoaded', function() {
    const galleryTrack = document.querySelector('.sejarah-gallery-track');
    const gallerySlides = document.querySelectorAll('.sejarah-gallery-slide');
    const prevBtn = document.querySelector('.sejarah-gallery-prev');
    const nextBtn = document.querySelector('.sejarah-gallery-next');
    const dots = document.querySelectorAll('.sejarah-gallery-dot');
    
    if (!galleryTrack || gallerySlides.length === 0) return;
    
    let currentSlide = 0;
    const totalSlides = gallerySlides.length;
    let autoSlideInterval = null;
    
    function updateSlideshow() {
        const translateX = -currentSlide * 100;
        galleryTrack.style.transform = `translateX(${translateX}%)`;
        
        // Update dots
        dots.forEach((dot, index) => {
            if (index === currentSlide) {
                dot.classList.remove('bg-white/50');
                dot.classList.add('bg-white');
            } else {
                dot.classList.remove('bg-white');
                dot.classList.add('bg-white/50');
            }
        });
    }
    
    function nextSlide() {
        currentSlide = (currentSlide + 1) % totalSlides;
        updateSlideshow();
        resetAutoSlide();
    }
    
    function prevSlide() {
        currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
        updateSlideshow();
        resetAutoSlide();
    }
    
    function goToSlide(index) {
        currentSlide = index;
        updateSlideshow();
        resetAutoSlide();
    }
    
    function startAutoSlide() {
        if (autoSlideInterval) clearInterval(autoSlideInterval);
        if (totalSlides > 1) {
            autoSlideInterval = setInterval(() => {
                nextSlide();
            }, 5000);
        }
    }
    
    function resetAutoSlide() {
        startAutoSlide();
    }
    
    // Navigation buttons
    if (nextBtn) nextBtn.addEventListener('click', nextSlide);
    if (prevBtn) prevBtn.addEventListener('click', prevSlide);
    
    // Dots navigation
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => goToSlide(index));
    });
    
    // Image click to zoom
    document.querySelectorAll('[data-image-url]').forEach(slide => {
        slide.addEventListener('click', function(e) {
            e.stopPropagation();
            const imageUrl = this.dataset.imageUrl;
            const imageTitle = this.dataset.imageTitle || 'Gambar Sejarah';
            
            // Create lightbox modal with zoom
            const lightbox = document.createElement('div');
            lightbox.className = 'fixed inset-0 bg-black/95 z-[100] flex items-center justify-center p-4';
            lightbox.style.cursor = 'zoom-out';
            lightbox.innerHTML = `
                <div class="relative max-w-7xl w-full h-full flex items-center justify-center">
                    <img src="${imageUrl}" alt="${imageTitle}" class="max-w-full max-h-full object-contain rounded-lg shadow-2xl cursor-zoom-out" style="transform: scale(1); transition: transform 0.3s ease;">
                    <button class="absolute top-4 right-4 text-white hover:text-gray-300 text-3xl md:text-4xl bg-black/50 rounded-full p-2 md:p-3 hover:bg-black/70 transition-colors" onclick="this.closest('.fixed').remove(); document.body.style.overflow = '';">
                        <i class="fas fa-times"></i>
                    </button>
                    <div class="absolute bottom-4 left-1/2 -translate-x-1/2 text-white bg-black/50 px-4 py-2 rounded-lg text-sm md:text-base">
                        ${imageTitle}
                    </div>
                </div>
            `;
            document.body.appendChild(lightbox);
            document.body.style.overflow = 'hidden';
            
            // Zoom functionality
            const img = lightbox.querySelector('img');
            let isZoomed = false;
            
            img.addEventListener('click', function(e) {
                e.stopPropagation();
                if (!isZoomed) {
                    this.style.transform = 'scale(2)';
                    this.style.cursor = 'zoom-out';
                    isZoomed = true;
                } else {
                    this.style.transform = 'scale(1)';
                    this.style.cursor = 'zoom-in';
                    isZoomed = false;
                }
            });
            
            // Close on background click
            lightbox.addEventListener('click', function(e) {
                if (e.target === this) {
                    this.remove();
                    document.body.style.overflow = '';
                }
            });
            
            // Close on Escape key
            const handleEscape = (e) => {
                if (e.key === 'Escape') {
                    lightbox.remove();
                    document.body.style.overflow = '';
                    document.removeEventListener('keydown', handleEscape);
                }
            };
            document.addEventListener('keydown', handleEscape);
        });
    });
    
    // Pause auto-slide on hover
    const slideshowContainer = galleryTrack.closest('.sejarah-gallery-slideshow');
    if (slideshowContainer) {
        slideshowContainer.addEventListener('mouseenter', () => {
            if (autoSlideInterval) clearInterval(autoSlideInterval);
        });
        slideshowContainer.addEventListener('mouseleave', () => {
            startAutoSlide();
        });
    }
    
    // Initialize
    updateSlideshow();
    startAutoSlide();
});

