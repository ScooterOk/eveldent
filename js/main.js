import "../styles/global.scss";

// document.querySelector("#app").innerHTML = `
//   <div>
//     <a href="https://vitejs.dev" target="_blank">
//       <img src="${viteLogo}" class="logo" alt="Vite logo" />
//     </a>
//     <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank">
//       <img src="${javascriptLogo}" class="logo vanilla" alt="JavaScript logo" />
//     </a>
//     <h1>Hello Vite!</h1>
//     <div class="card">
//       <button id="counter" type="button"></button>
//     </div>
//     <p class="read-the-docs">
//       Click on the Vite logo to learn more
//     </p>
//   </div>
// `;

const body = document.querySelector("body");
const header = document.querySelector("header.header");
const headerBurger = document.querySelector("#header__burger");
const header__menu = document.querySelector("#header__menu");

window.addEventListener("scroll", () => {
  const top = window.scrollY;
  const isFixed = header.classList.contains("fixed");
  if (top > 32 && !isFixed) {
    header.classList.add("fixed");
  } else if (top <= 32 && isFixed) {
    header.classList.remove("fixed");
  }
});

headerBurger.addEventListener("click", () => {
  const isOpen = body.classList.toggle("burger");
  headerBurger.setAttribute("aria-expanded", isOpen ? "true" : "false");
  headerBurger.setAttribute(
    "aria-label",
    isOpen ? "Закрити меню навігації" : "Відкрити меню навігації"
  );
});

header__menu
  .querySelectorAll("li a, li button")
  .forEach((el) =>
    el.addEventListener("click", () => {
      body.classList.remove("burger");
      headerBurger.setAttribute("aria-expanded", "false");
      headerBurger.setAttribute("aria-label", "Відкрити меню навігації");
    })
  );

// --- REVIEWS CAROUSEL (Embla) ---
import EmblaCarousel from "embla-carousel";

const emblaNode = document.querySelector(".reviews__embla .embla__viewport");
if (emblaNode) {
  const prevBtn = document.querySelector(".reviews__arrow--prev");
  const nextBtn = document.querySelector(".reviews__arrow--next");
  const dotsNode = document.querySelector(".reviews__dots");

  const emblaApi = EmblaCarousel(emblaNode, {
    loop: false,
    align: "start",
    slidesToScroll: 1,
    containScroll: "trimSnaps",
  });

  const updateDotsAndArrows = () => {
    if (prevBtn) prevBtn.disabled = !emblaApi.canScrollPrev();
    if (nextBtn) nextBtn.disabled = !emblaApi.canScrollNext();

    if (dotsNode) {
      const selected = emblaApi.selectedScrollSnap();
      const dotNodes = dotsNode.querySelectorAll(".reviews__dot");
      dotNodes.forEach((dot, idx) => {
        const isActive = idx === selected;
        dot.classList.toggle("is-active", isActive);
        dot.setAttribute("aria-current", isActive ? "true" : "false");
      });
    }
  };

  const setupDots = () => {
    if (!dotsNode) return;
    dotsNode.innerHTML = "";
    const slideSnapList = emblaApi.scrollSnapList();
    slideSnapList.forEach((_, idx) => {
      const dot = document.createElement("button");
      dot.classList.add("reviews__dot");
      dot.type = "button";
      dot.setAttribute("aria-label", `Перейти до відгуку ${idx + 1}`);
      dot.addEventListener("click", () => emblaApi.scrollTo(idx));
      dotsNode.appendChild(dot);
    });
  };

  setupDots();
  updateDotsAndArrows();

  if (prevBtn) prevBtn.addEventListener("click", () => emblaApi.scrollPrev());
  if (nextBtn) nextBtn.addEventListener("click", () => emblaApi.scrollNext());

  emblaApi.on("select", updateDotsAndArrows);
  emblaApi.on("reInit", () => {
    setupDots();
    updateDotsAndArrows();
  });
}
