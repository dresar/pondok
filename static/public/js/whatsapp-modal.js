// ==================== WhatsApp Modal Functions ====================
let selectedWhatsAppContact = null;
let selectedWhatsAppTemplate = null;
let useCustomMessage = false;

function openWhatsAppModal() {
    const modal = document.getElementById('whatsapp-modal');
    if (modal) {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
        // Reset selection
        selectedWhatsAppContact = null;
        selectedWhatsAppTemplate = null;
        useCustomMessage = false;
        updateWhatsAppSendButton();
        document.getElementById('whatsapp-selected-contact').textContent = 'Belum dipilih';
        document.getElementById('whatsapp-selected-template').textContent = 'Belum dipilih';
        
        // Reset custom message
        const customInput = document.getElementById('custom-message-input');
        if (customInput) {
            customInput.value = '';
        }
        const customSection = document.getElementById('custom-message-section');
        if (customSection) {
            customSection.classList.add('hidden');
        }
        const toggleBtn = document.getElementById('toggle-custom-btn');
        if (toggleBtn) {
            toggleBtn.innerHTML = '<i class="fas fa-edit"></i><span>Tulis Pesan Sendiri</span>';
        }
        const templateList = document.getElementById('whatsapp-template-list');
        if (templateList) {
            templateList.classList.remove('hidden');
        }
        
        // Reset visual selection
        document.querySelectorAll('#whatsapp-contact-list button').forEach(btn => {
            btn.classList.remove('border-green-500', 'bg-green-50');
            btn.classList.add('border-gray-200', 'bg-gray-50');
        });
        document.querySelectorAll('#whatsapp-template-list button').forEach(btn => {
            btn.classList.remove('border-green-500', 'bg-green-50');
            btn.classList.add('border-gray-200', 'bg-white');
        });
    }
}

function closeWhatsAppModal() {
    const modal = document.getElementById('whatsapp-modal');
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
        // Reset selection
        selectedWhatsAppContact = null;
        selectedWhatsAppTemplate = null;
        useCustomMessage = false;
        
        // Reset custom message
        const customInput = document.getElementById('custom-message-input');
        if (customInput) {
            customInput.value = '';
        }
        const customSection = document.getElementById('custom-message-section');
        if (customSection) {
            customSection.classList.add('hidden');
        }
        const toggleBtn = document.getElementById('toggle-custom-btn');
        if (toggleBtn) {
            toggleBtn.innerHTML = '<i class="fas fa-edit"></i><span>Tulis Pesan Sendiri</span>';
        }
        const templateList = document.getElementById('whatsapp-template-list');
        if (templateList) {
            templateList.classList.remove('hidden');
        }
    }
}

function toggleCustomMessage() {
    const customSection = document.getElementById('custom-message-section');
    const toggleBtn = document.getElementById('toggle-custom-btn');
    const templateList = document.getElementById('whatsapp-template-list');
    
    if (customSection && toggleBtn) {
        const isHidden = customSection.classList.contains('hidden');
        
        if (isHidden) {
            // Show custom message
            customSection.classList.remove('hidden');
            if (templateList) {
                templateList.classList.add('hidden');
            }
            toggleBtn.innerHTML = '<i class="fas fa-list"></i><span>Pilih Template</span>';
            useCustomMessage = true;
            
            // Clear template selection
            selectedWhatsAppTemplate = null;
            const templateDisplay = document.getElementById('whatsapp-selected-template');
            if (templateDisplay) {
                templateDisplay.textContent = 'Pesan Custom';
            }
            document.querySelectorAll('#whatsapp-template-list button').forEach(btn => {
                btn.classList.remove('border-green-500', 'bg-green-50');
                btn.classList.add('border-gray-200', 'bg-white');
            });
        } else {
            // Show template list
            customSection.classList.add('hidden');
            if (templateList) {
                templateList.classList.remove('hidden');
            }
            toggleBtn.innerHTML = '<i class="fas fa-edit"></i><span>Tulis Pesan Sendiri</span>';
            useCustomMessage = false;
            
            // Clear custom message
            const customInput = document.getElementById('custom-message-input');
            if (customInput) {
                customInput.value = '';
            }
            
            // Reset template display
            if (!selectedWhatsAppTemplate) {
                const templateDisplay = document.getElementById('whatsapp-selected-template');
                if (templateDisplay) {
                    templateDisplay.textContent = 'Belum dipilih';
                }
            }
        }
        updateWhatsAppSendButton();
    }
}

function toggleCustomMessage() {
    const customSection = document.getElementById('custom-message-section');
    const toggleBtn = document.getElementById('toggle-custom-btn');
    const templateList = document.getElementById('whatsapp-template-list');
    
    if (customSection && toggleBtn) {
        const isHidden = customSection.classList.contains('hidden');
        
        if (isHidden) {
            // Show custom message
            customSection.classList.remove('hidden');
            if (templateList) {
                templateList.classList.add('hidden');
            }
            toggleBtn.innerHTML = '<i class="fas fa-list"></i><span>Pilih Template</span>';
            useCustomMessage = true;
            
            // Clear template selection
            selectedWhatsAppTemplate = null;
            document.getElementById('whatsapp-selected-template').textContent = 'Pesan Custom';
            document.querySelectorAll('#whatsapp-template-list button').forEach(btn => {
                btn.classList.remove('border-green-500', 'bg-green-50');
                btn.classList.add('border-gray-200', 'bg-white');
            });
        } else {
            // Show template list
            customSection.classList.add('hidden');
            if (templateList) {
                templateList.classList.remove('hidden');
            }
            toggleBtn.innerHTML = '<i class="fas fa-edit"></i><span>Tulis Pesan Sendiri</span>';
            useCustomMessage = false;
            
            // Clear custom message
            const customInput = document.getElementById('custom-message-input');
            if (customInput) {
                customInput.value = '';
            }
            
            // Reset template display
            if (!selectedWhatsAppTemplate) {
                document.getElementById('whatsapp-selected-template').textContent = 'Belum dipilih';
            }
        }
        updateWhatsAppSendButton();
    }
}

function selectWhatsAppContact(buttonElement) {
    const phoneNumber = buttonElement.getAttribute('data-contact-number');
    const contactName = buttonElement.getAttribute('data-contact-name');
    
    selectedWhatsAppContact = {
        number: phoneNumber,
        name: contactName
    };
    const contactDisplay = document.getElementById('whatsapp-selected-contact');
    if (contactDisplay) {
        contactDisplay.textContent = contactName + ' (' + phoneNumber + ')';
    }
    updateWhatsAppSendButton();
    
    // Update visual selection
    document.querySelectorAll('#whatsapp-contact-list button').forEach(btn => {
        btn.classList.remove('border-green-500', 'bg-green-50');
        btn.classList.add('border-gray-200', 'bg-gray-50');
    });
    buttonElement.classList.remove('border-gray-200', 'bg-gray-50');
    buttonElement.classList.add('border-green-500', 'bg-green-50');
}

function selectWhatsAppTemplate(buttonElement) {
    const templateId = buttonElement.getAttribute('data-template-id');
    
    // Get template data from JSON script
    const templateScript = document.querySelector(`.whatsapp-template-data[data-template-id="${templateId}"]`);
    if (!templateScript) {
        console.error('Template data not found for ID:', templateId);
        return;
    }
    
    try {
        const templateData = JSON.parse(templateScript.textContent);
        selectedWhatsAppTemplate = {
            id: templateData.id,
            name: templateData.nama,
            message: templateData.pesan
        };
        
        const templateDisplay = document.getElementById('whatsapp-selected-template');
        if (templateDisplay) {
            templateDisplay.textContent = templateData.nama;
        }
        updateWhatsAppSendButton();
        
        // Update visual selection
        document.querySelectorAll('#whatsapp-template-list button').forEach(btn => {
            btn.classList.remove('border-green-500', 'bg-green-50');
            btn.classList.add('border-gray-200', 'bg-white');
        });
        buttonElement.classList.remove('border-gray-200', 'bg-white');
        buttonElement.classList.add('border-green-500', 'bg-green-50');
    } catch (e) {
        console.error('Error parsing template data:', e);
    }
}

function updateWhatsAppSendButton() {
    const sendBtn = document.getElementById('whatsapp-send-btn');
    if (sendBtn) {
        const customInput = document.getElementById('custom-message-input');
        const hasCustomMessage = useCustomMessage && customInput && customInput.value.trim().length > 0;
        const hasTemplate = selectedWhatsAppTemplate !== null;
        
        if (selectedWhatsAppContact && (hasTemplate || hasCustomMessage)) {
            sendBtn.disabled = false;
        } else {
            sendBtn.disabled = true;
        }
    }
}

function sendWhatsAppMessage() {
    if (!selectedWhatsAppContact) {
        alert('Silakan pilih nomor tujuan terlebih dahulu!');
        return;
    }
    
    let message = '';
    
    // Check if using custom message
    if (useCustomMessage) {
        const customInput = document.getElementById('custom-message-input');
        if (customInput && customInput.value.trim().length > 0) {
            message = customInput.value.trim();
        } else {
            alert('Silakan tulis pesan atau pilih template terlebih dahulu!');
            return;
        }
    } else if (selectedWhatsAppTemplate) {
        message = selectedWhatsAppTemplate.message;
    } else {
        alert('Silakan pilih template pesan atau tulis pesan custom terlebih dahulu!');
        return;
    }
    
    // Encode message for URL
    const encodedMessage = encodeURIComponent(message);
    const phoneNumber = selectedWhatsAppContact.number.replace(/[^0-9]/g, ''); // Remove non-digits
    
    // Create WhatsApp URL
    const whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodedMessage}`;
    
    // Open WhatsApp
    window.open(whatsappUrl, '_blank');
    
    // Close modal after a short delay
    setTimeout(() => {
        closeWhatsAppModal();
    }, 300);
}

// Add event listener for custom message input
document.addEventListener('DOMContentLoaded', function() {
    const customInput = document.getElementById('custom-message-input');
    if (customInput) {
        customInput.addEventListener('input', function() {
            updateWhatsAppSendButton();
            if (this.value.trim().length > 0) {
                document.getElementById('whatsapp-selected-template').textContent = 'Pesan Custom';
            } else if (!selectedWhatsAppTemplate) {
                document.getElementById('whatsapp-selected-template').textContent = 'Belum dipilih';
            }
        });
    }
});

// Make functions globally available
window.openWhatsAppModal = openWhatsAppModal;
window.closeWhatsAppModal = closeWhatsAppModal;
window.selectWhatsAppContact = selectWhatsAppContact;
window.selectWhatsAppTemplate = selectWhatsAppTemplate;
window.sendWhatsAppMessage = sendWhatsAppMessage;
window.toggleCustomMessage = toggleCustomMessage;

// Keyboard navigation for WhatsApp modal
document.addEventListener('keydown', function(e) {
    const whatsappModal = document.getElementById('whatsapp-modal');
    if (whatsappModal && !whatsappModal.classList.contains('hidden')) {
        if (e.key === 'Escape') {
            closeWhatsAppModal();
        }
    }
});

