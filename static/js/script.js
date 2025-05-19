document.addEventListener('DOMContentLoaded', function() {
  // Get the form element
  const subscribeForm = document.getElementById('subscribe-form');
  const emailInput = document.getElementById('email-input');
  const subscribeBtn = document.getElementById('subscribe-btn');
  const formMessage = document.getElementById('form-message');
  
  // Add form submission handler
  if (subscribeForm) {
    subscribeForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      // Reset form message
      formMessage.textContent = '';
      formMessage.classList.remove('text-red-500', 'text-green-500');
      
      // Get email value
      const email = emailInput.value.trim();
      
      // Basic validation
      if (!email) {
        showMessage('Please enter your email address.', 'error');
        return;
      }
      
      if (!isValidEmail(email)) {
        showMessage('Please enter a valid email address.', 'error');
        return;
      }
      
      // Disable button and show loading state
      subscribeBtn.disabled = true;
      subscribeBtn.innerHTML = 'Subscribing...';
      
      // Submit form via AJAX
      const formData = new FormData(subscribeForm);
      
      fetch('/subscribe', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          showMessage(data.message, 'success');
          emailInput.value = '';
        } else {
          showMessage(data.message, 'error');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        showMessage('An error occurred. Please try again later.', 'error');
      })
      .finally(() => {
        // Reset button state
        subscribeBtn.disabled = false;
        subscribeBtn.innerHTML = 'Subscribe for free';
      });
    });
  }
  
  // Helper function to validate email
  function isValidEmail(email) {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
  }
  
  // Helper function to show form messages
  function showMessage(message, type) {
    formMessage.textContent = message;
    
    if (type === 'error') {
      formMessage.classList.add('text-red-500');
      formMessage.classList.remove('text-green-500');
    } else {
      formMessage.classList.add('text-green-500');
      formMessage.classList.remove('text-red-500');
    }
  }
  
  // Simple animation for section visibility on scroll
  const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
  };
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-in');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);
  
  document.querySelectorAll('.animate-on-scroll').forEach(section => {
    observer.observe(section);
  });
});
