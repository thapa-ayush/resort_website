// Admin Dashboard Scripts

// Sidebar Active Link Highlighting
function initializeSidebar() {
    const currentPath = window.location.pathname;
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    
    sidebarLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.includes(href)) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// Search Functionality
function initializeSearch() {
    const searchInput = document.querySelector('.search-box input');
    if (!searchInput) return;
    
    searchInput.addEventListener('keyup', function(e) {
        const searchTerm = this.value.toLowerCase();
        const tableRows = document.querySelectorAll('tbody tr');
        
        tableRows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    });
}

// Checkbox Selection
function initializeCheckboxes() {
    const selectAllCheckbox = document.querySelector('.select-all');
    const itemCheckboxes = document.querySelectorAll('.item-checkbox');
    
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            itemCheckboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
            updateBulkActionsUI();
        });
    }
    
    itemCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const allChecked = Array.from(itemCheckboxes).every(cb => cb.checked);
            const someChecked = Array.from(itemCheckboxes).some(cb => cb.checked);
            
            if (selectAllCheckbox) {
                selectAllCheckbox.checked = allChecked;
                selectAllCheckbox.indeterminate = someChecked && !allChecked;
            }
            
            updateBulkActionsUI();
        });
    });
}

// Update Bulk Actions UI
function updateBulkActionsUI() {
    const bulkActionsSection = document.querySelector('.bulk-actions');
    const itemCheckboxes = document.querySelectorAll('.item-checkbox');
    const selectedCount = Array.from(itemCheckboxes).filter(cb => cb.checked).length;
    
    if (bulkActionsSection) {
        if (selectedCount > 0) {
            bulkActionsSection.classList.add('show');
            const bulkText = bulkActionsSection.querySelector('.bulk-text');
            if (bulkText) {
                bulkText.textContent = `${selectedCount} item${selectedCount !== 1 ? 's' : ''} selected`;
            }
        } else {
            bulkActionsSection.classList.remove('show');
        }
    }
    
    // Update stats
    updateStats();
}

// Update Stats
function updateStats() {
    const statElement = document.querySelector('[data-stat="selected"]');
    if (!statElement) return;
    
    const itemCheckboxes = document.querySelectorAll('.item-checkbox');
    const selectedCount = Array.from(itemCheckboxes).filter(cb => cb.checked).length;
    const totalCount = itemCheckboxes.length;
    
    statElement.textContent = `${selectedCount} of ${totalCount} selected`;
}

// Table Sorting
function initializeTableSorting() {
    const sortableHeaders = document.querySelectorAll('th.sortable');
    
    sortableHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const table = this.closest('table');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const cellIndex = Array.from(this.parentNode.children).indexOf(this);
            const isAscending = this.classList.contains('sort-asc');
            
            // Remove all sort indicators
            sortableHeaders.forEach(h => {
                h.classList.remove('sort-asc', 'sort-desc');
            });
            
            // Add sort indicator
            this.classList.toggle('sort-asc', !isAscending);
            this.classList.toggle('sort-desc', isAscending);
            
            // Sort rows
            rows.sort((a, b) => {
                const aValue = a.cells[cellIndex].textContent.trim();
                const bValue = b.cells[cellIndex].textContent.trim();
                
                // Try to parse as numbers
                const aNum = parseFloat(aValue);
                const bNum = parseFloat(bValue);
                
                if (!isNaN(aNum) && !isNaN(bNum)) {
                    return isAscending ? aNum - bNum : bNum - aNum;
                }
                
                // String comparison
                return isAscending 
                    ? aValue.localeCompare(bValue)
                    : bValue.localeCompare(aValue);
            });
            
            // Re-append sorted rows
            rows.forEach(row => tbody.appendChild(row));
        });
    });
}

// Bulk Actions
function initializeBulkActions() {
    const bulkPublishBtn = document.querySelector('.bulk-publish');
    const bulkDeleteBtn = document.querySelector('.bulk-delete');
    
    if (bulkPublishBtn) {
        bulkPublishBtn.addEventListener('click', function() {
            const selected = getSelectedItems();
            if (selected.length > 0) {
                if (confirm(`Publish ${selected.length} item(s)?`)) {
                    performBulkAction('publish', selected);
                }
            }
        });
    }
    
    if (bulkDeleteBtn) {
        bulkDeleteBtn.addEventListener('click', function() {
            const selected = getSelectedItems();
            if (selected.length > 0) {
                if (confirm(`Delete ${selected.length} item(s)? This action cannot be undone.`)) {
                    performBulkAction('delete', selected);
                }
            }
        });
    }
}

// Get Selected Items
function getSelectedItems() {
    const checkboxes = document.querySelectorAll('.item-checkbox:checked');
    return Array.from(checkboxes).map(cb => cb.value);
}

// Perform Bulk Action
function performBulkAction(action, items) {
    // This would typically make an AJAX request to the server
    console.log(`Performing ${action} on items:`, items);
    
    // Example implementation (uncomment and modify for your needs):
    /*
    fetch('/api/bulk-action/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({ action, items })
    })
    .then(response => response.json())
    .then(data => {
        alert('Action completed');
        location.reload();
    })
    .catch(error => console.error('Error:', error));
    */
}

// Pagination
function initializePagination() {
    const paginationButtons = document.querySelectorAll('.pagination button');
    
    paginationButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.classList.contains('active') || this.textContent === '...') {
                return;
            }
            
            // Handle pagination logic here
            console.log('Navigate to page:', this.textContent);
        });
    });
}

// Filter
function initializeFilters() {
    const filterSelects = document.querySelectorAll('select[data-filter]');
    
    filterSelects.forEach(select => {
        select.addEventListener('change', function() {
            const filterType = this.dataset.filter;
            const filterValue = this.value;
            
            // Apply filter
            applyFilter(filterType, filterValue);
        });
    });
}

// Apply Filter
function applyFilter(filterType, filterValue) {
    const tableRows = document.querySelectorAll('tbody tr');
    
    tableRows.forEach(row => {
        // This is a simple example - adjust based on your table structure
        let shouldShow = true;
        
        if (filterValue && filterValue !== 'all') {
            const cellText = row.textContent.toLowerCase();
            shouldShow = cellText.includes(filterValue.toLowerCase());
        }
        
        row.style.display = shouldShow ? '' : 'none';
    });
}

// Image Preview Modal
function initializeImagePreview() {
    const images = document.querySelectorAll('.room-img');
    
    images.forEach(image => {
        image.addEventListener('click', function() {
            const modal = createModal(this.src);
            document.body.appendChild(modal);
        });
    });
}

// Create Modal
function createModal(imageSrc) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="modal-close">&times;</span>
            <img src="${imageSrc}" alt="Preview">
        </div>
    `;
    
    modal.querySelector('.modal-close').addEventListener('click', function() {
        modal.remove();
    });
    
    modal.addEventListener('click', function(e) {
        if (e.target === this) {
            this.remove();
        }
    });
    
    return modal;
}

// Edit Row
function editRow(rowId) {
    console.log('Edit row:', rowId);
    // Navigate to edit page or open edit modal
}

// Delete Row
function deleteRow(rowId) {
    if (confirm('Are you sure you want to delete this item?')) {
        console.log('Delete row:', rowId);
        // Perform delete action
    }
}

// Initialize All
document.addEventListener('DOMContentLoaded', function() {
    initializeSidebar();
    initializeSearch();
    initializeCheckboxes();
    initializeTableSorting();
    initializeBulkActions();
    initializePagination();
    initializeFilters();
    initializeImagePreview();
});

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + F to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
        e.preventDefault();
        const searchInput = document.querySelector('.search-box input');
        if (searchInput) searchInput.focus();
    }
    
    // Escape to clear selection
    if (e.key === 'Escape') {
        const checkboxes = document.querySelectorAll('.item-checkbox');
        checkboxes.forEach(cb => cb.checked = false);
        const selectAll = document.querySelector('.select-all');
        if (selectAll) selectAll.checked = false;
        updateBulkActionsUI();
    }
});

// Add some style for the modal
if (!document.querySelector('style[data-admin-modal]')) {
    const style = document.createElement('style');
    style.setAttribute('data-admin-modal', 'true');
    style.innerHTML = `
        .modal {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }
        
        .modal-content {
            position: relative;
            max-width: 90vw;
            max-height: 90vh;
        }
        
        .modal-content img {
            width: 100%;
            height: auto;
            border-radius: 8px;
        }
        
        .modal-close {
            position: absolute;
            top: -30px;
            right: 0;
            font-size: 28px;
            color: white;
            cursor: pointer;
            user-select: none;
        }
        
        .modal-close:hover {
            color: #ccc;
        }
    `;
    document.head.appendChild(style);
}
