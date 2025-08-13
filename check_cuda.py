#!/usr/bin/env python3
"""
Script pour vérifier la configuration CUDA
"""

import torch
import whisper

def check_cuda():
    print("=== Vérification de la configuration CUDA ===\n")
    
    # Vérifier PyTorch
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA disponible: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"Version CUDA: {torch.version.cuda}")
        print(f"Nombre de GPUs: {torch.cuda.device_count()}")
        
        for i in range(torch.cuda.device_count()):
            print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
            print(f"  Mémoire totale: {torch.cuda.get_device_properties(i).total_memory / 1024**3:.1f} GB")
            print(f"  Mémoire disponible: {torch.cuda.memory_allocated(i) / 1024**3:.1f} GB")
    else:
        print("⚠️  CUDA n'est pas disponible - utilisation du CPU")
    
    print("\n=== Test de chargement du modèle Whisper ===")
    
    try:
        # Charger un petit modèle pour tester
        model = whisper.load_model("tiny", device="cuda" if torch.cuda.is_available() else "cpu")
        print(f"✅ Modèle Whisper chargé avec succès sur: {model.device}")
        
        if torch.cuda.is_available():
            print(f"✅ Utilisation de CUDA confirmée")
        else:
            print("⚠️  Utilisation du CPU (CUDA non disponible)")
            
    except Exception as e:
        print(f"❌ Erreur lors du chargement du modèle: {e}")
    
    print("\n=== Configuration recommandée ===")
    if torch.cuda.is_available():
        print("✅ Votre système est configuré pour utiliser CUDA")
        print("   Vous pouvez utiliser WHISPER_DEVICE=cuda")
    else:
        print("⚠️  CUDA n'est pas disponible")
        print("   Utilisez WHISPER_DEVICE=cpu ou installez les drivers NVIDIA")

if __name__ == "__main__":
    check_cuda()
