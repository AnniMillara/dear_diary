document.addEventListener("DOMContentLoaded", () => {
    // Cerrar las alertas después de unos segundos
    document.querySelectorAll(".alert").forEach((alerta) => {
        window.setTimeout(() => alerta.style.display = "none", 5000);
    });

    const input = document.getElementById("buscador");
    const grid = document.getElementById("entradas-grid");
    const tarjetas = document.querySelectorAll(".entrada-card");
    const estadoVacio = document.getElementById("estado-vacio");
    const sinResultados = document.getElementById("sin-resultados");

    if (!input || !grid) return;

    // Filtrar las entradas mientras se escribe
    input.addEventListener("input", () => {
        const texto = input.value.toLowerCase().trim();
        let tarjetasVisibles = 0;

        tarjetas.forEach((tarjeta) => {
            const contenido = tarjeta.getAttribute("data-contenido") || "";
            const fecha = tarjeta.getAttribute("data-fecha") || "";

            // Mostrar la tarjeta si coincide con la búsqueda
            if (contenido.includes(texto) || fecha.includes(texto)) {
                tarjeta.style.display = "flex";
                tarjetasVisibles++;
            } else {
                tarjeta.style.display = "none";
            }
        });

        // Mostrar mensaje si no hay resultados
        if (tarjetasVisibles === 0 && texto !== "") {
            grid.style.display = "none";
            if (estadoVacio) estadoVacio.style.display = "none";
            if (sinResultados) sinResultados.style.display = "block";
        } else {
            grid.style.display = "grid";
            if (estadoVacio) estadoVacio.style.display = "none";
            if (sinResultados) sinResultados.style.display = "none";
        }
    });
});