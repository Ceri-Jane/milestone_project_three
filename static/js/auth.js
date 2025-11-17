document.querySelectorAll(".password-toggle").forEach((icon) => {
    icon.addEventListener("click", () => {
        const wrapper = icon.closest(".password-row");
        const input = wrapper.querySelector("input");

        if (!input) return;

        input.type = input.type === "password" ? "text" : "password";
    });
});
