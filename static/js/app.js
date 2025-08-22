// Cartalyst Application JavaScript

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeLazyLoading();
    initializeImageErrorHandling();
    initializeToastNotifications();
    initializeSearchEnhancements();
    initializePartComparison();
    initializeAccessibility();
});

// Lazy Loading Implementation
function initializeLazyLoading() {
    const lazyImages = document.querySelectorAll('.lazy-load');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            });
        });

        lazyImages.forEach(img => {
            imageObserver.observe(img);
        });
    } else {
        // Fallback for browsers without IntersectionObserver
        lazyImages.forEach(img => {
            img.classList.add('loaded');
        });
    }
}

// Image Error Handling
function initializeImageErrorHandling() {
    const images = document.querySelectorAll('img');
    
    images.forEach(img => {
        img.addEventListener('error', function() {
            // Replace with default image if loading fails
            this.src = '/static/images/parts/default.jpeg';
            this.alt = 'Default part image';
            
            // Add error class for styling
            this.classList.add('image-error');
        });
        
        img.addEventListener('load', function() {
            this.classList.add('image-loaded');
        });
    });
}

// Toast Notification System
let toastContainer = null;

function initializeToastNotifications() {
    // Create toast container if it doesn't exist
    if (!document.getElementById('toast-container')) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'fixed top-4 right-4 z-50 space-y-2';
        document.body.appendChild(toastContainer);
    } else {
        toastContainer = document.getElementById('toast-container');
    }
}

function showToast(message, type = 'success', duration = 5000) {
    const toast = document.createElement('div');
    toast.className = `toast ${type} px-4 py-3 rounded-lg shadow-lg transform translate-x-full transition-transform duration-300`;
    
    const icon = getToastIcon(type);
    toast.innerHTML = `
        <div class="flex items-center space-x-2">
            ${icon}
            <span class="font-medium">${message}</span>
            <button onclick="closeToast(this)" class="ml-2 text-white hover:text-gray-200">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
            </button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Trigger animation
    setTimeout(() => {
        toast.classList.remove('translate-x-full');
    }, 100);
    
    // Auto remove
    setTimeout(() => {
        closeToast(toast.querySelector('button'));
    }, duration);
}

function getToastIcon(type) {
    const icons = {
        success: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>',
        error: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>',
        warning: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>',
        info: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>'
    };
    return icons[type] || icons.info;
}

function closeToast(button) {
    const toast = button.closest('.toast');
    toast.classList.add('translate-x-full');
    setTimeout(() => {
        toast.remove();
    }, 300);
}

// Enhanced Search Functionality
function initializeSearchEnhancements() {
    const searchInputs = document.querySelectorAll('input[name="q"]');
    
    searchInputs.forEach(input => {
        // Add search suggestions (basic implementation)
        input.addEventListener('input', debounce(handleSearchInput, 300));
        
        // Handle enter key
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                performSearch(this.value);
            }
        });
    });
}

function handleSearchInput(e) {
    const query = e.target.value.trim();
    if (query.length < 2) return;
    
    // Here you could implement search suggestions
    // For now, we'll just add visual feedback
    e.target.classList.add('search-active');
}

function performSearch(query) {
    if (!query.trim()) {
        showToast('Please enter a search term', 'warning');
        return;
    }
    
    // Show loading state
    const searchButton = document.querySelector('button[type="submit"]');
    if (searchButton) {
        const originalContent = searchButton.innerHTML;
        searchButton.innerHTML = '<div class="spinner"></div>';
        searchButton.disabled = true;
        
        // Restore button after a short delay (form submission will handle the actual search)
        setTimeout(() => {
            searchButton.innerHTML = originalContent;
            searchButton.disabled = false;
        }, 1000);
    }
    
    window.location.href = `/search?q=${encodeURIComponent(query)}`;
}

// Part Comparison Feature
let comparisonList = JSON.parse(localStorage.getItem('partComparison') || '[]');

function initializePartComparison() {
    updateComparisonUI();
    
    // Add comparison buttons to part cards
    const partCards = document.querySelectorAll('.part-card');
    partCards.forEach(card => {
        addComparisonButton(card);
    });
}

function addComparisonButton(card) {
    const partNo = card.querySelector('[data-part-no]')?.dataset.partNo;
    if (!partNo) return;
    
    const actionButtons = card.querySelector('.flex.space-x-2');
    if (!actionButtons) return;
    
    const compareButton = document.createElement('button');
    compareButton.className = 'px-3 py-1 text-xs border border-gray-300 rounded hover:bg-gray-50 transition-colors';
    compareButton.innerHTML = comparisonList.includes(partNo) ? 'Remove' : 'Compare';
    compareButton.onclick = () => toggleComparison(partNo, compareButton);
    
    actionButtons.appendChild(compareButton);
}

function toggleComparison(partNo, button) {
    const index = comparisonList.indexOf(partNo);
    
    if (index > -1) {
        comparisonList.splice(index, 1);
        button.innerHTML = 'Compare';
        showToast('Part removed from comparison', 'info');
    } else {
        if (comparisonList.length >= 3) {
            showToast('Maximum 3 parts can be compared', 'warning');
            return;
        }
        comparisonList.push(partNo);
        button.innerHTML = 'Remove';
        showToast('Part added to comparison', 'success');
    }
    
    localStorage.setItem('partComparison', JSON.stringify(comparisonList));
    updateComparisonUI();
}

function updateComparisonUI() {
    let comparisonWidget = document.getElementById('comparison-widget');
    
    if (comparisonList.length === 0) {
        if (comparisonWidget) {
            comparisonWidget.remove();
        }
        return;
    }
    
    if (!comparisonWidget) {
        comparisonWidget = document.createElement('div');
        comparisonWidget.id = 'comparison-widget';
        comparisonWidget.className = 'fixed bottom-4 right-4 bg-white border border-gray-300 rounded-lg shadow-lg p-4 z-40';
        document.body.appendChild(comparisonWidget);
    }
    
    comparisonWidget.innerHTML = `
        <div class="flex items-center justify-between mb-2">
            <h4 class="font-semibold text-sm">Compare Parts (${comparisonList.length}/3)</h4>
            <button onclick="clearComparison()" class="text-gray-400 hover:text-gray-600">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
            </button>
        </div>
        <div class="space-y-1 mb-3">
            ${comparisonList.map(partNo => `<div class="text-xs text-gray-600">${partNo}</div>`).join('')}
        </div>
        <button onclick="viewComparison()" class="w-full bg-blue-600 text-white text-sm py-2 rounded hover:bg-blue-700 transition-colors">
            View Comparison
        </button>
    `;
}

function clearComparison() {
    comparisonList = [];
    localStorage.removeItem('partComparison');
    updateComparisonUI();
    showToast('Comparison cleared', 'info');
}

function viewComparison() {
    if (comparisonList.length < 2) {
        showToast('Add at least 2 parts to compare', 'warning');
        return;
    }
    
    // For now, just show the part numbers
    // In a full implementation, this would open a comparison modal
    const partsList = comparisonList.join(', ');
    showToast(`Comparing parts: ${partsList}`, 'info', 8000);
}

// Enhanced Cart Functionality
async function addToCart(partNo, quantity = 1) {
    try {
        // Show loading state
        const button = event.target;
        const originalText = button.textContent;
        button.textContent = 'Adding...';
        button.disabled = true;
        
        const response = await fetch('/api/cart/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                part_no: partNo,
                quantity: quantity
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Item added to cart successfully!', 'success');
            updateCartCount();
        } else {
            showToast(data.error || 'Failed to add item to cart', 'error');
        }
    } catch (error) {
        console.error('Error adding to cart:', error);
        showToast('Error adding item to cart', 'error');
    } finally {
        // Restore button state
        const button = event.target;
        button.textContent = originalText;
        button.disabled = false;
    }
}

// Update cart count in header
async function updateCartCount() {
    try {
        const response = await fetch('/api/cart/count');
        if (response.ok) {
            const data = await response.json();
            const cartLinks = document.querySelectorAll('a[href*="cart"]');
            cartLinks.forEach(link => {
                const countElement = link.querySelector('.cart-count');
                if (countElement) {
                    countElement.textContent = data.count;
                } else if (data.count > 0) {
                    const badge = document.createElement('span');
                    badge.className = 'cart-count bg-red-500 text-white text-xs rounded-full px-2 py-1 ml-1';
                    badge.textContent = data.count;
                    link.appendChild(badge);
                }
            });
        }
    } catch (error) {
        console.error('Error updating cart count:', error);
    }
}

// Accessibility Enhancements
function initializeAccessibility() {
    // Add keyboard navigation for cards
    const cards = document.querySelectorAll('.part-card');
    cards.forEach(card => {
        card.setAttribute('tabindex', '0');
        card.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                const link = this.querySelector('a');
                if (link) {
                    link.click();
                }
            }
        });
    });
    
    // Add skip links
    addSkipLinks();
    
    // Enhance focus management
    enhanceFocusManagement();
}

function addSkipLinks() {
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.className = 'sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 bg-blue-600 text-white px-4 py-2 rounded z-50';
    skipLink.textContent = 'Skip to main content';
    document.body.insertBefore(skipLink, document.body.firstChild);
}

function enhanceFocusManagement() {
    // Add focus indicators
    const focusableElements = document.querySelectorAll('button, a, input, select, textarea, [tabindex]:not([tabindex="-1"])');
    
    focusableElements.forEach(element => {
        element.addEventListener('focus', function() {
            this.classList.add('focus-visible');
        });
        
        element.addEventListener('blur', function() {
            this.classList.remove('focus-visible');
        });
    });
}

// Utility Functions
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

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

function formatNumber(number) {
    return new Intl.NumberFormat('en-IN').format(number);
}

// Export functions for global use
window.CartalystApp = {
    showToast,
    addToCart,
    toggleComparison,
    clearComparison,
    viewComparison,
    performSearch,
    formatCurrency,
    formatNumber
};