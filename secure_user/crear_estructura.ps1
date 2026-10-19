$root = "secure_user"
$dirs = @(
    "$root\database", "$root\models", "$root\controllers",
    "$root\templates", "$root\static", "$root\static\css", "$root\static\js"
)
New-Item -ItemType Directory -Path $root -Force | Out-Null
foreach ($dir in $dirs) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
$files = @(
    "$root\app.py", "$root\Pipfile", "$root\Pipfile.lock", "$root\.env.example",
    "$root\.gitignore", "$root\README.md", "$root\database\schema.sql",
    "$root\models\__init__.py", "$root\models\db.py", "$root\models\usuario.py",
    "$root\models\entrada.py", "$root\controllers\__init__.py",
    "$root\controllers\auth_controller.py", "$root\controllers\entrada_controller.py",
    "$root\templates\base.html", "$root\templates\login.html", "$root\templates\registro.html",
    "$root\templates\entrada_lista.html", "$root\templates\entrada_form.html",
    "$root\templates\entrada_detalle.html", "$root\templates\entrada_buscar.html",
    "$root\templates\confirmar_eliminar.html", "$root\templates\error.html",
    "$root\static\css\style.css", "$root\static\js\script.js"
)
foreach ($file in $files) { if (-not (Test-Path $file)) { New-Item -ItemType File -Path $file -Force | Out-Null } }
Write-Host "Estructura creada en ./$root"
