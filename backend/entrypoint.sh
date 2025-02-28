#!/bin/sh

echo -e "\033[1;32mAplicando migrações do banco de dados...\033[0m"
python manage.py migrate

if [ $? -eq 0 ]; then
    echo -e "\033[1;32mMigrações aplicadas.\033[0m"
else
    echo -e "\033[1;31mErro ao aplicar migrações.\033[0m"
    exit 1
fi

echo -e "\033[1;32mCarregando dados de iniciais de áreas (init_areas.json)...\033[0m"
python manage.py loaddata init_areas.json

if [ $? -eq 0 ]; then
    echo -e "\033[1;32mDados iniciais de áreas carregados.\033[0m"
else
    echo -e "\033[1;31mErro ao carregar dados iniciais de áreas. Verifique o arquivo init_areas.json.\033[0m"
    exit 1
fi

echo -e "\033[1;32mIniciando o servidor Django...\033[0m"
exec python manage.py runserver 0.0.0.0:8000