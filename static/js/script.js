document.addEventListener('DOMContentLoaded', function() {
  // Cached DOM references. These will be refreshed whenever the
  // form is re-rendered.
  let subscribeForm;
  let emailInput;
  let subscribeBtn;
  let formMessage;

  // Helper to (re)grab form elements and attach the submit handler
  function attachFormHandler() {
    subscribeForm = document.getElementById('subscribe-form');
    emailInput = document.getElementById('email-input');
    subscribeBtn = document.getElementById('subscribe-btn');
    formMessage = document.getElementById('form-message');

    if (subscribeForm) {
      subscribeForm.addEventListener('submit', handleSubmit);
    }
  }
  
  // Create a notification element for success/error messages
  let notificationElement = document.createElement('div');
  notificationElement.id = 'notification';
  notificationElement.className = 'fixed top-0 left-0 right-0 p-4 opacity-0 transition-opacity duration-300 flex justify-center z-50';
  notificationElement.style.pointerEvents = 'none';
  document.body.appendChild(notificationElement);

  // Initial attach of form handler
  attachFormHandler();
  
  // Add form submission handler
  function handleSubmit(e) {
    e.preventDefault();

    // Refresh references in case the form was recreated
    emailInput = document.getElementById('email-input');
    subscribeBtn = document.getElementById('subscribe-btn');
    formMessage = document.getElementById('form-message');

    formMessage.textContent = '';
    formMessage.classList.remove('text-red-500', 'text-green-500');

    const email = emailInput.value.trim();
    if (!email) {
      showMessage('Please enter your email address.', 'error');
      return;
    }
    if (!isValidEmail(email)) {
      showMessage('Please enter a valid email address.', 'error');
      return;
    }

    subscribeBtn.disabled = true;
    subscribeBtn.innerHTML = 'Subscribing...';

    const formData = new FormData(subscribeForm);

    fetch('/subscribe', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          showNotification(data.message, 'success');
          emailInput.value = '';

          const formContainer = subscribeForm.parentElement;
          const originalFormHTML = formContainer.innerHTML;

          formContainer.innerHTML = `
            <div class="text-center py-6">
              <div class="text-2xl mb-4">🎉</div>
              <h3 class="text-xl font-bold mb-3">You're in!</h3>
              <p class="mb-6">Thanks for joining TheVibeLab.ai community. We'll be in touch soon with enterprise transformation insights.</p>
            </div>
          `;

          setTimeout(() => {
            formContainer.innerHTML = originalFormHTML;
            attachFormHandler();
          }, 5000);

        } else {
          showNotification(data.message, 'error');
          showMessage(data.message, 'error');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred. Please try again later.', 'error');
        showMessage('An error occurred. Please try again later.', 'error');
      })
      .finally(() => {
        const btn = document.getElementById('subscribe-btn');
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = 'Subscribe';
        }
      });
  }
  
  // Helper function to validate email
  function isValidEmail(email) {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
  }
  
  // Helper function to show form messages
  function showMessage(message, type) {
    if (!formMessage) return;
    
    formMessage.textContent = message;
    
    if (type === 'error') {
      formMessage.classList.add('text-red-500');
      formMessage.classList.remove('text-green-500');
    } else {
      formMessage.classList.add('text-green-500');
      formMessage.classList.remove('text-red-500');
    }
  }
  
  // Helper function to show toast notifications
  function showNotification(message, type) {
    const bgColor = type === 'success' ? 'bg-green-note' : 'bg-red-300';
    
    notificationElement.innerHTML = `
      <div class="sticky-note ${type === 'success' ? 'green-note' : 'purple-note'} p-4 shadow-lg max-w-md">
        <p class="text-center">${message}</p>
      </div>
    `;
    
    // Show notification
    setTimeout(() => {
      notificationElement.style.opacity = '1';
    }, 100);
    
    // Hide notification after 3 seconds
    setTimeout(() => {
      notificationElement.style.opacity = '0';
    }, 3000);
  }
});
