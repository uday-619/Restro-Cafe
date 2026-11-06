/* ==== Custom blob cursor  ==== */
const cursor = document.getElementById("cursor");
const trail  = document.getElementById("cursor-trail");
let tx = 0, ty = 0;

document.addEventListener("mousemove", e => {
  cursor.style.left = e.clientX + "px";
  cursor.style.top  = e.clientY + "px";
  tx = e.clientX; ty = e.clientY;
});

function animateTrail(){
  const rect = trail.getBoundingClientRect();
  const cx = rect.left + rect.width / 2;
  const cy = rect.top  + rect.height / 2;

  trail.style.left = cx + (tx - cx) * 0.08 + "px";
  trail.style.top  = cy + (ty - cy) * 0.08 + "px";
  requestAnimationFrame(animateTrail);
}
animateTrail();

/* ==== View‑image modal ==== */
document.querySelectorAll(".view-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const img = btn.closest(".food-item").getAttribute("data-img");
    document.getElementById("modal-img").src = img;
    document.getElementById("image-modal").style.display = "flex";
  });
});
const modal = document.getElementById("image-modal");
document.getElementById("close-modal").onclick = () => (modal.style.display = "none");
modal.onclick = e => { if (e.target === modal) modal.style.display = "none"; };

/* ==== AJAX Order Handler ==== */
document.querySelectorAll(".order-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const foodItem = btn.closest(".food-item");
    const itemId = foodItem.getAttribute("data-id");
    const csrfTokenEl = document.querySelector('[name=csrfmiddlewaretoken]');
    
    if (!csrfTokenEl) {
      alert("System security error: CSRF token not found.");
      return;
    }

    const csrfToken = csrfTokenEl.value;
    const formData = new FormData();
    formData.append('item_id', itemId);
    formData.append('csrfmiddlewaretoken', csrfToken);

    fetch('/menu/', {
      method: 'POST',
      body: formData
    })
    .then(res => {
      if (res.status === 201) {
        alert("Added to order successfully!");
        location.reload(); // Refresh to update order logs
      } else if (res.status === 401) {
        alert("Please log in first to order items.");
      } else {
        res.text().then(text => alert(text || "Failed to place order."));
      }
    })
    .catch(err => {
      alert("Network error. Please try again.");
    });
  });
});
