/* simple form handler (demo only) */
document.getElementById("contactForm").addEventListener("submit", e => {
  e.preventDefault();
  document.getElementById("status").textContent =
    "Thanks! Your message has been sent.";
  e.target.reset();
});

/* glow on map hover (extra effect) */
const mapBox = document.getElementById("mapBox");
mapBox.addEventListener("mouseenter", ()=> mapBox.style.boxShadow = "0 0 25px rgba(0,114,255,.6)");
mapBox.addEventListener("mouseleave", ()=> mapBox.style.boxShadow = "none");
