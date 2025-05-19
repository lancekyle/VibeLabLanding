document.addEventListener('DOMContentLoaded', function() {
  // Get the form element
  const subscribeForm = document.getElementById('subscribe-form');
  const emailInput = document.getElementById('email-input');
  const subscribeBtn = document.getElementById('subscribe-btn');
  const formMessage = document.getElementById('form-message');
  
  // Create a notification element for success/error messages
  let notificationElement = document.createElement('div');
  notificationElement.id = 'notification';
  notificationElement.className = 'fixed top-0 left-0 right-0 p-4 opacity-0 transition-opacity duration-300 flex justify-center z-50';
  notificationElement.style.pointerEvents = 'none';
  document.body.appendChild(notificationElement);
  
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
          // Show success notification
          showNotification(data.message, 'success');
          emailInput.value = '';
          
          // Show a celebratory message in the form area
          const formContainer = subscribeForm.parentElement;
          const originalFormHTML = formContainer.innerHTML;
          
          formContainer.innerHTML = `
            <div class="text-center py-6">
              <div class="text-2xl mb-4">🎉</div>
              <h3 class="text-xl font-bold mb-3">You're in!</h3>
              <p class="mb-6">Thanks for joining TheVibeLab.ai community. We'll be in touch soon with enterprise transformation insights.</p>
            </div>
          `;
          
          // Optional: Reset form after a timeout
          setTimeout(() => {
            formContainer.innerHTML = originalFormHTML;
            
            // Re-attach event listeners
            const newForm = document.getElementById('subscribe-form');
            if (newForm) {
              const newEmailInput = document.getElementById('email-input');
              const newSubscribeBtn = document.getElementById('subscribe-btn');
              const newFormMessage = document.getElementById('form-message');
              
              // Re-attach event listeners if needed
              newForm.addEventListener('submit', subscribeForm.onsubmit);
            }
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
        // Reset button state if the form is still visible
        if (!subscribeBtn.disabled) return;
        subscribeBtn.disabled = false;
        subscribeBtn.innerHTML = 'Subscribe';
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
