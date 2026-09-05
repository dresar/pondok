/**
 * AJAX Filter untuk Admin Panel
 * Universal filter function yang bisa digunakan di semua halaman admin panel
 */

(function() {
    'use strict';

    // Debounce function untuk search input
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Main filter function
    function initAjaxFilter(formId, targetContainerId, url, options = {}) {
        const form = document.getElementById(formId);
        if (!form) return;

        const targetContainer = document.getElementById(targetContainerId);
        if (!targetContainer) return;

        const defaultOptions = {
            pushUrl: true,
            showLoading: true,
            loadingClass: 'opacity-50 pointer-events-none',
            debounceDelay: 500,
            ...options
        };

        // Loading indicator
        let loadingIndicator = null;
        if (defaultOptions.showLoading) {
            loadingIndicator = document.createElement('div');
            loadingIndicator.className = 'fixed top-4 right-4 bg-blue-600 text-white px-4 py-2 rounded-lg shadow-lg z-50 hidden';
            loadingIndicator.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Memuat...';
            document.body.appendChild(loadingIndicator);
        }

        // Show loading
        function showLoading() {
            if (loadingIndicator) {
                loadingIndicator.classList.remove('hidden');
            }
            if (defaultOptions.showLoading) {
                // Split multiple classes and add them individually
                const classes = defaultOptions.loadingClass.split(' ');
                classes.forEach(cls => {
                    if (cls.trim()) {
                        targetContainer.classList.add(cls.trim());
                    }
                });
            }
        }

        // Hide loading
        function hideLoading() {
            if (loadingIndicator) {
                loadingIndicator.classList.add('hidden');
            }
            if (defaultOptions.showLoading) {
                // Split multiple classes and remove them individually
                const classes = defaultOptions.loadingClass.split(' ');
                classes.forEach(cls => {
                    if (cls.trim()) {
                        targetContainer.classList.remove(cls.trim());
                    }
                });
            }
        }

        // AJAX request function
        function performFilter() {
            const formData = new FormData(form);
            const params = new URLSearchParams(formData);
            
            // Build URL with query params
            let requestUrl = url;
            if (params.toString()) {
                requestUrl += (url.includes('?') ? '&' : '?') + params.toString();
            }

            showLoading();

            // Create XMLHttpRequest
            const xhr = new XMLHttpRequest();
            xhr.open('GET', requestUrl, true);
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            xhr.setRequestHeader('Accept', 'text/html');

            xhr.onload = function() {
                hideLoading();
                
                if (xhr.status >= 200 && xhr.status < 300) {
                    // Update target container
                    targetContainer.innerHTML = xhr.responseText;
                    
                    // Update URL without reload
                    if (defaultOptions.pushUrl) {
                        window.history.pushState({}, '', requestUrl);
                    }
                    
                    // Trigger custom event
                    const event = new CustomEvent('filterUpdated', {
                        detail: { url: requestUrl, params: params.toString() }
                    });
                    document.dispatchEvent(event);
                } else {
                    console.error('Filter request failed:', xhr.status, xhr.statusText);
                    alert('Terjadi kesalahan saat memuat data. Silakan coba lagi.');
                }
            };

            xhr.onerror = function() {
                hideLoading();
                console.error('Filter request error');
                alert('Terjadi kesalahan saat memuat data. Silakan coba lagi.');
            };

            xhr.send();
        }

        // Debounced filter function
        const debouncedFilter = debounce(performFilter, defaultOptions.debounceDelay);

        // Attach event listeners to all form inputs
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            // For text inputs, use debounced filter
            if (input.type === 'text' || input.type === 'search') {
                input.addEventListener('input', debouncedFilter);
            }
            // For selects and other inputs, use immediate filter
            else {
                input.addEventListener('change', performFilter);
            }
        });

        // Handle browser back/forward buttons
        window.addEventListener('popstate', function() {
            performFilter();
        });
    }

    // Auto-initialize filters on page load
    document.addEventListener('DOMContentLoaded', function() {
        // Initialize all filters with data attributes
        const filterForms = document.querySelectorAll('[data-ajax-filter]');
        filterForms.forEach(form => {
            const formId = form.id || form.getAttribute('id');
            const targetId = form.getAttribute('data-target');
            const url = form.getAttribute('data-url') || form.getAttribute('action');
            
            if (formId && targetId && url) {
                initAjaxFilter(formId, targetId, url);
            }
        });
    });

    // Export function for manual initialization
    window.initAjaxFilter = initAjaxFilter;
})();

