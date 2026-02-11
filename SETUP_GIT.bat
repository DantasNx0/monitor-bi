@echo off
echo ====================================================
echo        CONFIGURANDO GIT E REPOSITORIO
echo ====================================================
echo.

echo 1. Configurando usuario e email...
git config --global user.name "Paulo Eduardo"
git config --global user.email "pauloeduardobr124@gmail.com"

echo 2. Inicializando repositorio...
git init

echo 3. Adicionando arquivos...
git add .

echo 4. Criando primeiro commit...
git commit -m "Primeira versao do monitor de BI"

echo.
echo ====================================================
echo        PRONTO! AGORA SIGA OS PASSOS NO GITHUB
echo ====================================================
echo.
echo 1. Crie um "New Repository" no GitHub.
echo 2. Copie os comandos para "push an existing repository".
echo    (Geralmente sao: git remote add origin ... e git push ...)
echo.
pause
