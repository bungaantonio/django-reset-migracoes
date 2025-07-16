# Caminho para a base de dados
$dbPath = ".\db.sqlite3"

# Caminho do requirements.txt
$requirementsPath = ".\requirements.txt"

# Funcao auxiliar para pedir confirmacao robusta
function Confirmar($mensagem) {
    while ($true) {
        $resposta = Read-Host "$mensagem (s/n)"
        if ($resposta -eq 's') { return $true }
        elseif ($resposta -eq 'n') { return $false }
        else { Write-Host "Por favor, responda com 's' para sim ou 'n' para nao." }
    }
}

Write-Host "`n[1/5] Apagar base de dados SQLite..."
if (Test-Path $dbPath) {
    if (Confirmar "Deseja mesmo apagar a base de dados '$dbPath'?") {
        Remove-Item $dbPath
        Write-Host "Base de dados removida: $dbPath"
    } else {
        Write-Host "Operacao cancelada."
        exit 0
    }
} else {
    Write-Host "Base de dados nao encontrada: $dbPath"
}

Write-Host "`n[2/5] A localizar pastas de migracao..."
$migrations = Get-ChildItem -Recurse -Directory -Filter "migrations" |
    Where-Object { $_.FullName -notmatch "\\.venv\\" -and $_.FullName -notmatch "site-packages" }

if ($migrations.Count -eq 0) {
    Write-Host "Nenhuma pasta de migracao encontrada."
} else {
    Write-Host "Pastas de migracao encontradas:"
    $migrations | ForEach-Object { Write-Host " - $($_.FullName)" }
}

Write-Host "`n[3/5] A apagar ficheiros de migracao (exceto __init__.py)..."
if (Confirmar "Deseja remover os ficheiros de migracao gerados anteriormente?") {
    foreach ($folder in $migrations) {
        Get-ChildItem -Path $folder.FullName -Exclude "__init__.py" -Recurse |
            Where-Object { $_.Extension -eq ".py" -or $_.Extension -eq ".pyc" } |
            ForEach-Object {
                Write-Host "Apagando: $($_.FullName)"
                Remove-Item $_.FullName -Force
            }
    }
    Write-Host "Ficheiros de migracao apagados."
} else {
    Write-Host "Remocao de ficheiros de migracao cancelada."
}

Write-Host "`n[4/5] A aplicar novas migracoes..."
try {
    python manage.py makemigrations
    python manage.py migrate
    Write-Host "Migracoes aplicadas com sucesso."
} catch {
    Write-Host "Erro ao aplicar migracoes."
    exit 1
}

Write-Host "`n[5/5] A instalar dependencias do requirements.txt..."
if (Test-Path $requirementsPath) {
    if (Confirmar "Deseja instalar as dependencias listadas em '$requirementsPath'?") {
        try {
            pip install -r $requirementsPath
            Write-Host "Dependencias instaladas com sucesso."
        } catch {
            Write-Host "Erro ao instalar as dependencias."
            exit 1
        }
    } else {
        Write-Host "Instalacao de dependencias cancelada."
    }
} else {
    Write-Host "Ficheiro '$requirementsPath' nao encontrado. Pulando etapa."
}

Write-Host "`nProcesso concluido com sucesso."
