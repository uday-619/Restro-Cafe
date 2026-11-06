var crsr = document.querySelector("#cursor");
var blu = document.querySelector("#cursor-blu");

// Set initial centering offsets using GSAP to prevent inline transform overrides
gsap.set(crsr, { xPercent: -50, yPercent: -50 });
gsap.set(blu, { xPercent: -50, yPercent: -50 });

// Use gsap.quickTo for ultra-smooth and performant cursor tracking
var crsrX = gsap.quickTo(crsr, "x", { duration: 0, ease: "power3.out" });
var crsrY = gsap.quickTo(crsr, "y", { duration: 0, ease: "power3.out" });
var bluX = gsap.quickTo(blu, "x", { duration: 0.4, ease: "power3.out" });
var bluY = gsap.quickTo(blu, "y", { duration: 0.4, ease: "power3.out" });

document.addEventListener("mousemove", function (dets) {
  crsrX(dets.clientX);
  crsrY(dets.clientY);
  bluX(dets.clientX);
  bluY(dets.clientY);
});

var h4all = document.querySelectorAll("#nav h4, #nav img, #page1 #arrow, #scroller h4, .card, .elem, #footer img, #f2 h3, #f3 h3, #f4 h4");
h4all.forEach(function (elem) {
  elem.addEventListener("mouseenter", function () {
    gsap.to(crsr, {
      scale: 3,
      xPercent: -50,
      yPercent: -50,
      border: "1px solid #fff",
      backgroundColor: "transparent",
      duration: 0.2
    });
  });
  elem.addEventListener("mouseleave", function () {
    gsap.to(crsr, {
      scale: 1,
      xPercent: -50,
      yPercent: -50,
      border: "0px solid #95C11E",
      backgroundColor: "#95C11E",
      duration: 0.2
    });
  });
});

gsap.to("#nav", {
  backgroundColor: "#000",
  duration: 0.5,
  height: "110px",
  scrollTrigger: {
    trigger: "#nav",
    scroller: "body",
    // markers:true,
    start: "top -10%",
    end: "top -11%",
    scrub: 1,
  },
});

gsap.to("#main", {
  backgroundColor: "#000",
  scrollTrigger: {
    trigger: "#main",
    scroller: "body",
    // markers: true,
    start: "top -25%",
    end: "top -70%",
    scrub: 2,
  },
});

gsap.from("#about-us img,#about-us-in", {
  y: 90,
  opacity: 0,
  duration: 1,
  scrollTrigger: {
    trigger: "#about-us",
    scroller: "body",
    // markers:true,
    start: "top 70%",
    end: "top 65%",
    scrub: 1,
  },
});
gsap.from(".card", {
  scale: 0.8,
  // opacity:0,
  duration: 1,
  stagger: 0.1,
  scrollTrigger: {
    trigger: ".card",
    scroller: "body",
    // markers:false,
    start: "top 70%",
    end: "top 65%",
    scrub: 1,
  },
});
gsap.from("#colon1", {
  y: -70,
  x: -70,
  scrollTrigger: {
    trigger: "#colon1",
    scroller: "body",
    // markers:true,
    start: "top 55%",
    end: "top 45%",
    scrub: 4,
  },
});
gsap.from("#colon2", {
  y: 70,
  x: 70,
  scrollTrigger: {
    trigger: "#colon1",
    scroller: "body",
    // markers:true,
    start: "top 55%",
    end: "top 45%",
    scrub: 4,
  },
});
gsap.from("#page4 h1", {
  y: 50,
  scrollTrigger: {
    trigger: "#page4 h1",
    scroller: "body",
    // markers:true,
    start: "top 75%",
    end: "top 70%",
    scrub: 3,
  },
});

document.querySelector("#arrow").addEventListener("click", function () {
  document.querySelector("#page2").scrollIntoView({ behavior: "smooth" });
});
