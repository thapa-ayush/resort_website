// Diamond Hill Resort - Main JavaScript

// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Initialize hero slideshow
    initHeroSlideshow();
    
    // Initialize booking summary
    updateBookingSummary();
    initGalleryLightbox();
});

/**
 * Initialize hero slideshow transitions
 */
function initHeroSlideshow() {
    const slides = document.querySelectorAll('.hero-slideshow .slide');
    const slideTexts = document.querySelectorAll('.hero-slide-text');
    const slideDots = document.querySelectorAll('.slide-dot');
    
    if (slides.length === 0) return;
    
    let currentSlideIndex = 0;
    const slideInterval = 6000; // 6 seconds per slide
    
    // Function to update slide display
    function showSlide(index) {
        // Update images
        slides.forEach((slide, i) => {
            slide.style.opacity = i === index ? '1' : '0';
        });
        
        // Update text content
        slideTexts.forEach((text, i) => {
            text.style.display = i === index ? 'block' : 'none';
        });
        
        // Update dot indicators
        slideDots.forEach((dot, i) => {
            dot.classList.toggle('active', i === index);
        });
    }
    
    // Auto-advance slides
    function nextSlide() {
        currentSlideIndex = (currentSlideIndex + 1) % slides.length;
        showSlide(currentSlideIndex);
    }
    
    // Handle dot click navigation
    slideDots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentSlideIndex = index;
            showSlide(currentSlideIndex);
        });
    });
    
    // Start auto-advance
    setInterval(nextSlide, slideInterval);
}

/**
 * Format currency to NPR
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-NP', {
        style: 'currency',
        currency: 'NPR',
    }).format(amount);
}

/**
 * Calculate booking total
 */
function calculateTotal(roomPrice, checkIn, checkOut, guests) {
    const checkInDate = new Date(checkIn);
    const checkOutDate = new Date(checkOut);
    const nights = Math.ceil((checkOutDate - checkInDate) / (1000 * 60 * 60 * 24));
    
    if (nights <= 0) return 0;
    
    return roomPrice * nights * guests;
}

/**
 * Update booking summary
 */
function updateBookingSummary() {
    const roomSelect = document.getElementById('roomSelect');
    const checkInInput = document.querySelector('input[name="check_in"]');
    const checkOutInput = document.querySelector('input[name="check_out"]');
    const guestsInput = document.querySelector('input[name="guests"]');
    const summaryDisplay = document.getElementById('totalSummary');

    if (!roomSelect || !checkInInput || !checkOutInput || !guestsInput) return;

    function update() {
        const selectedOption = roomSelect.options[roomSelect.selectedIndex];
        const roomPrice = parseFloat(selectedOption.dataset.price) || 0;
        
        const checkIn = checkInInput.value;
        const checkOut = checkOutInput.value;
        const guests = parseInt(guestsInput.value) || 1;

        if (checkIn && checkOut && roomPrice > 0) {
            const total = calculateTotal(roomPrice, checkIn, checkOut, guests);
            if (summaryDisplay) {
                summaryDisplay.textContent = formatCurrency(total);
            }
        }
    }

    roomSelect.addEventListener('change', update);
    checkInInput.addEventListener('change', update);
    checkOutInput.addEventListener('change', update);
    guestsInput.addEventListener('change', update);
    
    update(); // Initial calculation
}

/**
 * Handle gallery lightbox
 */
function initGalleryLightbox() {
    const galleryItems = document.querySelectorAll('.gallery-item img');
    
    galleryItems.forEach(item => {
        item.addEventListener('click', function() {
            const modal = document.getElementById('imageModal');
            if (modal) {
                const modalImage = document.getElementById('modalImage');
                const modalCaption = document.getElementById('modalCaption');
                
                modalImage.src = this.src;
                modalCaption.textContent = this.alt;
            }
        });
    });
}

/**
 * Show loading spinner
 */
function showSpinner(show = true) {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.style.display = show ? 'flex' : 'none';
    }
}

/**
 * Validate email
 */
function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    toastContainer.appendChild(toast);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

/**
 * Create toast container if it doesn't exist
 */
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.style.position = 'fixed';
    container.style.top = '20px';
    container.style.right = '20px';
    container.style.zIndex = '9999';
    container.style.maxWidth = '400px';
    document.body.appendChild(container);
    return container;
}

/**
 * Debounce function for search/filter
 */
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

/**
 * Filter rooms by price
 */
function filterRoomsByPrice(minPrice, maxPrice) {
    const rooms = document.querySelectorAll('[data-room-card]');
    
    rooms.forEach(room => {
        const price = parseFloat(room.dataset.price);
        if (price >= minPrice && price <= maxPrice) {
            room.style.display = 'block';
        } else {
            room.style.display = 'none';
        }
    });
}

/**
 * Export data to CSV (for admin)
 */
function exportToCSV(data, filename = 'export.csv') {
    const csv = data.map(row => row.join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

/**
 * Log analytics event
 */
function logAnalytics(event, data = {}) {
    console.log(`[Analytics] ${event}`, data);
    // In production, send to analytics service (e.g., Google Analytics)
    if (typeof gtag !== 'undefined') {
        gtag('event', event, data);
    }
}

// Initialize on page load
// Note: Already initialized in DOMContentLoaded event above
