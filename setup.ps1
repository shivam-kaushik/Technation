# Skill Recognition Engine - Setup Script
# Run this script to verify installation and download required models

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Skill Recognition Engine - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python installation..." -ForegroundColor Yellow
python --version

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Python found" -ForegroundColor Green
Write-Host ""

# Install requirements
Write-Host "Installing Python packages..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install packages" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Packages installed" -ForegroundColor Green
Write-Host ""

# Download Sentence-BERT model
Write-Host "Downloading Sentence-BERT model (this may take a few minutes)..." -ForegroundColor Yellow
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Model download may have failed. Will retry on first run." -ForegroundColor Yellow
} else {
    Write-Host "✓ Model downloaded" -ForegroundColor Green
}

Write-Host ""

# Create output directory
Write-Host "Creating output directory..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "output" | Out-Null
Write-Host "✓ Output directory created" -ForegroundColor Green
Write-Host ""

# Verify data files
Write-Host "Verifying data files..." -ForegroundColor Yellow

$dataFiles = @(
    "data\skill_ontology.json",
    "data\ai_role_clusters.json",
    "data\microcredentials.json"
)

$allFilesExist = $true
foreach ($file in $dataFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file MISSING" -ForegroundColor Red
        $allFilesExist = $false
    }
}

if (-not $allFilesExist) {
    Write-Host ""
    Write-Host "ERROR: Some data files are missing!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run the application:" -ForegroundColor Yellow
Write-Host "  streamlit run app.py" -ForegroundColor White
Write-Host ""
Write-Host "The app will open in your default browser at:" -ForegroundColor Yellow
Write-Host "  http://localhost:8501" -ForegroundColor White
Write-Host ""
