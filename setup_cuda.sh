#!/bin/bash

echo "=== Configuration CUDA pour Whisper AI ==="
echo ""

# Vérifier si nvidia-smi est disponible
if command -v nvidia-smi &> /dev/null; then
    echo "✅ NVIDIA GPU détectée"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits
    echo ""
else
    echo "⚠️  NVIDIA GPU non détectée ou drivers non installés"
    echo "   Installez les drivers NVIDIA: https://www.nvidia.com/Download/index.aspx"
    exit 1
fi

# Vérifier si Docker est installé
if command -v docker &> /dev/null; then
    echo "✅ Docker installé"
    
    # Vérifier si nvidia-docker est configuré
    if docker run --rm --gpus all nvidia/cuda:12.1-base-ubuntu22.04 nvidia-smi &> /dev/null; then
        echo "✅ NVIDIA Docker Runtime configuré"
    else
        echo "⚠️  NVIDIA Docker Runtime non configuré"
        echo "   Installez nvidia-docker: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html"
    fi
else
    echo "⚠️  Docker non installé"
    echo "   Installez Docker: https://docs.docker.com/get-docker/"
fi

echo ""
echo "=== Installation des dépendances Python ==="

# Créer l'environnement virtuel si nécessaire
if [ ! -d ".venv" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv .venv
fi

# Activer l'environnement virtuel
source .venv/bin/activate

# Installer les dépendances
echo "Installation de PyTorch avec CUDA..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "=== Test de la configuration ==="
python check_cuda.py

echo ""
echo "=== Configuration terminée ==="
echo "Pour lancer l'application:"
echo "  source .venv/bin/activate"
echo "  export WHISPER_DEVICE=cuda"
echo "  flask run --host 0.0.0.0 --port 8000"
echo ""
echo "Ou avec Docker:"
echo "  docker compose up --build"
