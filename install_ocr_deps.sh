#!/bin/bash

# Script para instalar todas las dependencias de OCR

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║        INSTALADOR DE DEPENDENCIAS - OCR PDF to TXT                ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Detectar sistema operativo
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Sistema detectado: Linux"
    echo ""
    echo "📦 Instalando dependencias del sistema..."
    
    sudo apt-get update
    sudo apt-get install -y \
        poppler-utils \
        tesseract-ocr \
        libtesseract-dev \
        python3-pip \
        python3-dev
    
    INSTALL_STATUS=$?
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 Sistema detectado: macOS"
    echo ""
    
    # Verificar si Homebrew está instalado
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew no está instalado"
        echo "   Instala desde: https://brew.sh"
        exit 1
    fi
    
    echo "📦 Instalando dependencias con Homebrew..."
    brew install poppler tesseract
    
    INSTALL_STATUS=$?
    
else
    echo "❌ Sistema operativo no soportado: $OSTYPE"
    echo "   Soportados: Linux, macOS"
    exit 1
fi

if [ $INSTALL_STATUS -ne 0 ]; then
    echo ""
    echo "❌ Error durante la instalación de dependencias del sistema"
    exit 1
fi

echo ""
echo "✅ Dependencias del sistema instaladas"
echo ""
echo "📦 Instalando librerías Python..."
echo ""

# Instalar librerías Python
pip install --upgrade pip
pip install \
    pdfplumber \
    pdf2image \
    pytesseract \
    PyPDF2 \
    pillow

PYTHON_STATUS=$?

if [ $PYTHON_STATUS -ne 0 ]; then
    echo ""
    echo "❌ Error durante la instalación de librerías Python"
    exit 1
fi

echo ""
echo "✅ Librerías Python instaladas"
echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ INSTALACIÓN COMPLETADA                       ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 Próximo paso: ejecuta"
echo "   python3 extract_ocr.py"
echo ""
