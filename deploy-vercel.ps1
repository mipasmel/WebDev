# 🚀 Script de despliegue automático a Vercel
# Autor: Miguel Pastor

Write-Host "==> Iniciando despliegue de FastAPI Scraper a Vercel..." -ForegroundColor Cyan

# 1️⃣ Ir a la carpeta del proyecto
Set-Location "$PSScriptRoot"

# 2️⃣ Crear entorno virtual (si no existe)
if (-Not (Test-Path ".venv")) {
    Write-Host "Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv .venv
}

# 3️⃣ Activar entorno
Write-Host "Activando entorno..." -ForegroundColor Yellow
.venv\Scripts\activate

# 4️⃣ Instalar dependencias
if (Test-Path "fastapi_scraper/requirements.txt") {
    Write-Host "Instalando dependencias..." -ForegroundColor Yellow
    pip install -r fastapi_scraper/requirements.txt
} else {
    Write-Host "⚠️ No se encontró el archivo requirements.txt" -ForegroundColor Red
    exit
}

# 5️⃣ Confirmar cambios en Git
Write-Host "Añadiendo cambios a Git..." -ForegroundColor Yellow
git add .
$commitMessage = Read-Host "Mensaje del commit"
git commit -m "$commitMessage"

# 6️⃣ Subir a GitHub
Write-Host "Subiendo a GitHub..." -ForegroundColor Yellow
git push origin main

# 7️⃣ Desplegar en Vercel
Write-Host "Lanzando despliegue en Vercel..." -ForegroundColor Green
vercel --prod

Write-Host "✅ Despliegue completado con éxito." -ForegroundColor Cyan