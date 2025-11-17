document.addEventListener("DOMContentLoaded", () => {

    /* ==============================
       RESTORE UI STATE ON LOAD
    ============================== */
    const savedState = JSON.parse(localStorage.getItem("shelfState") || "{}");

    if (savedState.openSections) {
        document.querySelectorAll(".accordion-item").forEach((item, i) => {
            if (savedState.openSections.includes(i)) {
                item.classList.add("open");
            }
        });
    }

    if (savedState.scrollPositions) {
        document.querySelectorAll(".shelf-row").forEach((row, i) => {
            if (savedState.scrollPositions[i] !== undefined) {
                row.scrollLeft = savedState.scrollPositions[i];
            }
        });
    }

    /* ==============================
       SAVE UI STATE BEFORE ACTIONS
    ============================== */
    function saveState() {
        const openSections = [];
        document.querySelectorAll(".accordion-item").forEach((item, i) => {
            if (item.classList.contains("open")) openSections.push(i);
        });

        const scrollPositions = [];
        document.querySelectorAll(".shelf-row").forEach((row, i) => {
            scrollPositions[i] = row.scrollLeft;
        });

        localStorage.setItem("shelfState", JSON.stringify({
            openSections,
            scrollPositions
        }));
    }

    /* ==============================
       SPOT FIX — BEFORE ANY FORM ACTION
    ============================== */
    document.querySelectorAll(".shelf-actions form").forEach(form => {
        form.addEventListener("submit", () => {
            saveState(); // Save state before Django processes the change
        });
    });

    /* ==============================
       ACCORDION CLICK LOGIC
    ============================== */
    document.querySelectorAll(".accordion-header").forEach(header => {
        header.addEventListener("click", () => {
            header.closest(".accordion-item").classList.toggle("open");
            saveState(); // Keep state updated
        });
    });

    /* ==============================
       ARROW SCROLLING
    ============================== */
    document.querySelectorAll(".shelf-row").forEach((row) => {
        const wrapper = row.closest(".shelf-wrapper");
        const leftArrow = wrapper.querySelector(".scroll-left");
        const rightArrow = wrapper.querySelector(".scroll-right");

        const scrollAmount = 240;

        rightArrow.addEventListener("click", () => {
            row.scrollBy({ left: scrollAmount, behavior: "smooth" });
        });

        leftArrow.addEventListener("click", () => {
            row.scrollBy({ left: -scrollAmount, behavior: "smooth" });
        });
    });

});
