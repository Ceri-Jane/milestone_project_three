/* ============================================================
   PASSWORD VISIBILITY TOGGLE
   ------------------------------------------------------------
   - This script handles the "eye" icon next to password fields.
   - The input switches between type="password" and type="text".
   - ARIA attributes are updated so screen readers know the state.
   - No design or behaviour changes — only accessibility upgrades.
============================================================ */

document.querySelectorAll(".password-toggle").forEach((icon) => {
    
    // Each icon toggles visibility of the <input> inside the nearest .password-row
    icon.addEventListener("click", () => {

        const wrapper = icon.closest(".password-row");
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
           This is essential for low-vision users and screen reader users.
        ------------------------------------------------------------ */
        icon.setAttribute(
            "aria-label",
            isHidden ? "Hide password" : "Show password"
        );

        icon.setAttribute("aria-pressed", isHidden ? "true" : "false");
    });
});
