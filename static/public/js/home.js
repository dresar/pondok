// Tab functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tab buttons
    document.querySelectorAll('.tab-button').forEach(button => {
        button.addEventListener('click', function() {
            const tabName = this.dataset.tab;
            if (!tabName) return; // Skip if no tab name
            
            // Find the closest container - prefer section, then parent with max-w-* class
            let tabContainer = this.closest('.section');
            if (!tabContainer) {
                tabContainer = this.closest('.max-w-6xl') || this.closest('.max-w-7xl') || this.closest('.max-w-5xl') || this.closest('.max-w-4xl');
            }
            if (!tabContainer) {
                tabContainer = this.parentElement.parentElement; // Fallback to parent container
            }
            
            // Remove active class from all buttons in the same container
            if (tabContainer) {
                tabContainer.querySelectorAll('.tab-button').forEach(btn => {
                    btn.classList.remove('active', 'border-b-4', 'border-green-500', 'text-green-600');
                    btn.classList.add('text-gray-600');
                });
            }
            
            // Add active class to clicked button
            this.classList.add('active', 'border-b-4', 'border-green-500', 'text-green-600');
            this.classList.remove('text-gray-600');
            
            // Hide all tab contents in the same container
            if (tabContainer) {
                tabContainer.querySelectorAll('.tab-content').forEach(content => {
                    content.classList.add('hidden');
                    // Also add opacity/transform classes if they exist
                    content.classList.add('opacity-0', 'translate-y-4');
                });
            }
            
            // Show selected tab content
            // Try with and without 'tab-' prefix for compatibility
            const targetContent = document.getElementById(`tab-${tabName}`) || document.getElementById(tabName);
            if (targetContent) {
                // Remove hidden and any animation classes
                targetContent.classList.remove('hidden', 'opacity-0', 'translate-y-4');
                // Ensure it's visible
                targetContent.style.display = '';
                targetContent.style.opacity = '';
                targetContent.style.transform = '';
            } else {
                console.warn(`Tab content not found for: ${tabName}`, `Looking for: tab-${tabName} or ${tabName}`);
            }
    });
  });
    
    // Ensure initial tab is visible (for jadwal section)
    const jadwalSection = document.getElementById('jadwal');
    if (jadwalSection) {
        const initialTab = jadwalSection.querySelector('#tab-santri');
        if (initialTab && !initialTab.classList.contains('hidden')) {
            // Tab is already visible, good
        } else if (initialTab) {
            // Make sure initial tab is visible
            initialTab.classList.remove('hidden');
        }
    }
});

// Facility image modal - handled in home.html inline script

// FAQ Accordion
document.querySelectorAll('.faq-question').forEach(question => {
    question.addEventListener('click', function() {
        const answer = this.nextElementSibling;
        const toggle = this.querySelector('.faq-toggle i');
        const isHidden = answer.classList.contains('hidden');
        
        // Close all other FAQs
        document.querySelectorAll('.faq-answer').forEach(ans => {
            if (ans !== answer) {
                ans.classList.add('hidden');
            }
        });
        document.querySelectorAll('.faq-toggle i').forEach(icon => {
            if (icon !== toggle) {
                icon.classList.remove('fa-minus');
                icon.classList.add('fa-plus');
            }
        });
        
        // Toggle current FAQ
        if (isHidden) {
            answer.classList.remove('hidden');
            toggle.classList.remove('fa-plus');
            toggle.classList.add('fa-minus');
        } else {
            answer.classList.add('hidden');
            toggle.classList.remove('fa-minus');
            toggle.classList.add('fa-plus');
        }
    });
  });

  // Hero Slideshow
let currentSlide = 0;
let slideInterval = null;
const slides = document.querySelectorAll('.hero-slide');
const totalSlides = slides.length;
const heroTitle = document.getElementById('hero-title-text');
const heroSubtitle = document.getElementById('hero-subtitle-text');

function updateHeroText(slideIndex) {
    const activeSlide = slides[slideIndex];
    if (activeSlide) {
        const title = activeSlide.dataset.title || 'Pendaftaran Santri Baru';
        const subtitle = activeSlide.dataset.subtitle || '2025/2026';
        
        if (heroTitle) heroTitle.textContent = title;
        if (heroSubtitle) heroSubtitle.textContent = subtitle;
    }
}
  
  function showSlide(index) {
    slides.forEach((slide, i) => {
        slide.classList.remove('active');
        if (i === index) {
            slide.classList.add('active');
        }
    });
    
    // Update pagination dots
    const dots = document.querySelectorAll('.hero-dot');
    dots.forEach((dot, i) => {
      if (i === index) {
            dot.classList.remove('bg-white/50');
            dot.classList.add('bg-white');
      } else {
            dot.classList.remove('bg-white');
            dot.classList.add('bg-white/50');
        }
    });
    
    // Update hero text
    updateHeroText(index);
  }
  
  function nextSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    showSlide(currentSlide);
    resetAutoSlide();
}

function prevSlide() {
    currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
    showSlide(currentSlide);
    resetAutoSlide();
}

function goToSlide(index) {
    currentSlide = index;
    showSlide(currentSlide);
    resetAutoSlide();
}

function resetAutoSlide() {
    if (slideInterval) {
        clearInterval(slideInterval);
    }
    if (slides.length > 1) {
      slideInterval = setInterval(nextSlide, 5000);
    }
  }
  
// Initialize slideshow
if (slides.length > 0) {
    showSlide(0);
    resetAutoSlide();
    
    // Pagination dots
    const dots = document.querySelectorAll('.hero-dot');
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => goToSlide(index));
    });
}

  // Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
      if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in-visible');
        }
    });
}, observerOptions);

document.querySelectorAll('.fade-in').forEach(el => {
    observer.observe(el);
});

// Back to top button functionality
const backToTopBtn = document.getElementById('backToTop');
if (backToTopBtn) {
    window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
            backToTopBtn.classList.remove('opacity-0');
            backToTopBtn.style.opacity = '1';
    } else {
            backToTopBtn.style.opacity = '0';
        }
    });
    
    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// WhatsApp button functionality
const whatsappBtn = document.getElementById('whatsappBtn');
if (whatsappBtn) {
    whatsappBtn.addEventListener('click', function() {
        const contactNumber = this.dataset.contactNumber || '';
    if (contactNumber) {
            const message = encodeURIComponent('Halo, saya ingin bertanya tentang pendaftaran santri baru.');
            window.open(`https://wa.me/${contactNumber}?text=${message}`, '_blank');
    } else {
            alert('Contact person belum tersedia. Silakan hubungi melalui informasi yang tersedia di halaman.');
        }
    });
}

// Form validation helper
function validateForm(formElement) {
    const inputs = formElement.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('border-red-500');
        } else {
            input.classList.remove('border-red-500');
        }
    });
    
    return isValid;
}

// Lazy loading images
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        if (img.dataset.src) {
          img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
        }
      }
    });
  });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// Mobile menu toggle (if exists)
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const mobileMenu = document.getElementById('mobile-menu');
if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
    });
}

// Print functionality
function printPage() {
    window.print();
}

// Share functionality
function sharePage() {
    if (navigator.share) {
        const pageTitle = document.title || 'Pendaftaran Santri Baru';
        navigator.share({
            title: pageTitle,
            text: 'Pendaftaran Santri Baru - Pesantren',
            url: window.location.href
        });
    } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(window.location.href);
        alert('Link berhasil disalin ke clipboard!');
    }
}

// Initialize tooltips (if using a tooltip library)
document.querySelectorAll('[data-tooltip]').forEach(element => {
    element.addEventListener('mouseenter', function() {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
    tooltip.textContent = this.dataset.tooltip;
    document.body.appendChild(tooltip);
        
    const rect = this.getBoundingClientRect();
        tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
        tooltip.style.left = (rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2)) + 'px';
        
    this.tooltipElement = tooltip;
  });
    
    element.addEventListener('mouseleave', function() {
    if (this.tooltipElement) {
      this.tooltipElement.remove();
      this.tooltipElement = null;
    }
  });
});

// Performance monitoring
if ('performance' in window) {
    window.addEventListener('load', () => {
        const perfData = window.performance.timing;
        const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
        console.log('Page Load Time:', pageLoadTime, 'ms');
    });
}

// Error handling for images
document.querySelectorAll('img').forEach(img => {
    img.addEventListener('error', function() {
        this.style.display = 'none';
        this.alt = 'Image not available';
  });
});

// Keyboard navigation - Unified handler for all modals
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        // Close all modals in order of priority
    const modals = [
            { id: 'program-gallery-modal', closeFn: closeProgramGallery },
            { id: 'fasilitas-modal', closeFn: closeFasilitasModal },
            { id: 'prestasi-modal', closeFn: closePrestasiModal },
            { id: 'pengumuman-modal', closeFn: closePengumumanModal },
            { id: 'pengajar-modal', closeFn: closePengajarModal },
            { id: 'program-kegiatan-modal', closeFn: closeProgramKegiatanModal },
            { id: 'gallery-lightbox-modal', closeFn: closeGalleryLightbox },
            { id: 'gallery-video-modal', closeFn: closeGalleryVideoModal },
            { id: 'ekstrakurikuler-modal', closeFn: closeEkstrakurikulerModal },
            { id: 'dokumentasi-modal', closeFn: closeDokumentasiModal }
        ];
        
        // Find first open modal and close it
    for (const modal of modals) {
            const element = document.getElementById(modal.id);
            if (element && !element.classList.contains('hidden')) {
        modal.closeFn();
                break; // Only close the topmost modal
            }
        }
    }
    
    // Arrow key navigation for gallery modals
    if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
        const direction = e.key === 'ArrowLeft' ? -1 : 1;
        
        // Program gallery modal
    const programModal = document.getElementById('program-gallery-modal');
    if (programModal && !programModal.classList.contains('hidden')) {
      changeProgramImage(direction);
      return;
    }
        
        // Ekstrakurikuler modal
        const ekstraModal = document.getElementById('ekstrakurikuler-modal');
        if (ekstraModal && !ekstraModal.classList.contains('hidden')) {
      changeEkstrakurikulerImage(direction);
      return;
    }
        
        // Dokumentasi modal
        const docModal = document.getElementById('dokumentasi-modal');
        if (docModal && !docModal.classList.contains('hidden')) {
      changeDokumentasiImage(direction);
      return;
    }
  }
});

// Prevent form resubmission on refresh
if (window.history.replaceState) {
  window.history.replaceState(null, null, window.location.href);
}

// Counter animation for statistics
function animateCounter(element, target, duration = 2000) {
    let start = 0;
  const increment = target / (duration / 16);
    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = target + (element.textContent.includes('+') ? '+' : '') + (element.textContent.includes('%') ? '%' : '');
            clearInterval(timer);
    } else {
            element.textContent = Math.floor(start) + (element.textContent.includes('+') ? '+' : '') + (element.textContent.includes('%') ? '%' : '');
    }
  }, 16);
}

// Observe statistics section for counter animation
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const statNumbers = entry.target.querySelectorAll('.stat-number');
            statNumbers.forEach(stat => {
                const text = stat.textContent;
                const number = parseInt(text.replace(/\D/g, ''));
                if (number && !stat.dataset.animated) {
                    stat.dataset.animated = 'true';
                    animateCounter(stat, number, 2000);
                }
            });
        }
    });
}, { threshold: 0.5 });

const statsSection = document.getElementById('statistik');
if (statsSection) {
  statsObserver.observe(statsSection);
}

// Gallery lightbox functionality
document.querySelectorAll('.gallery-item').forEach(item => {
    item.addEventListener('click', function() {
        const imageUrl = this.querySelector('img')?.src || this.dataset.image;
        if (imageUrl) {
            // Create lightbox modal
            const lightbox = document.createElement('div');
            lightbox.className = 'fixed inset-0 bg-black/90 z-50 flex items-center justify-center p-4';
            lightbox.innerHTML = `
        <div class="relative max-w-4xl w-full">
                    <img src="${imageUrl}" alt="Gallery Image" class="w-full h-auto rounded-lg">
          <button class="absolute top-4 right-4 text-white hover:text-gray-300 text-2xl" onclick="this.closest('.fixed').remove()">
            <i class="fas fa-times"></i>
          </button>
        </div>
      `;
            document.body.appendChild(lightbox);
            lightbox.addEventListener('click', function(e) {
        if (e.target === this) {
          this.remove();
        }
      });
    }
  });
});

// Program Gallery Modal
let currentProgramImages = [];
let currentProgramImageIndex = 0;

function openProgramGalleryFromData(programId) {
    const scriptTag = document.querySelector(`script.program-images-data[data-program-id="${programId}"]`);
    if (!scriptTag) return;
    
    try {
        const images = JSON.parse(scriptTag.textContent);
        openProgramGallery(programId, images);
    } catch (e) {
        console.error('Error parsing images data:', e);
    }
}

function openProgramGallery(programId, images) {
    if (!images || images.length === 0) return;
    
    currentProgramImages = images;
    currentProgramImageIndex = 0;
    
    const modal = document.getElementById('program-gallery-modal');
    const mainImg = document.getElementById('program-gallery-main-img');
    const thumbnails = document.getElementById('program-gallery-thumbnails');
    const counter = document.getElementById('program-gallery-counter');
    const prevBtn = document.getElementById('program-gallery-prev');
    const nextBtn = document.getElementById('program-gallery-next');
    
    // Set main image
    mainImg.src = images[0].url;
    mainImg.alt = images[0].alt;
    
    // Create thumbnails
    thumbnails.innerHTML = '';
    images.forEach((img, index) => {
        const btn = document.createElement('button');
        btn.className = `flex-shrink-0 ${index === 0 ? 'ring-2 ring-white' : 'opacity-50'}`;
      btn.onclick = () => changeProgramImage(index - currentProgramImageIndex);
        const thumbImg = document.createElement('img');
      thumbImg.src = img.url;
      thumbImg.alt = img.alt;
        thumbImg.className = 'w-16 h-16 object-cover rounded-lg';
      btn.appendChild(thumbImg);
      thumbnails.appendChild(btn);
    });
    
    // Update counter
    counter.textContent = `${currentProgramImageIndex + 1} / ${images.length}`;
    
    // Show/hide navigation buttons
    prevBtn.classList.toggle('hidden', images.length <= 1 || currentProgramImageIndex === 0);
    nextBtn.classList.toggle('hidden', images.length <= 1 || currentProgramImageIndex === images.length - 1);
    
    // Show modal
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeProgramGallery() {
    const modal = document.getElementById('program-gallery-modal');
    modal.classList.add('hidden');
    document.body.style.overflow = '';
    currentProgramImages = [];
  currentProgramImageIndex = 0;
}

function changeProgramImage(direction) {
    if (currentProgramImages.length === 0) return;
    
    if (typeof direction === 'number') {
        // Direct index change
        currentProgramImageIndex = Math.max(0, Math.min(currentProgramImages.length - 1, currentProgramImageIndex + direction));
    } else {
        // Direction: -1 or 1
        currentProgramImageIndex = Math.max(0, Math.min(currentProgramImages.length - 1, currentProgramImageIndex + direction));
    }
    
    const mainImg = document.getElementById('program-gallery-main-img');
    const thumbnails = document.getElementById('program-gallery-thumbnails');
    const counter = document.getElementById('program-gallery-counter');
    const prevBtn = document.getElementById('program-gallery-prev');
    const nextBtn = document.getElementById('program-gallery-next');
    
    // Update main image
    mainImg.src = currentProgramImages[currentProgramImageIndex].url;
    mainImg.alt = currentProgramImages[currentProgramImageIndex].alt;
    
    // Update thumbnails active state
    Array.from(thumbnails.children).forEach((btn, index) => {
      if (index === currentProgramImageIndex) {
            btn.classList.add('ring-2', 'ring-white');
            btn.classList.remove('opacity-50');
      } else {
            btn.classList.remove('ring-2', 'ring-white');
            btn.classList.add('opacity-50');
        }
    });
    
    // Update counter
    counter.textContent = `${currentProgramImageIndex + 1} / ${currentProgramImages.length}`;
    
    // Show/hide navigation buttons
    prevBtn.classList.toggle('hidden', currentProgramImageIndex === 0);
    nextBtn.classList.toggle('hidden', currentProgramImageIndex === currentProgramImages.length - 1);
}

// Fasilitas Modal Functions
function openFasilitasModal(imageUrl, fasilitasName) {
    const modal = document.getElementById('fasilitas-modal');
    const modalImg = document.getElementById('fasilitas-modal-img');
    const modalTitle = document.getElementById('fasilitas-modal-title');
    
    if (modal && modalImg && modalTitle) {
        modalImg.src = imageUrl;
        modalImg.alt = fasilitasName;
        modalTitle.textContent = fasilitasName;
        
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }
}

function closeFasilitasModal() {
    const modal = document.getElementById('fasilitas-modal');
  if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
    }
}

function closeFasilitasNotification() {
    const notification = document.getElementById('fasilitas-notification');
    if (notification) {
        notification.style.display = 'none';
        localStorage.setItem('fasilitas_notification_closed', 'true');
    }
}

// Prestasi Modal Functions
function openPrestasiModal(id, judul, nilai, deskripsi, icon, warna) {
    const modal = document.getElementById('prestasi-modal');
    const modalTitle = document.getElementById('prestasi-modal-title');
    const modalValue = document.getElementById('prestasi-modal-value');
    const modalDesc = document.getElementById('prestasi-modal-desc');
    const modalIcon = document.getElementById('prestasi-modal-icon');
    const modalHeader = document.getElementById('prestasi-modal-header');
  
  if (!modal || !modalTitle || !modalValue) return;
  
    // Set content
    modalTitle.textContent = judul || 'Prestasi';
    modalValue.textContent = nilai || '-';
    modalDesc.textContent = deskripsi || 'Detail prestasi dan pencapaian pesantren';
    
    // Set icon
    if (modalIcon) {
        modalIcon.innerHTML = `<i class="${icon || 'fas fa-trophy'}"></i>`;
    }
    
    // Set header color based on warna
    const colorClasses = {
        'green': 'from-green-500 to-green-600',
        'blue': 'from-blue-500 to-blue-600',
        'purple': 'from-purple-500 to-purple-600',
        'orange': 'from-orange-500 to-orange-600',
        'red': 'from-red-500 to-red-600'
    };
    
    if (modalHeader) {
        modalHeader.className = `p-6 md:p-8 border-b border-gray-200 flex items-center justify-between bg-gradient-to-r ${colorClasses[warna] || 'from-green-500 to-blue-500'}`;
    }
    
    // Set value color
    const valueColorClasses = {
        'green': 'text-green-600',
        'blue': 'text-blue-600',
        'purple': 'text-purple-600',
        'orange': 'text-orange-600',
        'red': 'text-red-600'
    };
    modalValue.className = `text-5xl md:text-6xl font-bold mb-4 ${valueColorClasses[warna] || 'text-green-600'}`;
    
    // Show modal
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closePrestasiModal() {
    const modal = document.getElementById('prestasi-modal');
  if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
    }
}

// Pengumuman Modal Functions
function openPengumumanModal(id, judul, konten, tanggal, isPenting) {
    const modal = document.getElementById('pengumuman-modal');
    const modalTitle = document.getElementById('pengumuman-modal-title');
    const modalDate = document.getElementById('pengumuman-modal-date');
    const modalContent = document.getElementById('pengumuman-modal-content');
    const modalIcon = document.getElementById('pengumuman-modal-icon');
    const modalHeader = document.getElementById('pengumuman-modal-header');
  
  if (!modal || !modalTitle || !modalContent) return;
  
    // Set content
    modalTitle.textContent = judul || 'Pengumuman';
    modalDate.textContent = tanggal || '';
    
    // Set konten dengan format Summernote (HTML)
    // Konten sudah dalam format HTML dari Django (dengan |safe)
    if (konten) {
        // Trim whitespace dan langsung set sebagai HTML
        modalContent.innerHTML = konten.trim();
    } else {
        modalContent.innerHTML = 'Tidak ada konten';
    }
    
    // Set icon dan header color based on isPenting
  if (modalIcon) {
        modalIcon.innerHTML = `<i class="fas fa-${isPenting ? 'exclamation-triangle' : 'bullhorn'}"></i>`;
  }
  
  if (modalHeader) {
        modalHeader.className = `p-4 md:p-6 border-b border-gray-200 flex items-center justify-between bg-gradient-to-r ${isPenting ? 'from-red-500 to-red-600' : 'from-green-500 to-blue-500'}`;
  }
  
    // Show modal
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closePengumumanModal() {
    const modal = document.getElementById('pengumuman-modal');
  if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
  }
}

// Make functions globally available
window.openProgramGalleryFromData = openProgramGalleryFromData;
window.closeProgramGallery = closeProgramGallery;
window.changeProgramImage = changeProgramImage;
window.openFasilitasModal = openFasilitasModal;
window.closeFasilitasModal = closeFasilitasModal;
window.closeFasilitasNotification = closeFasilitasNotification;
window.openPrestasiModal = openPrestasiModal;
window.closePrestasiModal = closePrestasiModal;
window.openPengumumanModal = openPengumumanModal;
window.closePengumumanModal = closePengumumanModal;

// Testimoni carousel (if multiple testimonials)
const testimoniContainer = document.querySelector('#testimoni .grid');
if (testimoniContainer && testimoniContainer.children.length > 3) {
    let currentTestimoniIndex = 0;
    const testimoniItems = Array.from(testimoniContainer.children);
    const itemsPerView = window.innerWidth >= 1024 ? 3 : window.innerWidth >= 768 ? 2 : 1;
    
    function showTestimoni() {
        testimoniItems.forEach((item, index) => {
            if (index >= currentTestimoniIndex && index < currentTestimoniIndex + itemsPerView) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    }
    
    showTestimoni();
    
    // Auto-rotate testimonials
    setInterval(() => {
        currentTestimoniIndex = (currentTestimoniIndex + itemsPerView) % testimoniItems.length;
        showTestimoni();
    }, 5000);
}

// Form submission handler
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        if (!validateForm(this)) {
            e.preventDefault();
            alert('Mohon lengkapi semua field yang wajib diisi.');
        }
  });
});

// Search functionality (if search bar exists)
const searchInput = document.getElementById('search-input');
if (searchInput) {
    searchInput.addEventListener('input', function() {
        const query = this.value.toLowerCase();
        const searchableElements = document.querySelectorAll('[data-searchable]');
        
        searchableElements.forEach(element => {
            const text = element.textContent.toLowerCase();
            if (text.includes(query)) {
                element.style.display = '';
            } else {
                element.style.display = 'none';
            }
        });
    });
}

// Print page functionality
window.printPage = printPage;

// Share page functionality
window.sharePage = sharePage;

// Loading screen (if exists)
window.addEventListener('load', () => {
    const loader = document.getElementById('page-loader');
    if (loader) {
        loader.style.opacity = '0';
      setTimeout(() => {
            loader.style.display = 'none';
        }, 300);
    }
});

// Scroll progress indicator
const scrollProgress = document.createElement('div');
scrollProgress.className = 'fixed top-0 left-0 h-1 bg-green-600 z-50 transition-all duration-300';
scrollProgress.style.width = '0%';
document.body.appendChild(scrollProgress);

window.addEventListener('scroll', () => {
    const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (window.pageYOffset / windowHeight) * 100;
    scrollProgress.style.width = scrolled + '%';
});

// Parallax effect for hero section
const heroSection = document.querySelector('.hero-section');
if (heroSection) {
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const heroContent = heroSection.querySelector('.hero-content');
        if (heroContent && scrolled < heroSection.offsetHeight) {
            heroContent.style.transform = `translateY(${scrolled * 0.5}px)`;
            heroContent.style.opacity = 1 - (scrolled / heroSection.offsetHeight);
        }
    });
}

// Mobile menu toggle enhancement
const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', () => {
        const menu = document.getElementById('mobile-menu');
        if (menu) {
            menu.classList.toggle('hidden');
            menu.classList.toggle('flex');
        }
    });
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
        type === 'success' ? 'bg-green-500' : 
        type === 'error' ? 'bg-red-500' : 
        type === 'warning' ? 'bg-yellow-500' : 
        'bg-blue-500'
    } text-white`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
            setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Copy to clipboard functionality
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Berhasil disalin ke clipboard!', 'success');
    }).catch(() => {
        showNotification('Gagal menyalin ke clipboard', 'error');
    });
}

// Initialize all interactive elements
document.addEventListener('DOMContentLoaded', () => {
    // Add loading states to buttons
    document.querySelectorAll('button[type="submit"], a.cta-button').forEach(button => {
        button.addEventListener('click', function() {
            if (this.type === 'submit' || this.classList.contains('cta-button')) {
                this.classList.add('opacity-75', 'cursor-not-allowed');
                setTimeout(() => {
                    this.classList.remove('opacity-75', 'cursor-not-allowed');
                }, 2000);
            }
        });
    });
    
    // Add hover effects to cards
    document.querySelectorAll('.card, .info-card, .testimoni-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
      });
    });
    
    // Initialize tooltips
    document.querySelectorAll('[data-tooltip]').forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'absolute bg-gray-900 text-white text-xs rounded px-2 py-1 z-50';
            tooltip.textContent = this.dataset.tooltip;
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
            tooltip.style.left = (rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2)) + 'px';
            
            this.tooltipElement = tooltip;
        });
        
        element.addEventListener('mouseleave', function() {
            if (this.tooltipElement) {
                this.tooltipElement.remove();
                this.tooltipElement = null;
            }
        });
    });
});

// Analytics tracking (placeholder)
function trackEvent(category, action, label) {
    if (typeof gtag !== 'undefined') {
        gtag('event', action, {
            'event_category': category,
            'event_label': label
        });
    }
    console.log('Event tracked:', category, action, label);
}

// Track CTA clicks
document.querySelectorAll('a[href*="register"], a.cta-button').forEach(link => {
    link.addEventListener('click', function() {
        trackEvent('CTA', 'Click', this.textContent.trim());
    });
});

// Track section views
const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            trackEvent('Section', 'View', entry.target.id || 'Unknown');
        }
    });
}, { threshold: 0.5 });

document.querySelectorAll('section[id]').forEach(section => {
    sectionObserver.observe(section);
});

// Program gallery button event listeners
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.program-gallery-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const programId = this.getAttribute('data-program-id');
        if (programId) {
          openProgramGalleryFromData(parseInt(programId));
        }
      });
    });
    
    // Fasilitas notification
    const notification = document.getElementById('fasilitas-notification');
    if (notification) {
        const isClosed = localStorage.getItem('fasilitas_notification_closed');
        if (isClosed === 'true') {
            notification.style.display = 'none';
        }
        
        // Show notification when user scrolls to fasilitas section
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting && isClosed !== 'true') {
                    notification.style.display = 'block';
                }
            });
        }, { threshold: 0.1 });
        
        const fasilitasSection = document.getElementById('fasilitas');
        if (fasilitasSection) {
            observer.observe(fasilitasSection);
        }
    }
    
    // Prestasi card click handlers
    document.querySelectorAll('.prestasi-card').forEach(card => {
        card.addEventListener('click', function() {
            const id = this.getAttribute('data-stat-id');
            const judul = this.getAttribute('data-stat-judul');
            const nilai = this.getAttribute('data-stat-nilai');
            const deskripsi = this.getAttribute('data-stat-deskripsi');
            const icon = this.getAttribute('data-stat-icon');
            const warna = this.getAttribute('data-stat-warna');
            
            openPrestasiModal(id, judul, nilai, deskripsi, icon, warna);
      });
    });
    
    // Pengumuman detail button click handlers
    document.querySelectorAll('.pengumuman-detail-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            const id = this.getAttribute('data-pengumuman-id');
            const judul = this.getAttribute('data-pengumuman-judul');
            const tanggal = this.getAttribute('data-pengumuman-tanggal');
            const isPenting = this.getAttribute('data-pengumuman-is-penting') === 'true';
            
            // Get konten from script tag
            const scriptTag = document.querySelector(`script.pengumuman-konten-data[data-pengumuman-id="${id}"]`);
            let konten = '';
            if (scriptTag) {
                // Get HTML content directly (already safe from Django)
                konten = scriptTag.textContent.trim();
                // Remove any leading/trailing whitespace or newlines
                konten = konten.replace(/^\s+|\s+$/g, '');
            }
            
            openPengumumanModal(id, judul, konten, tanggal, isPenting);
      });
    });
  });

// Gallery Lightbox Functions
function openGalleryLightbox(imageUrl, title) {
    const modal = document.getElementById('gallery-lightbox-modal');
    const modalImg = document.getElementById('gallery-lightbox-img');
    const modalTitle = document.getElementById('gallery-lightbox-title');
    
    if (modal && modalImg && modalTitle) {
        modalImg.src = imageUrl;
        modalImg.alt = title;
        modalTitle.textContent = title;
        
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }
}

function closeGalleryLightbox() {
    const modal = document.getElementById('gallery-lightbox-modal');
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
    }
}

// Gallery Video Modal Functions
let currentGalleryVideoElement = null;

function openVideoModalFromGallery(element) {
    const videoUrl = element.getAttribute('data-video-url');
    if (!videoUrl || videoUrl.trim() === '') {
        alert('Video tidak tersedia');
        return;
    }
    
    console.log('Opening video:', videoUrl);
    
    const modal = document.getElementById('gallery-video-modal');
    const modalContent = document.getElementById('gallery-video-modal-content');
    
    if (!modal || !modalContent) {
        console.error('Modal elements not found');
        return;
    }
    
    // Stop and remove previous video if exists
    if (currentGalleryVideoElement) {
        try {
            currentGalleryVideoElement.pause();
            currentGalleryVideoElement.src = '';
            currentGalleryVideoElement.load();
        } catch (e) {
            console.error('Error stopping previous video:', e);
        }
        currentGalleryVideoElement = null;
    }
    
    // Clear content
    modalContent.innerHTML = '';
    
    // Show modal first
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    
    // Detect video type from URL
    const videoExtension = videoUrl.split('.').pop().toLowerCase();
    let videoType = 'video/mp4'; // default
    
    if (videoExtension === 'webm') {
        videoType = 'video/webm';
    } else if (videoExtension === 'ogg' || videoExtension === 'ogv') {
        videoType = 'video/ogg';
    } else if (videoExtension === 'mov') {
        videoType = 'video/quicktime';
    } else if (videoExtension === 'avi') {
        videoType = 'video/x-msvideo';
    }
    
    // Video file dengan HTML5 Video Player Native
    modalContent.innerHTML = `<video id="gallery-video-player" class="w-full h-full" controls playsinline preload="metadata">
        <source src="${videoUrl}" type="${videoType}">
        Browser Anda tidak mendukung pemutaran video HTML5. Silakan gunakan browser yang lebih baru.
    </video>`;
    
    // Get video element
    currentGalleryVideoElement = document.getElementById('gallery-video-player');
    
    if (!currentGalleryVideoElement) {
        console.error('Video element not created');
        return;
    }
    
    // Handle video events
    currentGalleryVideoElement.addEventListener('loadstart', function() {
        console.log('Video load started');
    });
    
    currentGalleryVideoElement.addEventListener('loadedmetadata', function() {
        console.log('Video metadata loaded successfully');
        // Try to play after metadata is loaded
        this.play().catch(function(error) {
            console.log('Autoplay prevented:', error);
            // This is normal, user interaction may be required
        });
    });
    
    currentGalleryVideoElement.addEventListener('loadeddata', function() {
        console.log('Video data loaded');
    });
    
    currentGalleryVideoElement.addEventListener('canplay', function() {
        console.log('Video can start playing');
    });
    
    currentGalleryVideoElement.addEventListener('error', function(e) {
        console.error('Video error details:', {
            error: e,
            errorCode: this.error,
            networkState: this.networkState,
            readyState: this.readyState,
            src: this.src
        });
        
        let errorMessage = 'Terjadi kesalahan saat memutar video.';
        
        if (this.error) {
            switch(this.error.code) {
              case MediaError.MEDIA_ERR_ABORTED:
                    errorMessage = 'Pemutaran video dibatalkan.';
                break;
              case MediaError.MEDIA_ERR_NETWORK:
                    errorMessage = 'Kesalahan jaringan saat memuat video.';
                break;
              case MediaError.MEDIA_ERR_DECODE:
                    errorMessage = 'Video tidak dapat didecode. Format mungkin tidak didukung.';
                break;
              case MediaError.MEDIA_ERR_SRC_NOT_SUPPORTED:
                    errorMessage = 'Format video tidak didukung oleh browser.';
                break;
              default:
                    errorMessage = 'Terjadi kesalahan saat memutar video. Pastikan file video valid dan format didukung.';
            }
        }
        
        // Show error message in modal instead of alert
        modalContent.innerHTML = `
            <div class="flex flex-col items-center justify-center h-full text-white p-8">
                <i class="fas fa-exclamation-triangle text-4xl mb-4 text-yellow-400"></i>
                <p class="text-lg font-semibold mb-2">${errorMessage}</p>
                <p class="text-sm text-gray-300 mb-4">URL: ${videoUrl}</p>
                <button onclick="closeGalleryVideoModal()" class="px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg transition-colors">
                    Tutup
                </button>
            </div>
        `;
    });
    
    // Try to load the video
    try {
        currentGalleryVideoElement.load();
    } catch (e) {
        console.error('Error loading video:', e);
    }
}

function closeGalleryVideoModal() {
    // Stop video before closing
    if (currentGalleryVideoElement) {
        try {
            currentGalleryVideoElement.pause();
            currentGalleryVideoElement.src = '';
            currentGalleryVideoElement.load();
        } catch (e) {
            console.error('Error stopping video:', e);
        }
        currentGalleryVideoElement = null;
    }
    
    const modal = document.getElementById('gallery-video-modal');
    const modalContent = document.getElementById('gallery-video-modal-content');
    modal.classList.add('hidden');
    modalContent.innerHTML = '';
    document.body.style.overflow = '';
}

// Ekstrakurikuler Modal Functions
let currentEkstrakurikulerImages = [];
let currentEkstrakurikulerIndex = 0;
let currentEkstrakurikulerData = null;

function openEkstrakurikulerModal(ekstraId) {
    // Find the data for this ekstrakurikuler
    const dataElement = document.querySelector(`.ekstrakurikuler-images-data[data-ekstra-id="${ekstraId}"]`);
    if (!dataElement) {
        console.error('Data ekstrakurikuler tidak ditemukan');
        return;
    }
    
    try {
        currentEkstrakurikulerData = JSON.parse(dataElement.textContent);
        currentEkstrakurikulerImages = currentEkstrakurikulerData.images || [];
        
        if (currentEkstrakurikulerImages.length === 0) {
            alert('Tidak ada gambar untuk ekstrakurikuler ini');
            return;
        }
        
        currentEkstrakurikulerIndex = 0;
        updateEkstrakurikulerModal();
        
        const modal = document.getElementById('ekstrakurikuler-modal');
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    } catch (e) {
        console.error('Error parsing ekstrakurikuler data:', e);
    }
}

function closeEkstrakurikulerModal() {
    const modal = document.getElementById('ekstrakurikuler-modal');
    modal.classList.add('hidden');
    document.body.style.overflow = '';
    currentEkstrakurikulerImages = [];
    currentEkstrakurikulerIndex = 0;
    currentEkstrakurikulerData = null;
}

function changeEkstrakurikulerImage(direction) {
    if (currentEkstrakurikulerImages.length === 0) return;
    
    currentEkstrakurikulerIndex += direction;
    
    if (currentEkstrakurikulerIndex < 0) {
        currentEkstrakurikulerIndex = currentEkstrakurikulerImages.length - 1;
    } else if (currentEkstrakurikulerIndex >= currentEkstrakurikulerImages.length) {
        currentEkstrakurikulerIndex = 0;
    }
    
    updateEkstrakurikulerModal();
}

function updateEkstrakurikulerModal() {
    if (currentEkstrakurikulerImages.length === 0) return;
    
    const currentImage = currentEkstrakurikulerImages[currentEkstrakurikulerIndex];
    const modal = document.getElementById('ekstrakurikuler-modal');
    const mainImg = document.getElementById('ekstrakurikuler-modal-main-img');
    const title = document.getElementById('ekstrakurikuler-modal-title');
    const counter = document.getElementById('ekstrakurikuler-modal-counter');
    const prevBtn = document.getElementById('ekstrakurikuler-modal-prev');
    const nextBtn = document.getElementById('ekstrakurikuler-modal-next');
    const thumbnails = document.getElementById('ekstrakurikuler-modal-thumbnails');
    
    if (mainImg) mainImg.src = currentImage.url;
    if (mainImg) mainImg.alt = currentImage.alt;
    if (title && currentEkstrakurikulerData) title.textContent = currentEkstrakurikulerData.nama;
    if (counter) counter.textContent = `${currentEkstrakurikulerIndex + 1} / ${currentEkstrakurikulerImages.length}`;
    
    // Show/hide navigation buttons
    if (prevBtn) {
        if (currentEkstrakurikulerImages.length > 1) {
            prevBtn.classList.remove('hidden');
        } else {
            prevBtn.classList.add('hidden');
        }
    }
    if (nextBtn) {
        if (currentEkstrakurikulerImages.length > 1) {
            nextBtn.classList.remove('hidden');
        } else {
            nextBtn.classList.add('hidden');
        }
    }
    
    // Update thumbnails
    if (thumbnails) {
        thumbnails.innerHTML = '';
        currentEkstrakurikulerImages.forEach((img, index) => {
            const thumbBtn = document.createElement('button');
            thumbBtn.className = `flex-shrink-0 ${index === currentEkstrakurikulerIndex ? 'ring-2 ring-green-500' : 'opacity-50'}`;
            thumbBtn.onclick = () => {
                currentEkstrakurikulerIndex = index;
                updateEkstrakurikulerModal();
            };
            const thumbImg = document.createElement('img');
            thumbImg.src = img.url;
            thumbImg.alt = img.alt;
            thumbImg.className = 'w-16 h-16 object-cover rounded-lg';
            thumbBtn.appendChild(thumbImg);
            thumbnails.appendChild(thumbBtn);
        });
    }
}

// Make gallery functions globally available
window.openGalleryLightbox = openGalleryLightbox;
window.closeGalleryLightbox = closeGalleryLightbox;
window.openVideoModalFromGallery = openVideoModalFromGallery;
window.closeGalleryVideoModal = closeGalleryVideoModal;
window.openEkstrakurikulerModal = openEkstrakurikulerModal;
window.closeEkstrakurikulerModal = closeEkstrakurikulerModal;
window.changeEkstrakurikulerImage = changeEkstrakurikulerImage;

// Dokumentasi Modal Functions
let currentDokumentasiImages = [];
let currentDokumentasiIndex = 0;
let currentDokumentasiData = null;

function openDokumentasiModal(docId) {
    // Find the data for this dokumentasi
    const dataElement = document.querySelector(`.dokumentasi-images-data[data-doc-id="${docId}"]`);
    if (!dataElement) {
        console.error('Data dokumentasi tidak ditemukan');
        return;
    }
    
    try {
        currentDokumentasiData = JSON.parse(dataElement.textContent);
        currentDokumentasiImages = currentDokumentasiData.images || [];
        
        if (currentDokumentasiImages.length === 0) {
            alert('Tidak ada gambar untuk dokumentasi ini');
            return;
        }
        
        currentDokumentasiIndex = 0;
        updateDokumentasiModal();
        
        const modal = document.getElementById('dokumentasi-modal');
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    } catch (e) {
        console.error('Error parsing dokumentasi data:', e);
    }
}

function closeDokumentasiModal() {
    const modal = document.getElementById('dokumentasi-modal');
    modal.classList.add('hidden');
    document.body.style.overflow = '';
    currentDokumentasiImages = [];
    currentDokumentasiIndex = 0;
    currentDokumentasiData = null;
}

function changeDokumentasiImage(direction) {
    if (currentDokumentasiImages.length === 0) return;
    
    currentDokumentasiIndex += direction;
    
    if (currentDokumentasiIndex < 0) {
        currentDokumentasiIndex = currentDokumentasiImages.length - 1;
    } else if (currentDokumentasiIndex >= currentDokumentasiImages.length) {
        currentDokumentasiIndex = 0;
    }
    
    updateDokumentasiModal();
}

function updateDokumentasiModal() {
    if (currentDokumentasiImages.length === 0) return;
    
    const currentImage = currentDokumentasiImages[currentDokumentasiIndex];
    const modal = document.getElementById('dokumentasi-modal');
    const mainImg = document.getElementById('dokumentasi-modal-main-img');
    const title = document.getElementById('dokumentasi-modal-title');
    const kategori = document.getElementById('dokumentasi-modal-kategori');
    const tanggal = document.getElementById('dokumentasi-modal-tanggal');
    const lokasi = document.getElementById('dokumentasi-modal-lokasi');
    const counter = document.getElementById('dokumentasi-modal-counter');
    const prevBtn = document.getElementById('dokumentasi-modal-prev');
    const nextBtn = document.getElementById('dokumentasi-modal-next');
    const thumbnails = document.getElementById('dokumentasi-modal-thumbnails');
    
    if (mainImg) mainImg.src = currentImage.url;
    if (mainImg) mainImg.alt = currentImage.alt;
    if (title && currentDokumentasiData) title.textContent = currentDokumentasiData.judul;
    if (kategori && currentDokumentasiData) kategori.innerHTML = `<i class="fas fa-tag mr-1"></i>${currentDokumentasiData.kategori || ''}`;
    if (tanggal && currentDokumentasiData && currentDokumentasiData.tanggal) tanggal.innerHTML = `<i class="fas fa-calendar-alt mr-1"></i>${currentDokumentasiData.tanggal}`;
    if (lokasi && currentDokumentasiData && currentDokumentasiData.lokasi) lokasi.innerHTML = `<i class="fas fa-map-marker-alt mr-1"></i>${currentDokumentasiData.lokasi}`;
    if (counter) counter.textContent = `${currentDokumentasiIndex + 1} / ${currentDokumentasiImages.length}`;
    
    // Show/hide navigation buttons
    if (prevBtn) {
        if (currentDokumentasiImages.length > 1) {
            prevBtn.classList.remove('hidden');
        } else {
            prevBtn.classList.add('hidden');
        }
    }
    if (nextBtn) {
        if (currentDokumentasiImages.length > 1) {
            nextBtn.classList.remove('hidden');
        } else {
            nextBtn.classList.add('hidden');
        }
    }
    
    // Update thumbnails
    if (thumbnails) {
        thumbnails.innerHTML = '';
        currentDokumentasiImages.forEach((img, index) => {
            const thumbBtn = document.createElement('button');
            thumbBtn.className = `flex-shrink-0 ${index === currentDokumentasiIndex ? 'ring-2 ring-green-500' : 'opacity-50'}`;
            thumbBtn.onclick = () => {
                currentDokumentasiIndex = index;
                updateDokumentasiModal();
            };
            const thumbImg = document.createElement('img');
            thumbImg.src = img.url;
            thumbImg.alt = img.alt;
            thumbImg.className = 'w-16 h-16 object-cover rounded-lg';
            thumbBtn.appendChild(thumbImg);
            thumbnails.appendChild(thumbBtn);
        });
    }
}

// Make dokumentasi functions globally available
window.openDokumentasiModal = openDokumentasiModal;
window.closeDokumentasiModal = closeDokumentasiModal;
window.changeDokumentasiImage = changeDokumentasiImage;


// ============================================
// PENGAJAR SLIDESHOW & MODAL
// ============================================

// Pengajar Slideshow (Mobile Only)
document.addEventListener('DOMContentLoaded', function() {
    const slideshow = document.querySelector('.pengajar-slideshow-track');
    const slides = document.querySelectorAll('.pengajar-slide');
    const dots = document.querySelectorAll('.pengajar-slideshow-dot');
    const prevBtn = document.querySelector('.pengajar-slideshow-prev');
    const nextBtn = document.querySelector('.pengajar-slideshow-next');
    
    if (!slideshow || slides.length === 0) return;
    
    let currentSlide = 0;
    let autoSlideInterval = null;
    
    function showSlide(index) {
        if (index < 0) index = slides.length - 1;
        if (index >= slides.length) index = 0;
        
        currentSlide = index;
        slideshow.style.transform = `translateX(-${currentSlide * 100}%)`;
        
        // Update dots
        dots.forEach((dot, i) => {
            if (i === currentSlide) {
                dot.classList.add('bg-white');
                dot.classList.remove('bg-white/50');
            } else {
                dot.classList.remove('bg-white');
                dot.classList.add('bg-white/50');
            }
        });
    }
    
    function startAutoSlide() {
        // Hanya auto-slide di mobile (lebar < 768px)
        if (window.innerWidth < 768) {
            if (autoSlideInterval) clearInterval(autoSlideInterval);
            autoSlideInterval = setInterval(() => {
                showSlide(currentSlide + 1);
            }, 5000);
        } else {
            if (autoSlideInterval) {
                clearInterval(autoSlideInterval);
                autoSlideInterval = null;
            }
        }
    }
    
    function stopAutoSlide() {
        if (autoSlideInterval) {
            clearInterval(autoSlideInterval);
            autoSlideInterval = null;
        }
    }
    
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            showSlide(currentSlide - 1);
            stopAutoSlide();
            startAutoSlide();
        });
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            showSlide(currentSlide + 1);
            stopAutoSlide();
            startAutoSlide();
        });
    }
    
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            showSlide(index);
            stopAutoSlide();
            startAutoSlide();
        });
    });
    
    // Start auto-slide on load
    startAutoSlide();
    
    // Restart auto-slide on window resize
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            stopAutoSlide();
            startAutoSlide();
        }, 250);
    });
    
    // Pause auto-slide on hover (mobile)
    if (slideshow) {
        slideshow.addEventListener('mouseenter', stopAutoSlide);
        slideshow.addEventListener('mouseleave', () => {
            if (window.innerWidth < 768) {
                startAutoSlide();
            }
        });
    }
});

// Pengajar Modal
let currentPengajarData = null;

function openPengajarModal(pengajarId) {
    const modal = document.getElementById('pengajar-modal');
    const content = document.getElementById('pengajar-modal-content');
    
    if (!modal || !content) return;
    
    // Show modal with loading
    modal.classList.remove('hidden');
    content.innerHTML = `
        <div class="text-center py-8">
            <i class="fas fa-spinner fa-spin text-4xl text-gray-400"></i>
            <p class="mt-4 text-gray-600">Memuat data...</p>
        </div>
    `;
    
    // Fetch data
    fetch(`/tenaga-pengajar/${pengajarId}/json/`)
        .then(response => response.json())
        .then(data => {
            currentPengajarData = data;
            renderPengajarModal(data);
        })
        .catch(error => {
            console.error('Error:', error);
            content.innerHTML = `
                <div class="text-center py-8">
                    <i class="fas fa-exclamation-circle text-4xl text-red-400"></i>
                    <p class="mt-4 text-red-600">Gagal memuat data pengajar</p>
                </div>
            `;
        });
}

function closePengajarModal(event) {
    // Prevent event bubbling
    if (event) {
        event.stopPropagation();
    }
    
    const modal = document.getElementById('pengajar-modal');
    if (modal) {
        modal.classList.add('hidden');
        // Reset scroll position
        const content = document.getElementById('pengajar-modal-content');
        if (content) {
            content.scrollTop = 0;
        }
    }
    currentPengajarData = null;
}

function renderPengajarModal(data) {
    const content = document.getElementById('pengajar-modal-content');
    if (!content) return;
    
    // Check if ada media sosial
    const hasSocialMedia = data.whatsapp || data.facebook || data.instagram || data.twitter || data.linkedin || data.youtube || data.tiktok;
    
    const html = `
        <!-- Header Card dengan Gradient -->
        <div class="relative bg-gradient-to-br from-green-500 to-blue-500 p-4 sm:p-5 md:p-6 lg:p-8 text-white sticky top-0 z-10">
            <div class="flex items-center justify-between mb-3 sm:mb-4">
                <div class="flex items-center gap-2 sm:gap-3 md:gap-4 flex-1 min-w-0">
                    ${data.foto ? `
                    <img src="${data.foto}" alt="${data.nama_lengkap}" class="w-16 h-16 sm:w-20 sm:h-20 md:w-24 md:h-24 rounded-full object-cover border-2 sm:border-4 border-white shadow-xl flex-shrink-0">
                    ` : `
                    <div class="w-16 h-16 sm:w-20 sm:h-20 md:w-24 md:h-24 rounded-full bg-white/20 backdrop-blur-sm border-2 sm:border-4 border-white shadow-xl flex items-center justify-center flex-shrink-0">
                        <i class="fas fa-user text-2xl sm:text-3xl md:text-4xl lg:text-5xl text-white"></i>
                    </div>
                    `}
                    <div class="flex-1 min-w-0">
                        <div class="mb-1.5 sm:mb-2 flex flex-wrap gap-1.5 sm:gap-2">
                            <span class="px-2 sm:px-3 py-0.5 sm:py-1 text-xs font-semibold rounded-full ${data.jenis_kelamin_short === 'Ustadz' ? 'bg-blue-600/80 text-white' : 'bg-pink-600/80 text-white'}">
                                ${data.jenis_kelamin_short}
                            </span>
                            ${data.bagian_jabatan ? `
                            <span class="px-2 sm:px-3 py-0.5 sm:py-1 text-xs font-semibold rounded-full bg-white/20 backdrop-blur-sm text-white">
                                ${data.bagian_jabatan}
                            </span>
                            ` : ''}
                        </div>
                        <h3 class="text-base sm:text-lg md:text-xl lg:text-2xl font-bold mb-1 line-clamp-2">${data.nama_lengkap}</h3>
                        ${data.nama_panggilan ? `<p class="text-sm md:text-base text-white/90">${data.nama_panggilan}</p>` : ''}
                    </div>
                </div>
                <button onclick="closePengajarModal()" class="bg-white/20 hover:bg-white/30 text-white p-2 rounded-full transition-colors shadow-lg flex-shrink-0 ml-4">
                    <i class="fas fa-times text-xl"></i>
                </button>
            </div>
            
            <!-- Media Sosial di Header (jika ada) -->
            ${hasSocialMedia ? `
            <div class="flex items-center gap-1.5 sm:gap-2 flex-wrap mt-2 sm:mt-3">
                ${data.whatsapp ? `
                <a href="https://wa.me/${data.whatsapp}" target="_blank" rel="noopener noreferrer" class="bg-white/20 hover:bg-white/30 backdrop-blur-sm text-white p-1.5 sm:p-2 rounded-lg transition-colors" title="WhatsApp">
                    <i class="fab fa-whatsapp text-sm sm:text-base"></i>
                </a>
                ` : ''}
                ${data.facebook ? `
                <a href="${data.facebook}" target="_blank" rel="noopener noreferrer" class="bg-white/20 hover:bg-white/30 backdrop-blur-sm text-white p-1.5 sm:p-2 rounded-lg transition-colors" title="Facebook">
                    <i class="fab fa-facebook-f text-sm sm:text-base"></i>
                </a>
                ` : ''}
                ${data.instagram ? `
                <a href="${data.instagram}" target="_blank" rel="noopener noreferrer" class="bg-white/20 hover:bg-white/30 backdrop-blur-sm text-white p-1.5 sm:p-2 rounded-lg transition-colors" title="Instagram">
                    <i class="fab fa-instagram text-sm sm:text-base"></i>
                </a>
                ` : ''}
                ${data.twitter ? `
                <a href="${data.twitter}" target="_blank" rel="noopener noreferrer" class="bg-white/20 hover:bg-white/30 backdrop-blur-sm text-white p-1.5 sm:p-2 rounded-lg transition-colors" title="Twitter/X">
                    <i class="fab fa-twitter text-sm sm:text-base"></i>
                </a>
                ` : ''}
                ${data.linkedin ? `
                <a href="${data.linkedin}" target="_blank" rel="noopener noreferrer" class="bg-white/20 hover:bg-white/30 backdrop-blur-sm text-white p-1.5 sm:p-2 rounded-lg transition-colors" title="LinkedIn">
                    <i class="fab fa-linkedin-in text-sm sm:text-base"></i>
                </a>
                ` : ''}
                ${data.youtube ? `
                <a href="${data.youtube}" target="_blank" rel="noopener noreferrer" class="bg-white/20 hover:bg-white/30 backdrop-blur-sm text-white p-1.5 sm:p-2 rounded-lg transition-colors" title="YouTube">
                    <i class="fab fa-youtube text-sm sm:text-base"></i>
                </a>
                ` : ''}
                ${data.tiktok ? `
                <a href="${data.tiktok}" target="_blank" rel="noopener noreferrer" class="bg-white/20 hover:bg-white/30 backdrop-blur-sm text-white p-1.5 sm:p-2 rounded-lg transition-colors" title="TikTok">
                    <i class="fab fa-tiktok text-sm sm:text-base"></i>
                </a>
                ` : ''}
            </div>
            ` : ''}
        </div>
        
        <!-- Content Card -->
        <div class="p-3 sm:p-4 md:p-6 bg-white">
            
            <!-- Biodata -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                ${data.tempat_lahir || data.tanggal_lahir ? `
                <div>
                    <label class="text-sm font-medium text-gray-500">Tempat & Tanggal Lahir</label>
                    <p class="text-gray-900">${data.tempat_lahir || ''}${data.tanggal_lahir ? (data.tempat_lahir ? ', ' : '') + data.tanggal_lahir : ''}</p>
                </div>
                ` : ''}
                ${data.alamat ? `
                <div>
                    <label class="text-sm font-medium text-gray-500">Alamat</label>
                    <p class="text-gray-900">${data.alamat}</p>
                </div>
                ` : ''}
                ${data.no_hp ? `
                <div>
                    <label class="text-sm font-medium text-gray-500">No. HP</label>
                    <p class="text-gray-900">${data.no_hp}</p>
                </div>
                ` : ''}
                ${data.email ? `
                <div>
                    <label class="text-sm font-medium text-gray-500">Email</label>
                    <p class="text-gray-900">${data.email}</p>
                </div>
                ` : ''}
            </div>
            
            <!-- Pendidikan -->
            ${data.pendidikan_terakhir || data.universitas || data.tahun_lulus ? `
            <div class="mb-6 pb-6 border-b border-gray-200">
                <h4 class="text-lg font-semibold text-gray-900 mb-3">Pendidikan</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    ${data.pendidikan_terakhir ? `
                    <div>
                        <label class="text-sm font-medium text-gray-500">Pendidikan Terakhir</label>
                        <p class="text-gray-900">${data.pendidikan_terakhir}</p>
                    </div>
                    ` : ''}
                    ${data.universitas ? `
                    <div>
                        <label class="text-sm font-medium text-gray-500">Universitas/Institusi</label>
                        <p class="text-gray-900">${data.universitas}</p>
                    </div>
                    ` : ''}
                    ${data.tahun_lulus ? `
                    <div>
                        <label class="text-sm font-medium text-gray-500">Tahun Lulus</label>
                        <p class="text-gray-900">${data.tahun_lulus}</p>
                    </div>
                    ` : ''}
                    ${data.riwayat_pendidikan ? `
                    <div class="md:col-span-2">
                        <label class="text-sm font-medium text-gray-500">Riwayat Pendidikan</label>
                        <p class="text-gray-900 whitespace-pre-line">${data.riwayat_pendidikan}</p>
                    </div>
                    ` : ''}
                </div>
            </div>
            ` : ''}
            
            <!-- Keahlian -->
            ${data.bidang_keahlian || data.mata_pelajaran ? `
            <div class="mb-6 pb-6 border-b border-gray-200">
                <h4 class="text-lg font-semibold text-gray-900 mb-3">Keahlian & Bidang</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    ${data.bidang_keahlian ? `
                    <div>
                        <label class="text-sm font-medium text-gray-500">Bidang Keahlian</label>
                        <p class="text-gray-900">${data.bidang_keahlian}</p>
                    </div>
                    ` : ''}
                    ${data.mata_pelajaran ? `
                    <div>
                        <label class="text-sm font-medium text-gray-500">Mata Pelajaran yang Diampu</label>
                        <p class="text-gray-900">${data.mata_pelajaran}</p>
                    </div>
                    ` : ''}
                </div>
            </div>
            ` : ''}
            
            <!-- Pengalaman & Prestasi -->
            ${data.pengalaman_mengajar || data.prestasi ? `
            <div class="mb-6 pb-6 border-b border-gray-200">
                <h4 class="text-lg font-semibold text-gray-900 mb-3">Pengalaman & Prestasi</h4>
                ${data.pengalaman_mengajar ? `
                <div class="mb-4">
                    <label class="text-sm font-medium text-gray-500">Pengalaman Mengajar</label>
                    <p class="text-gray-900 whitespace-pre-line">${data.pengalaman_mengajar}</p>
                </div>
                ` : ''}
                ${data.prestasi ? `
                <div>
                    <label class="text-sm font-medium text-gray-500">Prestasi</label>
                    <p class="text-gray-900 whitespace-pre-line">${data.prestasi}</p>
                </div>
                ` : ''}
            </div>
            ` : ''}
            
            <!-- Biodata Tambahan -->
            ${data.organisasi || data.karya_tulis || data.motto ? `
            <div class="mb-6 pb-6 border-b border-gray-200">
                <h4 class="text-lg font-semibold text-gray-900 mb-3">Biodata Tambahan</h4>
                ${data.organisasi ? `
                <div class="mb-4">
                    <label class="text-sm font-medium text-gray-500">Organisasi</label>
                    <p class="text-gray-900 whitespace-pre-line">${data.organisasi}</p>
                </div>
                ` : ''}
                ${data.karya_tulis ? `
                <div class="mb-4">
                    <label class="text-sm font-medium text-gray-500">Karya Tulis</label>
                    <p class="text-gray-900 whitespace-pre-line">${data.karya_tulis}</p>
                </div>
                ` : ''}
                ${data.motto ? `
                <div>
                    <label class="text-sm font-medium text-gray-500">Motto</label>
                    <p class="text-gray-900 italic text-lg">"${data.motto}"</p>
                </div>
                ` : ''}
            </div>
            ` : ''}
            
            <!-- Media Sosial Card (jika ada) -->
            ${hasSocialMedia ? `
            <div class="mb-6">
                <h4 class="text-lg font-semibold text-gray-900 mb-3">Media Sosial</h4>
                <div class="flex flex-wrap gap-3">
                    ${data.whatsapp ? `
                    <a href="https://wa.me/${data.whatsapp}" target="_blank" rel="noopener noreferrer" class="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors">
                        <i class="fab fa-whatsapp"></i>
                        <span>WhatsApp</span>
                    </a>
                    ` : ''}
                    ${data.facebook ? `
                    <a href="${data.facebook}" target="_blank" rel="noopener noreferrer" class="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors">
                        <i class="fab fa-facebook-f"></i>
                        <span>Facebook</span>
                    </a>
                    ` : ''}
                    ${data.instagram ? `
                    <a href="${data.instagram}" target="_blank" rel="noopener noreferrer" class="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700 text-white rounded-lg transition-colors">
                        <i class="fab fa-instagram"></i>
                        <span>Instagram</span>
                    </a>
                    ` : ''}
                    ${data.twitter ? `
                    <a href="${data.twitter}" target="_blank" rel="noopener noreferrer" class="flex items-center gap-2 px-4 py-2 bg-blue-400 hover:bg-blue-500 text-white rounded-lg transition-colors">
                        <i class="fab fa-twitter"></i>
                        <span>Twitter</span>
                    </a>
                    ` : ''}
                    ${data.linkedin ? `
                    <a href="${data.linkedin}" target="_blank" rel="noopener noreferrer" class="flex items-center gap-2 px-4 py-2 bg-blue-700 hover:bg-blue-800 text-white rounded-lg transition-colors">
                        <i class="fab fa-linkedin-in"></i>
                        <span>LinkedIn</span>
                    </a>
                    ` : ''}
                    ${data.youtube ? `
                    <a href="${data.youtube}" target="_blank" rel="noopener noreferrer" class="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors">
                        <i class="fab fa-youtube"></i>
                        <span>YouTube</span>
                    </a>
                    ` : ''}
                    ${data.tiktok ? `
                    <a href="${data.tiktok}" target="_blank" rel="noopener noreferrer" class="flex items-center gap-2 px-4 py-2 bg-gray-800 hover:bg-gray-900 text-white rounded-lg transition-colors">
                        <i class="fab fa-tiktok"></i>
                        <span>TikTok</span>
                    </a>
                    ` : ''}
                </div>
            </div>
            ` : ''}
        </div>
    `;
    
    content.innerHTML = html;
}

// Make pengajar functions globally available
window.openPengajarModal = openPengajarModal;
window.closePengajarModal = closePengajarModal;

// ============================================
// TAB SWITCHERS
// ============================================

// Tab Switcher untuk Timing Kegiatan Harian
function switchTimingTab(tabName, showNotification = true) {
    // Tab names untuk notifikasi
    const tabNames = {
        'putra': 'Santri Putra',
        'putri': 'Santri Putri'
    };
    
    // Hide all timing tab contents dengan fade out
    const timingContents = document.querySelectorAll('.timing-tab-content');
    timingContents.forEach(content => {
        content.classList.add('opacity-0', 'translate-y-4');
      setTimeout(() => {
            content.classList.add('hidden');
      }, 300);
    });
    
    // Remove active class from all buttons
    const timingButtons = document.querySelectorAll('#tab-timing-putra, #tab-timing-putri');
    timingButtons.forEach(btn => {
        if (btn) {
            btn.classList.remove('border-green-500', 'text-green-700', 'font-bold', 'bg-green-100', 'bg-green-200');
            btn.classList.add('border-transparent', 'text-gray-700', 'font-semibold', 'bg-white');
        }
    });
    
    // Show selected tab content dengan fade in
    setTimeout(() => {
        const selectedContent = document.getElementById(`content-timing-${tabName}`);
        if (selectedContent) {
            selectedContent.classList.remove('hidden');
            // Trigger reflow untuk animasi
            selectedContent.offsetHeight;
        setTimeout(() => {
                selectedContent.classList.remove('opacity-0', 'translate-y-4');
                selectedContent.classList.add('opacity-100', 'translate-y-0');
            }, 50);
        }
    }, 300);
    
    // Add active class to selected button
    const selectedButton = document.getElementById(`tab-timing-${tabName}`);
    if (selectedButton) {
        selectedButton.classList.remove('border-transparent', 'text-gray-700', 'font-semibold', 'bg-white');
        selectedButton.classList.add('border-green-500', 'text-green-700', 'font-bold', 'bg-green-100');
    }
    
    // Show notification hanya jika showNotification = true (saat user klik button)
    if (showNotification) {
        showTabNotification(`Menampilkan: ${tabNames[tabName]}`);
    }
}

// Tab Switcher untuk Program
function switchProgramTab(tabName, showNotification = true) {
    // Tab names untuk notifikasi
    const tabNames = {
        'pendidikan': 'Program Pendidikan',
        'kegiatan': 'Program/Kegiatan'
    };
    
    // Hide all tab contents dengan fade out (menggunakan Tailwind classes)
    const contents = document.querySelectorAll('.tab-content');
    contents.forEach(content => {
        content.classList.add('opacity-0', 'translate-y-4');
      setTimeout(() => {
            content.classList.add('hidden');
      }, 300);
    });
    
    // Remove active class from all buttons
    const buttons = document.querySelectorAll('#tab-pendidikan, #tab-kegiatan');
    buttons.forEach(btn => {
        if (btn) {
            btn.classList.remove('border-green-500', 'text-green-700', 'font-bold', 'bg-green-100', 'bg-green-200');
            btn.classList.add('border-transparent', 'text-gray-700', 'font-semibold', 'bg-white');
        }
    });
    
    // Show selected tab content dengan fade in (menggunakan Tailwind classes)
    setTimeout(() => {
        const selectedContent = document.getElementById(`content-${tabName}`);
        if (selectedContent) {
            selectedContent.classList.remove('hidden');
            // Trigger reflow untuk animasi
            selectedContent.offsetHeight;
        setTimeout(() => {
                selectedContent.classList.remove('opacity-0', 'translate-y-4');
                selectedContent.classList.add('opacity-100', 'translate-y-0');
            }, 50);
        }
    }, 300);
    
    // Add active class to selected button
    const selectedButton = document.getElementById(`tab-${tabName}`);
    if (selectedButton) {
        selectedButton.classList.remove('border-transparent', 'text-gray-700', 'font-semibold', 'bg-white');
        selectedButton.classList.add('border-green-500', 'text-green-700', 'font-bold', 'bg-green-100');
    }
    
    // Show notification hanya jika showNotification = true (saat user klik button)
    if (showNotification) {
        showTabNotification(`Menampilkan: ${tabNames[tabName]}`);
    }
}

// Show notification toast
function showTabNotification(message) {
    const notification = document.getElementById('tab-notification');
    const notificationText = document.getElementById('tab-notification-text');
    
    if (notification && notificationText) {
        notificationText.textContent = message;
        // Show notification dengan Tailwind classes
        notification.classList.remove('opacity-0', '-translate-y-4', 'pointer-events-none');
        notification.classList.add('opacity-100', 'translate-y-0');
        
        // Hide notification after 2 seconds
    setTimeout(() => {
            notification.classList.remove('opacity-100', 'translate-y-0');
            notification.classList.add('opacity-0', '-translate-y-4', 'pointer-events-none');
        }, 2000);
    }
}

// Tab Switcher untuk Perlengkapan
function switchPerlengkapanTab(tabName, showNotification = false) {
    // Tab names untuk notifikasi
    const tabNames = {
        'putra': 'Santri Putra',
        'putri': 'Santri Putri'
    };
    
    // Hide all perlengkapan tab contents dengan fade out
    const perlengkapanContents = document.querySelectorAll('.perlengkapan-tab-content');
    perlengkapanContents.forEach(content => {
        content.classList.add('opacity-0', 'translate-y-4');
      setTimeout(() => {
            content.classList.add('hidden');
      }, 300);
    });
    
    // Remove active class from all buttons
    const perlengkapanButtons = document.querySelectorAll('#tab-perlengkapan-putra, #tab-perlengkapan-putri');
    perlengkapanButtons.forEach(btn => {
        if (btn) {
            btn.classList.remove('border-green-500', 'text-green-600', 'font-bold', 'bg-green-50');
            btn.classList.add('border-transparent', 'text-gray-600', 'font-semibold');
        }
    });
    
    // Show selected tab content dengan fade in
    setTimeout(() => {
        const selectedContent = document.getElementById(`content-perlengkapan-${tabName}`);
        if (selectedContent) {
            selectedContent.classList.remove('hidden');
            // Trigger reflow untuk animasi
            selectedContent.offsetHeight;
        setTimeout(() => {
                selectedContent.classList.remove('opacity-0', 'translate-y-4');
                selectedContent.classList.add('opacity-100', 'translate-y-0');
            }, 50);
        }
    }, 300);
    
    // Add active class to selected button
    const selectedButton = document.getElementById(`tab-perlengkapan-${tabName}`);
    if (selectedButton) {
        selectedButton.classList.remove('border-transparent', 'text-gray-600', 'font-semibold');
        selectedButton.classList.add('border-green-500', 'text-green-600', 'font-bold', 'bg-green-50');
    }
    
    // Show notification hanya jika showNotification = true (saat user klik button)
    if (showNotification) {
        showTabNotification(`Menampilkan: ${tabNames[tabName]}`);
    }
}

// Make tab switchers globally available
window.switchTimingTab = switchTimingTab;
window.switchProgramTab = switchProgramTab;
window.switchPerlengkapanTab = switchPerlengkapanTab;

// ============================================
// PROGRAM/KEGIATAN MODAL
// ============================================

// Program/Kegiatan Modal
function openProgramKegiatanModal(programId) {
    const modal = document.getElementById('program-kegiatan-modal');
    const content = document.getElementById('program-kegiatan-modal-content');
    
    if (!modal || !content) return;
    
    // Get program data from JSON
    let programData = null;
    const jsonData = document.querySelector(`[data-program-json-id="${programId}"]`);
    if (jsonData) {
        try {
            programData = JSON.parse(jsonData.textContent);
        } catch (e) {
            console.error('Error parsing program data:', e);
        }
    }
    
    if (!programData) {
        // Fallback: Extract data from the card
        const card = document.querySelector(`[data-program-id="${programId}"]`);
        if (card) {
            const nama = card.querySelector('h3')?.textContent?.trim() || '';
            const deskripsi = card.querySelector('p')?.textContent?.trim() || '';
            const gambar = card.querySelector('img')?.src || '';
            programData = { id: programId, nama, deskripsi, gambar };
        }
    }
    
    if (!programData) {
        content.innerHTML = `
            <div class="text-center py-8">
                <i class="fas fa-exclamation-circle text-4xl text-red-400"></i>
                <p class="mt-4 text-red-600">Data program tidak ditemukan</p>
            </div>
        `;
        modal.classList.remove('hidden');
        return;
    }
    
    // Render modal
    renderProgramKegiatanModal(programData);
    modal.classList.remove('hidden');
}

function closeProgramKegiatanModal(event) {
    if (event) {
        event.stopPropagation();
    }
    
    const modal = document.getElementById('program-kegiatan-modal');
    if (modal) {
        modal.classList.add('hidden');
        const content = document.getElementById('program-kegiatan-modal-content');
        if (content) {
            content.scrollTop = 0;
        }
    }
}

function renderProgramKegiatanModal(data) {
    const content = document.getElementById('program-kegiatan-modal-content');
    if (!content) return;
    
    const html = `
        <!-- Header Card dengan Gradient -->
        <div class="relative bg-gradient-to-br from-green-500 to-blue-500 p-6 md:p-8 text-white">
            <div class="flex items-center justify-between mb-4">
                <div class="flex-1">
                    <h3 class="text-xl md:text-2xl font-bold mb-2">${data.nama}</h3>
                    ${data.tanggal_mulai ? `
                    <p class="text-sm md:text-base text-white/90">
                        <i class="fas fa-calendar mr-2"></i>
                        ${data.tanggal_mulai}
                        ${data.tanggal_selesai ? ` - ${data.tanggal_selesai}` : ''}
                    </p>
                    ` : ''}
                </div>
                <button onclick="closeProgramKegiatanModal()" class="bg-white/20 hover:bg-white/30 text-white p-2 rounded-full transition-colors shadow-lg flex-shrink-0 ml-4">
                    <i class="fas fa-times text-xl"></i>
                </button>
            </div>
            
            ${data.gambar ? `
            <div class="mt-4">
                <img src="${data.gambar}" alt="${data.nama}" class="w-full h-48 md:h-64 object-cover rounded-lg shadow-xl">
            </div>
            ` : ''}
        </div>
        
        <!-- Content Card -->
        <div class="p-4 md:p-6 bg-white">
            ${data.deskripsi ? `
            <div class="mb-6">
                <h4 class="text-lg font-semibold text-gray-900 mb-3">Deskripsi Program</h4>
                <div class="text-gray-700 leading-relaxed prose prose-sm max-w-none">
                    ${data.deskripsi}
                </div>
            </div>
            ` : ''}
            
            ${data.meta_description ? `
            <div class="mb-6 pb-6 border-b border-gray-200">
                <h4 class="text-lg font-semibold text-gray-900 mb-3">Informasi Tambahan</h4>
                <p class="text-gray-700 leading-relaxed">${data.meta_description}</p>
            </div>
            ` : ''}
        </div>
    `;
    
    content.innerHTML = html;
}

// Make program/kegiatan modal functions globally available
window.openProgramKegiatanModal = openProgramKegiatanModal;
window.closeProgramKegiatanModal = closeProgramKegiatanModal;

// ============================================
// INITIALIZATION
// ============================================

// Initialize tabs and event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tab - show pendidikan by default (tanpa notifikasi)
    if (document.getElementById('content-pendidikan')) {
        switchProgramTab('pendidikan', false);
    }
    
    // Initialize timing tab - show putra by default (tanpa notifikasi)
    if (document.getElementById('content-timing-putra')) {
        switchTimingTab('putra', false);
    }
    
    // Initialize perlengkapan tab - show putra by default (tanpa notifikasi)
    if (document.getElementById('content-perlengkapan-putra')) {
        switchPerlengkapanTab('putra', false);
    }
    
    // Program cards click handlers
    const programCards = document.querySelectorAll('.program-kegiatan-card');
    programCards.forEach((card) => {
        card.addEventListener('click', function() {
            // Get program ID from data attribute
            const programId = this.dataset.programId;
            if (programId) {
                openProgramKegiatanModal(programId);
            }
        });
      });
  });

