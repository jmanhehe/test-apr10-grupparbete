param (
    [int]$AppPort = 5000
)

Write-Host "Starting the application on port $AppPort..."

# Check if Docker is installed
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker is not installed. Please install Docker Desktop and try again."
    exit 1
}

# Check if Docker is running
try {
    docker info | Out-Null
} catch {
    Write-Error "Docker is not running. Please start Docker Desktop."
    exit 1
}

# Check if port 5432 is in use
$portUsed = Get-NetTCPConnection -LocalPort 5432 -ErrorAction SilentlyContinue
if ($portUsed) {
    Write-Error "Port 5432 is already in use. Please stop the process using it or change the port in docker-compose.yml."
    exit 1
}

# Set the environment variable for the app port
$env:APP_PORT = "$AppPort"

# Run docker compose
docker compose up --build
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Error "Docker Compose failed to start. Maybe port $AppPort was already in use?"
    Write-Host ""
    Write-Host "Usage: ./local-start.ps1 -AppPort 5001"
    exit 1
}
