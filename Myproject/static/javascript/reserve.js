// reserve.js

document.addEventListener('DOMContentLoaded', () => {
  // Mark taken seats from database on page load
  if (typeof takenSeatsData !== 'undefined') {
    Object.keys(takenSeatsData).forEach(seatId => {
      const seatEl = document.querySelector(`.seat[data-id="${seatId}"]`);
      if (seatEl) {
        seatEl.classList.remove('free', 'selected');
        seatEl.classList.add('taken');
        seatEl.textContent = takenSeatsData[seatId][0].toUpperCase();
      }
    });
  }
});

document.querySelectorAll('.seat.free').forEach(seat => {
  seat.addEventListener('click', () => {
    if (seat.classList.contains('taken')) return;
    seat.classList.toggle('selected');
  });
});

document.getElementById('reserve').addEventListener('click', () => {
  const name = document.getElementById('customer').value.trim();
  const selected = document.querySelectorAll('.seat.selected');
  const msg = document.getElementById('msg');

  if (!name || selected.length === 0) {
    msg.textContent = 'Please enter your name and select at least one seat.';
    msg.style.color = 'red';
    return;
  }

  const seatIds = Array.from(selected).map(seat => seat.getAttribute('data-id'));
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  const formData = new FormData();
  formData.append('customer_name', name);
  seatIds.forEach(id => formData.append('seat_ids', id));
  formData.append('csrfmiddlewaretoken', csrfToken);

  fetch('/seat_reservation/', {
    method: 'POST',
    body: formData
  })
  .then(res => {
    if (res.status === 201) {
      msg.textContent = 'Reservations confirmed successfully!';
      msg.style.color = 'green';
      setTimeout(() => location.reload(), 1000);
    } else {
      res.text().then(text => {
        msg.textContent = text || 'Failed to confirm reservations.';
        msg.style.color = 'red';
      });
    }
  })
  .catch(err => {
    msg.textContent = 'Network error occurred. Please try again.';
    msg.style.color = 'red';
  });
});
