// Medical Search App JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the app
    initializeApp();
});

function initializeApp() {
    // Initialize tooltips if Bootstrap is loaded
    if (typeof bootstrap !== 'undefined') {
        initializeTooltips();
    }
    
    // Initialize search functionality
    initializeSearch();
    
    // Initialize UI enhancements
    initializeUIEnhancements();
    
    // Initialize accessibility features
    initializeAccessibility();
}

function initializeTooltips() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function initializeSearch() {
    const searchForm = document.querySelector('form[method="POST"]');
    const searchInput = document.querySelector('input[name="query"]');
    
    if (!searchForm || !searchInput) return;
    
    // Add search suggestions functionality
    initializeSearchSuggestions(searchInput);
    
    // Handle form submission
    searchForm.addEventListener('submit', function(e) {
        const query = searchInput.value.trim();
        
        if (!query) {
            e.preventDefault();
            showAlert('Please enter a medical question or search term.', 'warning');
            searchInput.focus();
            return;
        }
        
        // Show loading state
        showSearchLoading(true);
        
        // Log search for analytics (if needed)
        logSearch(query);
    });
    
    // Handle Enter key in search input
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchForm.dispatchEvent(new Event('submit'));
        }
    });
}

function initializeSearchSuggestions(searchInput) {
    // Medical search suggestions
    const medicalSuggestions = [
        'Type 2 diabetes management guidelines',
        'Hypertension treatment protocols',
        'COVID-19 clinical trials',
        'Cardiac arrest resuscitation',
        'Pneumonia antibiotic therapy',
        'Stroke rehabilitation guidelines',
        'Cancer screening recommendations',
        'Depression treatment algorithms',
        'Asthma management protocols',
        'Sepsis treatment guidelines',
        'Heart failure medications',
        'Wound healing techniques',
        'Pain management strategies',
        'Vaccine efficacy studies',
        'Diagnostic imaging guidelines'
    ];
    
    let suggestionTimeout;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(suggestionTimeout);
        const query = this.value.trim().toLowerCase();
        
        if (query.length < 3) {
            hideSuggestions();
            return;
        }
        
        suggestionTimeout = setTimeout(() => {
            const matches = medicalSuggestions.filter(suggestion => 
                suggestion.toLowerCase().includes(query)
            ).slice(0, 5);
            
            if (matches.length > 0) {
                showSuggestions(matches, searchInput);
            } else {
                hideSuggestions();
            }
        }, 300);
    });
    
    // Hide suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.search-suggestions') && e.target !== searchInput) {
            hideSuggestions();
        }
    });
}

function showSuggestions(suggestions, searchInput) {
    hideSuggestions(); // Remove existing suggestions
    
    const suggestionsContainer = document.createElement('div');
    suggestionsContainer.className = 'search-suggestions position-absolute bg-white border rounded shadow-sm w-100';
    suggestionsContainer.style.cssText = 'z-index: 1000; top: 100%; left: 0; max-height: 300px; overflow-y: auto;';
    
    suggestions.forEach(suggestion => {
        const suggestionItem = document.createElement('div');
        suggestionItem.className = 'suggestion-item p-2 border-bottom cursor-pointer';
        suggestionItem.style.cursor = 'pointer';
        suggestionItem.textContent = suggestion;
        
        suggestionItem.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#f8f9fa';
        });
        
        suggestionItem.addEventListener('mouseleave', function() {
            this.style.backgroundColor = 'white';
        });
        
        suggestionItem.addEventListener('click', function() {
            searchInput.value = suggestion;
            hideSuggestions();
            searchInput.focus();
        });
        
        suggestionsContainer.appendChild(suggestionItem);
    });
    
    // Position the suggestions relative to the search input
    const inputContainer = searchInput.closest('.input-group') || searchInput.parentElement;
    inputContainer.style.position = 'relative';
    inputContainer.appendChild(suggestionsContainer);
}

function hideSuggestions() {
    const existingSuggestions = document.querySelector('.search-suggestions');
    if (existingSuggestions) {
        existingSuggestions.remove();
    }
}

function showSearchLoading(show) {
    const submitBtn = document.querySelector('button[type="submit"]');
    if (!submitBtn) return;
    
    const originalText = submitBtn.innerHTML;
    
    if (show) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2" role="status"></span>
            Searching...
        `;
    } else {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    }
}

function initializeUIEnhancements() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const href = this.getAttribute('href');
            if (!href || href === '#') return;
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add hover effects to result cards
    document.querySelectorAll('.result-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Initialize copy functionality for search results
    initializeCopyFunctionality();
    
    // Initialize keyboard shortcuts
    initializeKeyboardShortcuts();
}

function initializeCopyFunctionality() {
    // Add copy buttons to summaries and content
    document.querySelectorAll('.ai-summary, .content-text').forEach(element => {
        const copyBtn = document.createElement('button');
        copyBtn.className = 'btn btn-outline-secondary btn-sm copy-btn';
        copyBtn.innerHTML = '<i data-feather="copy"></i>';
        copyBtn.title = 'Copy to clipboard';
        copyBtn.style.cssText = 'position: absolute; top: 0.5rem; right: 0.5rem; opacity: 0; transition: opacity 0.2s;';
        
        element.style.position = 'relative';
        element.appendChild(copyBtn);
        
        // Show/hide copy button on hover
        element.addEventListener('mouseenter', () => {
            copyBtn.style.opacity = '1';
        });
        
        element.addEventListener('mouseleave', () => {
            copyBtn.style.opacity = '0';
        });
        
        // Handle copy action
        copyBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const textToCopy = element.textContent.trim();
            copyToClipboard(textToCopy);
            
            // Show feedback
            const originalHTML = this.innerHTML;
            this.innerHTML = '<i data-feather="check"></i>';
            this.classList.add('btn-success');
            
            setTimeout(() => {
                this.innerHTML = originalHTML;
                this.classList.remove('btn-success');
                feather.replace();
            }, 2000);
        });
    });
    
    // Reinitialize Feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        // Modern async clipboard API
        navigator.clipboard.writeText(text).then(() => {
            showAlert('Content copied to clipboard!', 'success');
        }).catch(() => {
            fallbackCopyToClipboard(text);
        });
    } else {
        // Fallback for older browsers
        fallbackCopyToClipboard(text);
    }
}

function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.cssText = 'position: fixed; top: -9999px; left: -9999px;';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showAlert('Content copied to clipboard!', 'success');
    } catch (err) {
        showAlert('Failed to copy content', 'error');
    }
    
    document.body.removeChild(textArea);
}

function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Focus search input with Ctrl/Cmd + K
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[name="query"]');
            if (searchInput) {
                searchInput.focus();
                searchInput.select();
            }
        }
        
        // Escape key to clear search or close modals
        if (e.key === 'Escape') {
            hideSuggestions();
            
            // Close any open modals
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                const modal = bootstrap.Modal.getInstance(openModal);
                if (modal) modal.hide();
            }
        }
    });
}

function initializeAccessibility() {
    // Add ARIA labels to interactive elements
    document.querySelectorAll('.quick-search').forEach(btn => {
        btn.setAttribute('aria-label', `Search for ${btn.textContent}`);
    });
    
    // Improve focus management
    document.querySelectorAll('.result-card a').forEach(link => {
        link.addEventListener('focus', function() {
            this.closest('.result-card').style.outline = '2px solid var(--medical-blue)';
        });
        
        link.addEventListener('blur', function() {
            this.closest('.result-card').style.outline = 'none';
        });
    });
    
    // Add skip links for screen readers
    addSkipLinks();
}

function addSkipLinks() {
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'Skip to main content';
    skipLink.className = 'visually-hidden-focusable btn btn-medical';
    skipLink.style.cssText = 'position: absolute; top: 1rem; left: 1rem; z-index: 9999;';
    
    document.body.insertBefore(skipLink, document.body.firstChild);
    
    // Add main content ID if not present
    const mainElement = document.querySelector('main') || document.querySelector('.container').parentElement;
    if (mainElement && !mainElement.id) {
        mainElement.id = 'main-content';
    }
}

function showAlert(message, type = 'info') {
    // Create alert element
    const alert = document.createElement('div');
    alert.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    alert.style.cssText = 'position: fixed; top: 1rem; right: 1rem; z-index: 9999; min-width: 300px; max-width: 500px;';
    
    const icon = getIconForAlertType(type);
    alert.innerHTML = `
        <i data-feather="${icon}" class="me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alert);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alert.parentElement) {
            alert.classList.remove('show');
            setTimeout(() => {
                if (alert.parentElement) {
                    alert.remove();
                }
            }, 300);
        }
    }, 5000);
    
    // Reinitialize Feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

function getIconForAlertType(type) {
    const icons = {
        success: 'check-circle',
        error: 'alert-circle',
        warning: 'alert-triangle',
        info: 'info'
    };
    return icons[type] || 'info';
}

function logSearch(query) {
    // Log search query for analytics (implement as needed)
    console.log('Search query:', query);
    
    // You can integrate with analytics services here
    // Example: gtag('event', 'search', { search_term: query });
}

// Feature modal functions (referenced in base.html)
function showFeatureModal(feature) {
    const modal = document.getElementById('featureModal');
    const title = document.getElementById('featureModalLabel');
    const text = document.getElementById('featureModalText');
    
    const featureInfo = {
        calculators: {
            title: 'Medical Calculators',
            text: 'Clinical risk calculators and assessment tools are being developed. This feature will include cardiovascular risk scores, dosage calculators, and clinical prediction rules.'
        },
        guidelines: {
            title: 'Clinical Guidelines',
            text: 'Evidence-based clinical practice guidelines are being curated. This feature will provide quick access to the latest treatment protocols and diagnostic criteria.'
        }
    };
    
    const info = featureInfo[feature] || {
        title: 'Feature Coming Soon',
        text: 'This feature is currently being developed and will be available soon.'
    };
    
    title.textContent = info.title;
    text.textContent = info.text;
    
    const bootstrapModal = new bootstrap.Modal(modal);
    bootstrapModal.show();
}

// Global error handler
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    
    // Show user-friendly error message for critical errors
    if (e.error && e.error.message) {
        showAlert('An unexpected error occurred. Please refresh the page and try again.', 'error');
    }
});

// Handle unhandled promise rejections
window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
    e.preventDefault(); // Prevent the default browser behavior
});
