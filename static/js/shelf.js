/*jslint
    browser: true,
    long: true
*/

/*global document, localStorage, JSON */

/* ============================================================
   SHELF PAGE UI STATE + ACCESSIBILITY LOGIC
============================================================ */

document.addEventListener("DOMContentLoaded", function () {

    /* Declare all variables at top (for JSLint compliance) */
    var savedState = JSON.parse(localStorage.getItem("shelfState") || "{}");
    var openSections;
    var scrollPositions;
    var sections;
    var positions;
    var header;

    /* ============================================================
       RESTORE UI STATE ON LOAD
    ============================================================ */
    if (savedState.openSections) {
        openSections = savedState.openSections;

        document.querySelectorAll(
            ".accordion-item"
        ).forEach(function (item, i) {

            if (openSections.includes(i)) {

                item.classList.add("open");

                header = item.querySelector(".accordion-header");

                if (header) {
                    header.setAttribute("aria-expanded", "true");
                }
            }
        });
    }

    if (savedState.scrollPositions) {
        scrollPositions = savedState.scrollPositions;

        document.querySelectorAll(
            ".shelf-row"
        ).forEach(function (row, i) {

            if (scrollPositions[i] !== undefined) {
                row.scrollLeft = scrollPositions[i];
            }
        });
    }

    /* ============================================================
       SAVE UI STATE
    ============================================================ */
    function saveState() {
        sections = [];
        positions = [];

        document.querySelectorAll(
            ".accordion-item"
        ).forEach(function (item, i) {

            if (item.classList.contains("open")) {
                sections.push(i);
            }
        });

        document.querySelectorAll(
            ".shelf-row"
        ).forEach(function (row, i) {
            positions[i] = row.scrollLeft;
        });

        localStorage.setItem(
            "shelfState",
            JSON.stringify({
                openSections: sections,
                scrollPositions: positions
            })
        );
    }

    /* ============================================================
       SAVE STATE BEFORE FORM SUBMISSION
    ============================================================ */
    document.querySelectorAll(
        ".shelf-actions form"
    ).forEach(function (form) {
        form.addEventListener("submit", function () {
            saveState();
        });
    });

    /* ============================================================
       ACCORDION LOGIC
    ============================================================ */
    document.querySelectorAll(
        ".accordion-header"
    ).forEach(function (headerEl) {

        headerEl.addEventListener("click", function () {
            var item = headerEl.closest(".accordion-item");
            var isOpen = item.classList.toggle("open");

            headerEl.setAttribute(
                "aria-expanded",
                (
                    isOpen
                    ? "true"
                    : "false"
                )
            );

            saveState();
        });
    });

    /* ============================================================
       HORIZONTAL ARROW SCROLLING
    ============================================================ */
    document.querySelectorAll(".shelf-row").forEach(function (row) {

        var wrapper = row.closest(".shelf-wrapper");
        var leftArrow = wrapper.querySelector(".scroll-left");
        var rightArrow = wrapper.querySelector(".scroll-right");
        var scrollAmount = 240;

        rightArrow.addEventListener("click", function () {
            row.scrollBy({
                behavior: "smooth",
                left: scrollAmount
            });
        });

        leftArrow.addEventListener("click", function () {
            row.scrollBy({
                behavior: "smooth",
                left: -scrollAmount
            });
        });
    });
});
