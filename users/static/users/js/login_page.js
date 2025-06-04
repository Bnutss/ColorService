function togglePassword() {
    const passwordInput = document.getElementById('id_password');
    const passwordEye = document.getElementById('password-eye');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        passwordEye.classList.remove('fa-eye');
        passwordEye.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        passwordEye.classList.remove('fa-eye-slash');
        passwordEye.classList.add('fa-eye');
    }
}

document.querySelector('.btn-submit').addEventListener('click', function (e) {
    const ripple = this.querySelector('.btn-ripple');
    const rect = this.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;

    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    ripple.classList.add('ripple-animation');

    setTimeout(() => {
        ripple.classList.remove('ripple-animation');
    }, 600);
});

document.querySelector('.login-form').addEventListener('submit', function (e) {
    const button = this.querySelector('.btn-submit');
    const overlay = document.querySelector('.overlay');

    // Предотвращаем повторную отправку, если кнопка уже в состоянии загрузки
    if (button.classList.contains('loading')) {
        e.preventDefault();
        return;
    }

    // Активируем состояние загрузки
    button.classList.add('loading');
    overlay.classList.add('active');
});