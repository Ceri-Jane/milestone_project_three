document.addEventListener("DOMContentLoaded", () => {

    /* ============================================================
       RESTORE UI STATE ON LOAD
       ------------------------------------------------------------
       The shelf page remembers:
       - which accordion sections were open, and
       - each shelf-row's horizontal scroll position

       This helps users (especially keyboard + screen reader users)
       continue where they left off after an action, instead of being
       thrown back to the top of the page.
    ============================================================ */
    const savedState = JSON.parse(localStorage.getItem("shelfState") || "{}");

    if (savedState.openSections) {
        document.querySelectorAll(".accordion-item").forEach((item, i) => {
            if (savedState.openSections.includes(i)) {
                item.classList.add("open");

                // Accessibility: ensure ARIA reflects restored open state
                const header = item.querySelector(".accordion-header");
                if (header) header.setAttribute("aria-expanded", "true");
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

    /* ============================================================
       SAVE UI STATE BEFORE ACTIONS
       ------------------------------------------------------------
       This function collects:
       - all open accordion indexes
       - all horizontal scroll positions

       Then it serialises them into localStorage.
       Called before Django redirects the page (form submissions).
    ============================================================ */
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

    /* ============================================================
       SPOT FIX — BEFORE ANY FORM ACTION
       ------------------------------------------------------------
       All buttons inside shelf cards lead to Django form submissions:
       - move between shelves
       - remove movie
       - set thumbs up/down

       We MUST save UI state right before the form submits so that
       when the page reloads, the user ends up exactly where they were.
    ============================================================ */
    document.querySelectorAll(".shelf-actions form").forEach(form => {
        form.addEventListener("submit", () => {
            saveState();
        });
    });

    /* ============================================================
       ACCORDION CLICK LOGIC (Custom accordion system)
       ------------------------------------------------------------
       This accordion is built manually (not Bootstrap).
       We toggle a CSS class "open" on click.

       Accessibility:
       - Update aria-expanded so screen readers know the state
       - The content sections already have unique IDs
    ============================================================ */
    document.querySelectorAll(".accordion-header").forEach(header => {
        header.addEventListener("click", () => {

            const item = header.closest(".accordion-item");
            const isOpen = item.classList.toggle("open");

            // Accessibility: inform assistive tech of expanded/collapsed state
            header.setAttribute("aria-expanded", isOpen ? "true" : "false");

            saveState();
        });
    });

    /* ============================================================
       ARROW SCROLLING
       ------------------------------------------------------------
       Each shelf section has:
       - A horizontally scrollable shelf-row
       - Left + right arrow buttons for accessibility

       Users on keyboards or with motor impairments get easy
       horizontal navigation without needing to drag-scroll.
    ============================================================ */
    document.querySelectorAll(".shelf-row").forEach((row) => {

        const wrapper = row.closest(".shelf-wrapper");
        const leftArrow = wrapper.querySelector(".scroll-left");
        const rightArrow = wrapper.querySelector(".scroll-right");

        const scrollAmount = 240; // consistent jump movement

        rightArrow.addEventListener("click", () => {
            row.scrollBy({ left: scrollAmount, behavior: "smooth" });
        });

        leftArrow.addEventListener("click", () => {
            row.scrollBy({ left: -scrollAmount, behavior: "smooth" });
        });
    });

});
