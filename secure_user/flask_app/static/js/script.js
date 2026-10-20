document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".alert").forEach((alerta) => {
        window.setTimeout(() => alerta.style.display = "none", 5000);
    });

    const input = document.getElementById("buscador");
    const grid = document.getElementById("entradas-grid");
    const estadoVacio = document.getElementById("estado-vacio");
    const sinResultados = document.getElementById("sin-resultados");
    const form = input ? input.closest("form") : null;

    if (!input || !grid) return;

    if (form) {
        form.addEventListener("submit", (e) => e.preventDefault());
    }

    let timeoutId = null;

    const filtrar = () => {
        const texto = input.value.trim().toLowerCase();
        const tarjetas = grid.querySelectorAll(".entrada-card");
        let visibles = 0;

        tarjetas.forEach((tarjeta) => {
            // Buscamos en el texto completo de la tarjeta
            const contenido = tarjeta.textContent.toLowerCase();
            if (contenido.includes(texto)) {
                tarjeta.style.display = "";
                visibles++;
            } else {
                tarjeta.style.display = "none";
            }
        });

        if (tarjetas.length === 0) {
            grid.style.display = "none";
            estadoVacio.style.display = "block";
            sinResultados.style.display = "none";
            return;
        }

        if (visibles === 0) {
            grid.style.display = "none";
            estadoVacio.style.display = "none";
            sinResultados.style.display = "block";
        } else {
            grid.style.display = "grid";
            estadoVacio.style.display = "none";
            sinResultados.style.display = "none";
        }
    };

    input.addEventListener("input", () => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(filtrar, 200);
    });

    if (input.value.trim() !== "") {
        filtrar();
    }
});