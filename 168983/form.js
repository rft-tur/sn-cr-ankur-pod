document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('eventForm');
    const errorMessage = document.getElementById('errorMessage');
    const errorText = document.getElementById('errorText');
    const successMessage = document.getElementById('successMessage');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        errorMessage.style.display = 'none';
        successMessage.style.display = 'none';

        const name = document.getElementById('name').value.trim();
        const phone = document.getElementById('phone').value.trim();
        const description = document.getElementById('description').value.trim();
        const mediaFiles = document.getElementById('media').files;

        // Validation
        let errors = [];
        if (name === '') {
            errors.push('Please enter your full name.');
        }
        if (phone === '') {
            errors.push('Please enter your contact phone number.');
        } else if (!isValidPhone(phone)) {
            errors.push('Please enter a valid phone number.');
        }
        if (description === '') {
            errors.push('Please provide an event description.');
        }
        if (mediaFiles.length === 0) {
            errors.push('Please upload at least one media file.');
        }
        if (errors.length > 0) {
            showError(errors.join(' '));
        } else {
            showSuccess();
            setTimeout(() => {
                form.submit();
            }, 1000);
        }
    });

    function isValidPhone(phone) {
        const phoneRegex = /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/;
        return phoneRegex.test(phone);
    }

    function showError(message) {
        errorText.textContent = message;
        errorMessage.style.display = 'block';
        errorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    function showSuccess() {
        successMessage.style.display = 'block';
        successMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
});