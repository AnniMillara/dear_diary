document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".alert").forEach((alerta) => {
        window.setTimeout(() => alerta.style.display = "none", 5000);
    });

    const input = document.getElementById("buscador");
    const grid = document.getElementById("entradas-grid");
    const estadoVacio = document.getElementById("estado-vacio");
    const sinResultados = document.getElementById("sin-resultados");

    if (!input || !grid) return;

    let timeoutId = null;
    let requestSeq = 0;

    const crearCard = (e) => {
        const card = document.createElement("div");
        card.className = "entrada-card";

        const header = document.createElement("div");
        header.className = "entrada-header";

        const title = document.createElement("span");
        title.className = "entrada-titulo";
        title.textContent = "Entrada";
        header.appendChild(title);

        const emoji = document.createElement("span");
        emoji.className = "entrada-emoji";
        emoji.textContent = e.emoji || "📝";
        header.appendChild(emoji);

        card.appendChild(header);

        const fecha = document.createElement("div");
        fecha.className = "entrada-fecha";
        fecha.textContent = "✦ " + e.fecha_formato;
        card.appendChild(fecha);

        const acciones = document.createElement("div");
        acciones.className = "entrada-acciones";

        const btnVer = document.createElement("a");
        btnVer.href = "/entradas/detalle/" + e.id;
        btnVer.className = "btn btn-sm btn-info";
        btnVer.textContent = "Leer más";

        const btnEditar = document.createElement("a");
        btnEditar.href = "/entradas/editar/" + e.id;
        btnEditar.className = "btn btn-sm btn-warning";
        btnEditar.textContent = "Editar";

        const btnBorrar = document.createElement("a");
        btnBorrar.href = "/entradas/confirmar_eliminar/" + e.id;
        btnBorrar.className = "btn btn-sm btn-danger";
        btnBorrar.textContent = "Eliminar";

        acciones.appendChild(btnVer);
        acciones.appendChild(btnEditar);
        acciones.appendChild(btnBorrar);
        card.appendChild(acciones);

        return card;
    };

    const render = (entradas, texto) => {
        grid.innerHTML = "";
        if (entradas.length === 0) {
            grid.style.display = "none";
            if (texto) {
                estadoVacio.style.display = "none";
                sinResultados.style.display = "block";
            } else {
                sinResultados.style.display = "none";
                estadoVacio.style.display = "block";
            }
            return;
        }

        grid.style.display = "grid";
        estadoVacio.style.display = "none";
        sinResultados.style.display = "none";

        const frag = document.createDocumentFragment();
        entradas.forEach((e) => frag.appendChild(crearCard(e)));
        grid.appendChild(frag);
    };

    const buscar = async () => {
        const texto = input.value.trim();
        const mySeq = ++requestSeq;
        try {
            const resp = await fetch("/entradas/buscar_json?texto=" + encodeURIComponent(texto));
            if (mySeq !== requestSeq) return;
            if (resp.status === 401) { window.location.href = "/"; return; }
            if (!resp.ok) return;
            const data = await resp.json();
            if (mySeq !== requestSeq) return;
            render(data.entradas, texto);
        } catch (err) {
            console.error("Error:", err);
        }
    };

    input.addEventListener("input", () => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(buscar, 200);
    });
});