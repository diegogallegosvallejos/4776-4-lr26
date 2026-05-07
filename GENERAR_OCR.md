# 🚀 Cómo Generar OCR/TXT para Todos los PDFs

He creado **2 formas** de convertir automáticamente tus PDFs a archivos TXT con OCR:

---

## ✅ **Opción 1: Script Python (RECOMENDADO - Ejecutar Ahora)**

### Instalación de dependencias

```bash
# En Linux/macOS:
sudo apt-get install poppler-utils tesseract-ocr libtesseract-dev

# En macOS con Homebrew:
brew install poppler tesseract

# Instalar librerías Python:
pip install pdf2image pytesseract PyPDF2 pdfplumber pillow
```

### Ejecutar el script

```bash
python3 extract_ocr.py
```

**¿Qué hace?**
- ✅ Busca todos los PDFs en el repositorio
- ✅ Extrae texto con PDFPlumber (para PDFs nativos)
- ✅ Aplica OCR con Tesseract (para escaneos)
- ✅ Genera carpeta `OCR_EXTRACCIONES/` con estructura idéntica
- ✅ Crea índice (`INDEX.md`) y buscador (`BUSCADOR.md`)
- ✅ Genera resumen en JSON

**Resultado:**
```
OCR_EXTRACCIONES/
├── Evaluacion_Contractual/
│   ├── Evaluacion Contractual/
│   │   ├── CRS Allende.txt
│   │   └── H La Florida.txt
├── Evaluacion_Financiera/
│   ├── Evaluacion Financiera/
│   │   ├── Balance Firmado 2023 Layner.txt
│   │   ├── Balance Firmado 2024 Layner.txt
│   │   └── ... (13 más)
├── Experiencia_del_Oferente/
│   └── ... (18 archivos TXT)
├── Ofertas_*/
│   └── ... (31 archivos TXT)
├── INDEX.md          ← Índice completo
├── BUSCADOR.md       ← Guía de búsqueda
└── resumen.json      ← Estadísticas
```

---

## ✅ **Opción 2: GitHub Actions (AUTOMÁTICO)**

> **Nota:** Requiere permisos de admin en el repositorio

Agregué un workflow que se ejecuta **automáticamente** cada vez que subes PDFs nuevos.

### Cómo usar:

1. **Manualmente desde GitHub:**
   - Ve a tu repo → **Actions**
   - Busca "Extraer OCR de PDFs a TXT"
   - Haz clic en **Run workflow**

2. **Automático al hacer push:**
   - El workflow se ejecuta cada vez que subes archivos `.pdf`
   - Los resultados se guardan en `OCR_EXTRACCIONES/`

---

## 🔍 **Cómo Buscar Términos en los TXT**

Una vez generados los archivos TXT:

### Terminal (grep)
```bash
# Buscar palabra clave
grep -r "acuerdo" OCR_EXTRACCIONES/

# Case-insensitive
grep -ri "clausula" OCR_EXTRACCIONES/

# Con contexto (3 líneas antes/después)
grep -C 3 "responsabilidad" OCR_EXTRACCIONES/

# Contar ocurrencias
grep -ri "multa" OCR_EXTRACCIONES/ | wc -l
```

### Python
```python
from pathlib import Path

# Buscar término
termino = "incumplimiento"
for txt_file in Path('OCR_EXTRACCIONES').rglob('*.txt'):
    with open(txt_file, 'r', encoding='utf-8') as f:
        if termino.lower() in f.read().lower():
            print(f"✅ {txt_file}")
```

### GitHub Web
1. Abre tu repo en GitHub
2. Presiona `Ctrl+K`
3. Navega a `OCR_EXTRACCIONES/`
4. Busca en los archivos .txt

---

## 📊 **Términos Jurídicos para Buscar**

```bash
# Contractuales
grep -ri "acuerdo\|clausula\|contrato" OCR_EXTRACCIONES/

# Financieros
grep -ri "balance\|factura\|pago" OCR_EXTRACCIONES/

# De Cumplimiento
grep -ri "incumplimiento\|multa\|penalidad" OCR_EXTRACCIONES/

# De Garantía
grep -ri "garantia\|fianza\|seguro" OCR_EXTRACCIONES/
```

---

## 📁 **Estructura de Archivos Generados**

### `OCR_EXTRACCIONES/INDEX.md`
Índice completo de todos los archivos TXT generados, organizados por carpeta.

### `OCR_EXTRACCIONES/BUSCADOR.md`
Guía con ejemplos de búsqueda, comandos grep, scripts Python, etc.

### `OCR_EXTRACCIONES/resumen.json`
Estadísticas:
- Total PDFs procesados
- Exitosos/fallidos
- Caracteres extraídos
- Método de extracción (directo/OCR)

### `OCR_EXTRACCIONES/[carpeta]/[archivo].txt`
Archivo de texto con:
- Encabezado con metadatos (original, fecha, páginas, método)
- Contenido extraído del PDF
- Separadores de página para claridad

---

## ⚙️ **Opciones Avanzadas**

### Regenerar solo cierta carpeta
```bash
# Crear script personalizado
find Ofertas_*/ -name "*.pdf" -exec pdftotext {} \;
```

### Usar OCR específicamente en todos los PDFs
```bash
for pdf in $(find . -name "*.pdf"); do
  pdfimages -png "$pdf" - | tesseract - stdout spa+eng > "${pdf%.pdf}.txt"
done
```

### Buscar múltiples términos
```bash
# Crear reporte
echo "=== Reporte de Términos Jurídicos ===" > reporte.txt
for termino in "acuerdo" "clausula" "responsabilidad" "multa"; do
  echo "" >> reporte.txt
  echo "### $termino" >> reporte.txt
  grep -ri "$termino" OCR_EXTRACCIONES/ >> reporte.txt
done
cat reporte.txt
```

---

## ✨ **Siguientes Pasos**

1. **Ejecuta ahora:**
   ```bash
   python3 extract_ocr.py
   ```

2. **Haz push con los archivos TXT:**
   ```bash
   git add OCR_EXTRACCIONES/
   git commit -m "🔍 Extracciones OCR de PDFs"
   git push
   ```

3. **Busca términos jurídicos:**
   ```bash
   grep -r "acuerdo" OCR_EXTRACCIONES/
   ```

4. **Integra con tu herramienta externa:**
   - Usa las URLs raw de los `.txt`
   - O descarga el contenido completo
   - O procesa con OpenAI/Claude

---

## 🆘 **Troubleshooting**

**Error: "pytesseract: "tesseract is not installed"**
```bash
# Instala Tesseract
sudo apt-get install tesseract-ocr  # Linux
brew install tesseract               # macOS
```

**Error: "ModuleNotFoundError: No module named 'pdf2image'"**
```bash
pip install pdf2image pdf2image PyPDF2
```

**Los TXT están vacíos?**
- Asegúrate de tener Tesseract instalado
- Algunos PDFs pueden ser protegidos
- Verifica en `OCR_EXTRACCIONES/resumen.json` qué falló

---

**¿Necesitas ayuda?** Ejecuta `python3 extract_ocr.py` y revisa los logs. 🚀
