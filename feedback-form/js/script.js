document.getElementById('feedback-form').addEventListener('submit', async function(event) {
  event.preventDefault();
  
  const form = event.target;
  const formData = new FormData(form);
  const data = {};
  
  // Collect form data
  for (let [key, value] of formData.entries()) {
    if (key === 'Q7_Useful_Topics[]') {
      data['Q7_Useful_Topics'] = data['Q7_Useful_Topics'] || [];
      data['Q7_Useful_Topics'].push(value);
    } else {
      data[key] = value;
    }
  }
  
  // Convert Q7_Useful_Topics array to string
  if (data['Q7_Useful_Topics']) {
    data['Q7_Useful_Topics'] = data['Q7_Useful_Topics'].join(', ');
  }
  
  try {
    const response = await fetch('https://script.google.com/macros/s/AKfycbykn0s52Bh5pvDmvaTLorhRfqyUglzzyaHUF6OLLPqGZAR5ATw1lRlamgN9NUVmR56y/exec', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    
    if (response.ok) {
      alert('Thank you for your feedback!');
      form.reset();
    } else {
      alert('Error submitting feedback. Please try again.');
    }
  } catch (error) {
    alert('Error submitting feedback. Please try again.');
    console.error('Error:', error);
  }
});
