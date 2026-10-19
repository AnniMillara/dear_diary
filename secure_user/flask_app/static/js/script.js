document.addEventListener("DOMContentLoaded", () => { document.querySelectorAll(".alert").forEach((alerta) => { window.setTimeout(() => alerta.classList.add("alert-hidden"), 5000); }); });
