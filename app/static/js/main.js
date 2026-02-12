document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".reveal");
    cards.forEach((el, i) => {
        el.style.animationDelay = `${i * 90}ms`;
    });

    const idCard = document.getElementById("interactiveIdCard");
    const flipCard = document.getElementById("flipCard");
    const flipToggle = document.getElementById("flipToggle");

    if (flipCard && flipToggle) {
        const applyFlipState = () => {
            const isFlipped = flipCard.classList.contains("is-flipped");
            flipToggle.setAttribute("aria-pressed", isFlipped ? "true" : "false");
            flipToggle.textContent = isFlipped ? "Show Front Side" : "Flip ID Card";
        };

        flipToggle.addEventListener("click", () => {
            flipCard.classList.toggle("is-flipped");
            applyFlipState();
        });

        applyFlipState();
    }

    if (!idCard) {
        return;
    }

    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (prefersReducedMotion) {
        return;
    }

    idCard.addEventListener("mousemove", (event) => {
        if (flipCard && flipCard.classList.contains("is-flipped")) {
            return;
        }

        const rect = idCard.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        const rotateY = ((x / rect.width) - 0.5) * 10;
        const rotateX = (0.5 - (y / rect.height)) * 8;

        idCard.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
    });

    idCard.addEventListener("mouseleave", () => {
        idCard.style.transform = "rotateX(0deg) rotateY(0deg)";
    });
});
