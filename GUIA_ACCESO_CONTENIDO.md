# Guía de Acceso y Procesamiento de Contenido Jurídico

## Problema Identificado
Los archivos PDF son binarios. GitHub los entrega en base64 vía API, lo cual es ineficiente para análisis de contenido jurídico.

---

## Solución: 3 Opciones Operativas

### ✅ OPCIÓN 1: Acceso a Texto OCR (RECOMENDADO)

**Objetivo:** Extraer texto de PDFs para análisis jurídico sin base64

#### A. Usar API de Extracción de Texto (Sin Código)

**Herramientas recomendadas:**

| Herramienta | Uso | Ventaja |
|---|---|---|
| **Adobe PDF Services API** | Extraer texto de PDFs | Mantiene formato legal, tablas, firmas |
| **Upstash Document Processing** | OCR + extracción | Serverless, sin configuración |
| **AWS Textract** | OCR de documentos | Reconoce tablas y firmas digitales |
| **OpenAI Vision API** | Análisis de PDFs | Comprensión jurídica integrada |

#### B. Flujo Automatizado con GitHub Actions

```yaml
# .github/workflows/pdf-extract.yml
name: Extraer Texto de PDFs
on:
  push:
    paths:
      - '**.pdf'

jobs:
  extract:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Instalar herramientas
        run: sudo apt-get install -y poppler-utils
      - name: Extraer PDF a TXT
        run: |
          find . -name "*.pdf" -type f | while read pdf; do
            pdftotext "$pdf" "${pdf%.pdf}.txt"
          done
      - name: Commit cambios
        run: |
          git config user.name "PDF Extractor"
          git config user.email "bot@github.local"
          git add "*.txt"
          git commit -m "Extracción automática de texto de PDFs" || true
          git push
```

---

### ✅ OPCIÓN 2: Índice de Resúmenes Jurídicos

**Objetivo:** Crear un documento de referencia rápida sin necesidad de procesar cada PDF

#### A. Crear `RESUMEN_CONTENIDO_JURIDICO.md`

Estructura sugerida:

```markdown
# Resumen de Contenido Jurídico - Licitación 4776-4-LR26

## Categoría: Evaluación Contractual
- **Archivo:** CRS Allende.pdf
- **Contenido clave:** [Resumen 1-2 párrafos del contenido jurídico]
- **Acuerdos:** [Términos principales]
- **Fecha:** [Si aplica]

## Categoría: Evaluación Financiera
- **Archivos relacionados:** Balance 2023, Balance 2024, F-22 AT, etc.
- **Síntesis:** [Análisis financiero de la oferta]

## Categoría: Ofertas
- **Oferente:** LAYNER SPA
- **Documentos críticos:**
  - RUT: 76.034.985-2
  - Documentación: Escrituras, Poderes, Vigencia, etc.
```

#### B. Script para Generar Índice Automático

```python
# scripts/generar_indice.py
import json
import os
from datetime import datetime

INDEX = {
    "timestamp": datetime.now().isoformat(),
    "repositorio": "4776-4-LR26",
    "archivos_indexados": []
}

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.pdf'):
            ruta_completa = os.path.join(root, file)
            tamaño = os.path.getsize(ruta_completa)
            
            INDEX["archivos_indexados"].append({
                "ruta": ruta_completa,
                "nombre": file,
                "tamaño_kb": tamaño / 1024,
                "categoria": root.split('/')[1] if '/' in root else "raíz",
                "acceso": f"https://raw.githubusercontent.com/Diegogallegosvallejos/4776-4-LR26/main/{ruta_completa}",
                "requiere_ocr": True
            })

with open('INDICE_ARCHIVOS.json', 'w', encoding='utf-8') as f:
    json.dump(INDEX, f, ensure_ascii=False, indent=2)

print(f"✅ Índice generado: {len(INDEX['archivos_indexados'])} archivos")
```

---

### ✅ OPCIÓN 3: Acceso a URLs de Descarga Directa (INMEDIATO)

**Ventaja:** No requiere API de GitHub, funciona con cualquier herramienta

#### A. URLs de Descarga Directa (Raw Content)

Para cada PDF, GitHub proporciona descarga directa:

```
https://raw.githubusercontent.com/Diegogallegosvallejos/4776-4-LR26/main/[RUTA_DEL_ARCHIVO]
```

**Ejemplos:**
```
# PDFs raíz
https://raw.githubusercontent.com/Diegogallegosvallejos/4776-4-LR26/main/5-Cuadro_de_Ofertas_4776-4-LR26.pdf
https://raw.githubusercontent.com/Diegogallegosvallejos/4776-4-LR26/main/Plan_de_Trabajo%20(1).pdf

# PDFs en carpetas
https://raw.githubusercontent.com/Diegogallegosvallejos/4776-4-LR26/main/Ofertas_20260506122727/Escritura_LAYNER_SPA.pdf
https://raw.githubusercontent.com/Diegogallegosvallejos/4776-4-LR26/main/Evaluacion_Financiera/Evaluacion%20Financiera/Balance%20Firmado%202024%20Layner.pdf
```

#### B. Script para Generar URLs de Descarga

```bash
#!/bin/bash
# scripts/generar_urls.sh

echo "# URLs de Descarga Directa - Archivos Jurídicos" > URLS_DESCARGA.md
echo "Generado: $(date)" >> URLS_DESCARGA.md
echo "" >> URLS_DESCARGA.md

find . -name "*.pdf" -type f | sort | while read pdf; do
    # URL-encode la ruta
    url_path=$(echo "$pdf" | sed 's/ /%20/g' | sed 's/^.\///')
    url="https://raw.githubusercontent.com/Diegogallegosvallejos/4776-4-LR26/main/$url_path"
    
    echo "- [$pdf]($url)" >> URLS_DESCARGA.md
done

echo "✅ URLs generadas en URLS_DESCARGA.md"
```

---

## Solución Integrada Recomendada

### Paso 1: Crear Base de Datos JSON de Metadatos

```json
{
  "id_licitacion": "4776-4-LR26",
  "archivos": [
    {
      "nombre": "Escritura_LAYNER_SPA.pdf",
      "ruta_github": "Ofertas_20260506122727/Escritura_LAYNER_SPA.pdf",
      "sha": "8686ad2368ac4ec6e773fe8c99701eb2d792b312",
      "tamaño_bytes": 1418960,
      "categoria": "ofertas",
      "ofertante": "LAYNER_SPA",
      "tipo_documento": "Escritura Social",
      "url_descarga": "https://raw.githubusercontent.com/Diegogallegosvallejos/4776-4-LR26/main/Ofertas_20260506122727/Escritura_LAYNER_SPA.pdf",
      "url_api_raw": "https://api.github.com/repos/Diegogallegosvallejos/4776-4-LR26/contents/Ofertas_20260506122727/Escritura_LAYNER_SPA.pdf",
      "procesable_ocr": true,
      "requiere_firma_digital": true
    }
  ]
}
```

### Paso 2: Integración con Herramientas Externas

**Para herramientas que necesiten el contenido:**

```python
import requests
import base64
from pdf2image import convert_from_bytes

# Obtener PDF desde GitHub (opción raw)
url = "https://raw.githubusercontent.com/Diegogallegosvallejos/4776-4-LR26/main/Ofertas_20260506122727/Escritura_LAYNER_SPA.pdf"
response = requests.get(url)

# Opción A: Procesar con OCR
from pytesseract import pytesseract
images = convert_from_bytes(response.content)
texto_extraido = "\n".join([pytesseract.image_to_string(img) for img in images])

# Opción B: Enviar a API de análisis (OpenAI, etc.)
# análisis_juridico = analizador_legal.procesar(response.content)
```

### Paso 3: Crear Dashboard de Acceso

```html
<!-- docs/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Portal de Acceso - Licitación 4776-4-LR26</title>
    <style>
        body { font-family: Arial; max-width: 1200px; margin: 20px auto; }
        .pdf-card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .download { color: #0066cc; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Portal de Documentos - Licitación 4776-4-LR26</h1>
    <div id="archivos"></div>
    <script>
        fetch('archivos.json').then(r => r.json()).then(data => {
            const html = data.archivos.map(arch => `
                <div class="pdf-card">
                    <h3>${arch.nombre}</h3>
                    <p>Ruta: ${arch.ruta_github}</p>
                    <a class="download" href="${arch.url_descarga}">⬇️ Descargar</a>
                </div>
            `).join('');
            document.getElementById('archivos').innerHTML = html;
        });
    </script>
</body>
</html>
```

---

## Resumen: Próximos Pasos

| Paso | Acción | Resultado |
|------|--------|-----------|
| 1 | Usar URLS de descarga directa (inmediato) | Acceso sin base64 |
| 2 | Implementar workflow GitHub Actions | OCR automático → TXT |
| 3 | Crear índice JSON de metadatos | Base de datos indexable |
| 4 | Integrar con herramientas externas | Análisis jurídico automático |

---

## Recomendación Final

**Para tu caso específico (análisis jurídico):**

1. ✅ **Usa URLs RAW** para descarga directa
2. ✅ **Configura GitHub Actions** para extraer OCR automáticamente
3. ✅ **Mantén un JSON de metadatos** para búsquedas rápidas
4. ✅ **Integra con OpenAI API** o similar para análisis de contenido

Esto te da acceso total sin limitaciones de base64.
