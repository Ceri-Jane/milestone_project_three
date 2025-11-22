/* ============================================================
   PASSWORD VISIBILITY TOGGLE
   ------------------------------------------------------------
   - Handles the "eye" icon next to password fields.
   - Input switches between type="password" and type="text".
   - ARIA attributes update to reflect the visibility state.
   - Supports both mouse AND keyboard activation (Enter key).
   - No design/behaviour changes — only accessibility upgrades.
============================================================ */

document.querySelectorAll(".password-toggle").forEach((icon) => {
    
    // Each icon toggles visibility of the <input> inside the nearest .password-row
    icon.addEventListener("click", () => toggleVisibility(icon));

    // Keyboard accessibility: allow Enter key to toggle visibility
    icon.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            toggleVisibility(icon);
        }
    });

    /* Helper function that toggles the password visibility */
    function toggleVisibility(iconElement) {

        const wrapper = iconElement.closest(".password-row");
        const input = wrapper.querySelector("input");

        if (!input) return;

        /* ------------------------------------------------------------
           Toggle password visibility
        ------------------------------------------------------------ */
        const isHidden = input.type === "password";
        input.type = isHidden ? "text" : "password";

        /* ------------------------------------------------------------
           Accessibility improvement:
           - aria-label updates dynamically
           - aria-pressed communicates toggle state to screen readers
        ------------------------------------------------------------ */
        iconElement.setAttribute(
            "aria-label",
            isHidden ? "Hide password" : "Show password"
        );

        iconElement.setAttribute("aria-pressed", isHidden ? "true" : "false");
    }
});
