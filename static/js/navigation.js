console.log("Navigation module loaded.");
const navigationLinks = document.querySelectorAll('nav a[href^="#"]');

navigationLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
        event.preventDefault();

        const targetId = link.getAttribute("href");
        const targetSection = document.querySelector(targetId);

        if (targetSection) {
            targetSection.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        }
    });
});