document.addEventListener('DOMContentLoaded', () => {
  const themeToggleBtn = document.getElementById('theme-toggle');
  const darkIcon = document.getElementById('theme-toggle-dark-icon');
  const lightIcon = document.getElementById('theme-toggle-light-icon');

  if (!themeToggleBtn) return;

  // Установка правильной иконки при загрузке
  if (document.documentElement.classList.contains('dark')) {
    lightIcon.classList.remove('hidden');
  } else {
    darkIcon.classList.remove('hidden');
  }

  themeToggleBtn.addEventListener('click', function () {
    darkIcon.classList.toggle('hidden');
    lightIcon.classList.toggle('hidden');

    if (document.documentElement.classList.contains('dark')) {
      // Light
      document.documentElement.classList.remove('dark');
      document.documentElement.setAttribute('data-theme', 'light');
      localStorage.setItem('theme', 'light');
    } else {
      // Dark
      document.documentElement.classList.add('dark');
      document.documentElement.setAttribute('data-theme', 'dark');
      localStorage.setItem('theme', 'dark');
    }
  });
});
