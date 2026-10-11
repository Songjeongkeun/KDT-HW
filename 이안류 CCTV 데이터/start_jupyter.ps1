$ErrorActionPreference = 'Stop'
$projectRoot = $PSScriptRoot
$pythonPath = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw 'Create .venv and install requirements.txt before starting Jupyter.'
}
Set-Location -LiteralPath $projectRoot
# Register inside this venv rather than writing a machine-specific user kernel.
& $pythonPath -m ipykernel install --sys-prefix --name riptide-cctv --display-name 'Python (.venv) - Riptide CCTV'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
# Keep token authentication enabled and bind only to this computer.
& $pythonPath -m jupyter_server --ServerApp.ip=127.0.0.1 --ServerApp.port=8888 --ServerApp.port_retries=0 --ServerApp.open_browser=False --MappingKernelManager.default_kernel_name=riptide-cctv
exit $LASTEXITCODE
