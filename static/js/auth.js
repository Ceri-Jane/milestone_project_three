/*global document */

/* ============================================================
   PASSWORD VISIBILITY TOGGLE
============================================================ */

/**
 * Toggles the visibility of the password field.
 * @param {HTMLElement} iconElement
 */
function toggleVisibility(iconElement) {
    var wrapper;
    var input;
    var isHidden;

    wrapper = iconElement.closest(".password-row");
    input = wrapper.querySelector("input");

    if (!input) {
        return;
    }

    isHidden = input.type === "password";

    input.type = (
        isHidden
        ? "text"
        : "password"
    );

    iconElement.setAttribute(
        "aria-label",
        (
            isHidden
            ? "Hide password"
            : "Show password"
        )
    );

    iconElement.setAttribute(
        "aria-pressed",
        (
            isHidden
            ? "true"
            : "false"
        )
    );
}

document.querySelectorAll(".password-toggle").forEach(function (icon) {
    icon.addEventListener("click", function () {
        toggleVisibility(icon);
    });

    icon.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            toggleVisibility(icon);
        }
    });
});
