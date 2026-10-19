document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("form[data-confirmar]").forEach(function (form) {
        form.addEventListener("submit", function (event) {
            const mensaje = form.getAttribute("data-confirmar") || "¿Estás seguro?";
            if (!window.confirm(mensaje)) {
                event.preventDefault();
            }
        });
    });

    const hoy = new Date();
    const fechaLocal = new Date(hoy.getTime() - hoy.getTimezoneOffset() * 60000)
        .toISOString().slice(0, 10);
    document.querySelectorAll('input[type="date"]').forEach(function (input) {
        if (!input.max) input.max = fechaLocal;
    });
});
