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
  body.classList.toggle("burger");
});

header__menu
  .querySelectorAll("li a, li button")
  .forEach((el) =>
    el.addEventListener("click", () => body.classList.remove("burger"))
  );
