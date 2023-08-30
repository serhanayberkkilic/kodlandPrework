document.addEventListener("DOMContentLoaded", function() {
    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirm-password");
    const submitButton = document.querySelector("button[type='submit']");
    const popup = document.getElementById("popup");

    // Popup'ı gizleyen fonksiyon
    function hidePopup() {
        popup.style.display = 'none';
    }

    confirmPassword.addEventListener("input", function() {
        if (password.value === confirmPassword.value) {
            confirmPassword.setCustomValidity('');
            submitButton.disabled = false;
            hidePopup(); // Popup'ı gizle
        } else {
            confirmPassword.setCustomValidity('Şifreler uyuşmuyor.');
            submitButton.disabled = true;
            popup.style.display = 'block'; // Popup'ı göster
            setTimeout(hidePopup, 3000); // 3 saniye sonra popup'ı otomatik olarak gizle
        }
    });
});
