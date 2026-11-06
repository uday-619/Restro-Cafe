document.addEventListener('DOMContentLoaded', () => {
  const mainContainer = document.querySelector('.main-container');
  const signupLink = document.querySelector('.signup-link');
  const loginLink = document.querySelector('.login-link');

  if (signupLink && loginLink && mainContainer) {
    signupLink.addEventListener('click', (e) => {
      e.preventDefault();
      mainContainer.classList.add('active');
    });

    loginLink.addEventListener('click', (e) => {
      e.preventDefault();
      mainContainer.classList.remove('active');
    });
  }

  // Profile picture file selector filename update
  const fileInput = document.getElementById('profile_picture');
  const fileNameText = document.getElementById('file-name-text');
  if (fileInput && fileNameText) {
    fileInput.addEventListener('change', (e) => {
      if (e.target.files.length > 0) {
        fileNameText.textContent = e.target.files[0].name;
        fileNameText.style.color = '#95C11E';
      } else {
        fileNameText.textContent = 'Profile Picture';
        fileNameText.style.color = '';
      }
    });
  }
});
