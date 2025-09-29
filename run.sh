#!/bin/bash
# Script de lancement rapide
echo "🚀 Lancement Claire-IA..."
source venv/bin/activate
streamlit run app/interface.py --server.port 8501 --server.address 0.0.0.0
