/**
 * Global Notification System untuk Admin Panel
 * 
 * Fungsi ini menyediakan helper untuk menampilkan notifikasi toast di pojok kanan atas
 * 
 * Usage:
 * - showNotification('success', 'Data berhasil disimpan!')
 * - showNotification('error', 'Terjadi kesalahan!', 7000)
 * - showNotification('warning', 'Perhatian!')
 * - showNotification('info', 'Informasi penting')
 * 
 * Atau menggunakan Custom Event:
 * - document.dispatchEvent(new CustomEvent('showNotification', {
 *     detail: { type: 'success', message: 'Berhasil!', duration: 5000 }
 *   }))
 */

// Fungsi sudah tersedia secara global dari base.html
// File ini hanya untuk dokumentasi dan helper tambahan

// Helper untuk notifikasi CRUD
const NotificationHelper = {
    // Success notifications
    success: function(message, duration = 5000) {
        if (typeof window.showNotification === 'function') {
            return window.showNotification('success', message, duration);
        }
    },
    
    // Error notifications
    error: function(message, duration = 7000) {
        if (typeof window.showNotification === 'function') {
            return window.showNotification('error', message, duration);
        }
    },
    
    // Warning notifications
    warning: function(message, duration = 6000) {
        if (typeof window.showNotification === 'function') {
            return window.showNotification('warning', message, duration);
        }
    },
    
    // Info notifications
    info: function(message, duration = 5000) {
        if (typeof window.showNotification === 'function') {
            return window.showNotification('info', message, duration);
        }
    },
    
    // CRUD specific helpers
    created: function(itemName = 'Data') {
        return this.success(`${itemName} berhasil ditambahkan!`);
    },
    
    updated: function(itemName = 'Data') {
        return this.success(`${itemName} berhasil diperbarui!`);
    },
    
    deleted: function(itemName = 'Data') {
        return this.success(`${itemName} berhasil dihapus!`);
    },
    
    saved: function(itemName = 'Data') {
        return this.success(`${itemName} berhasil disimpan!`);
    },
    
    errorSave: function(itemName = 'Data') {
        return this.error(`Gagal menyimpan ${itemName}. Silakan coba lagi.`);
    },
    
    errorDelete: function(itemName = 'Data') {
        return this.error(`Gagal menghapus ${itemName}. Silakan coba lagi.`);
    },
    
    errorLoad: function(itemName = 'Data') {
        return this.error(`Gagal memuat ${itemName}. Silakan refresh halaman.`);
    },
    
    confirmDelete: function(itemName = 'Data') {
        return this.warning(`Apakah Anda yakin ingin menghapus ${itemName}?`);
    }
};

// Export untuk penggunaan global
if (typeof window !== 'undefined') {
    window.NotificationHelper = NotificationHelper;
}

