#!/usr/bin/env python3
"""
Extractor OCR de PDFs a TXT
Convierte automáticamente todos los PDFs del repositorio a archivos de texto con OCR
"""

import os
import sys
from pathlib import Path
import subprocess
import json
from datetime import datetime

# Intentar importar librerías
try:
    import pdfplumber
    from pdf2image import convert_from_path
    import pytesseract
    from PIL import Image
except ImportError as e:
    print(f"❌ Error: Falta instalar dependencias")
    print(f"   Ejecuta: pip install pdfplumber pdf2image pytesseract pillow PyPDF2")
    sys.exit(1)


class PDFtoTXTExtractor:
    def __init__(self):
        self.ocr_results = {
            "timestamp": datetime.now().isoformat(),
            "total_pdfs": 0,
            "exitosos": 0,
            "fallidos": 0,
            "archivos": [],
            "tiempo_inicio": datetime.now().isoformat()
        }
        self.output_dir = Path('OCR_EXTRACCIONES')
        self.output_dir.mkdir(exist_ok=True)

    def extract_pdf(self, pdf_path):
        """Extrae texto de un PDF usando PDFPlumber + Tesseract OCR"""
        print(f"\n📄 Procesando: {pdf_path}")
        
        extracted_text = ""
        method_used = "unknown"
        
        try:
            # Método 1: Extracción directa con pdfplumber
            print(f"  → Intentando extracción de texto directo...")
            try:
                with pdfplumber.open(str(pdf_path)) as pdf:
                    for page_num, page in enumerate(pdf.pages, 1):
                        text = page.extract_text()
                        if text and len(text.strip()) > 20:
                            extracted_text += f"\n\n{'='*80}\nPÁGINA {page_num}\n{'='*80}\n\n{text}"
                        
                if len(extracted_text.strip()) > 100:
                    method_used = "directo"
                    print(f"  ✅ Extracción directa exitosa")
                    
            except Exception as e:
                print(f"  ⚠️  Extracción directa falló: {str(e)}")
            
            # Método 2: OCR con Tesseract si extracción directa fue insuficiente
            if len(extracted_text.strip()) < 100:
                print(f"  → Usando OCR con Tesseract (puede tomar tiempo)...")
                method_used = "ocr"
                
                try:
                    images = convert_from_path(str(pdf_path), dpi=150)
                    print(f"    Convertidas {len(images)} páginas a imágenes")
                    
                    for page_num, image in enumerate(images, 1):
                        print(f"    Procesando página {page_num}/{len(images)}...", end='\r')
                        try:
                            # Tesseract con español + inglés
                            ocr_text = pytesseract.image_to_string(image, lang='spa+eng')
                            if ocr_text and len(ocr_text.strip()) > 20:
                                extracted_text += f"\n\n{'='*80}\nPÁGINA {page_num} (OCR)\n{'='*80}\n\n{ocr_text}"
                        except Exception as e:
                            print(f"    ⚠️  Error en página {page_num}: {str(e)}")
                    
                    print(f"    ✅ OCR completado")
                    
                except Exception as e:
                    print(f"  ❌ Error en OCR: {str(e)}")
                    raise
            
            # Guardar archivo TXT
            output_path = self.output_dir / pdf_path.parent / f"{pdf_path.stem}.txt"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                # Encabezado
                f.write("╔" + "="*78 + "╗\n")
                f.write("║ " + "EXTRACCIÓN OCR AUTOMÁTICA".center(76) + " ║\n")
                f.write("╠" + "="*78 + "╣\n")
                f.write(f"║ Archivo: {str(pdf_path):<62} ║\n")
                f.write(f"║ Extraído: {datetime.now().isoformat():<57} ║\n")
                f.write(f"║ Método: {method_used:<70} ║\n")
                f.write("╚" + "="*78 + "╝\n\n")
                f.write(extracted_text)
            
            char_count = len(extracted_text)
            self.ocr_results["exitosos"] += 1
            print(f"  ✅ Guardado: {output_path}")
            print(f"     ({char_count} caracteres, método: {method_used})")
            
            self.ocr_results["archivos"].append({
                "original": str(pdf_path),
                "output": str(output_path),
                "caracteres": char_count,
                "metodo": method_used,
                "estado": "exitoso"
            })
            
            return True
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            self.ocr_results["fallidos"] += 1
            self.ocr_results["archivos"].append({
                "original": str(pdf_path),
                "estado": "fallido",
                "error": str(e)
            })
            return False

    def create_index(self):
        """Crea índice de archivos OCR"""
        print("\n📖 Creando índice...")
        
        index_content = """# Índice de Extracciones OCR - Licitación 4776-4-LR26

Este directorio contiene las extracciones de texto de todos los archivos PDF del repositorio.

**Generado:** """ + datetime.now().isoformat() + """

## 📁 Estructura de Directorios

"""
        
        # Agrupar por carpeta
        txt_files = sorted(self.output_dir.rglob('*.txt'))
        by_dir = {}
        
        for txt_file in txt_files:
            if txt_file.name in ['INDEX.md', 'BUSCADOR.md', 'resumen.json']:
                continue
            dir_name = str(txt_file.parent).replace(str(self.output_dir) + '/', '')
            if dir_name == 'OCR_EXTRACCIONES':
                dir_name = 'raíz'
            if dir_name not in by_dir:
                by_dir[dir_name] = []
            by_dir[dir_name].append(txt_file)
        
        for dir_name in sorted(by_dir.keys()):
            index_content += f"\n### {dir_name}\n\n"
            for txt_file in sorted(by_dir[dir_name]):
                rel_path = str(txt_file).replace(f"{self.output_dir}/", "")
                file_size = txt_file.stat().st_size
                index_content += f"- [{txt_file.name}]({rel_path}) - {file_size/1024:.1f} KB\n"
        
        index_content += f"""

## 📊 Estadísticas

- **Total archivos OCR generados:** {len(txt_files)}
- **Timestamp:** {datetime.now().isoformat()}
- **Completitud:** {(self.ocr_results['exitosos']/max(1, self.ocr_results['total_pdfs'])*100):.1f}%

## 🔍 Cómo buscar

Ver: [BUSCADOR.md](BUSCADOR.md)

## 📝 Resumen de procesamiento

Ver: [resumen.json](resumen.json)
"""
        
        index_path = self.output_dir / 'INDEX.md'
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        print(f"  ✅ Índice creado: {index_path}")

    def create_searcher_guide(self):
        """Crea guía de búsqueda"""
        print("🔍 Creando guía de búsqueda...")
        
        searcher_content = """# 🔍 Buscador de Términos - OCR Extracciones

## Búsqueda rápida en terminal

```bash
# Buscar palabra clave
grep -r "acuerdo" OCR_EXTRACCIONES/

# Case-insensitive
grep -ri "clausula" OCR_EXTRACCIONES/

# Con contexto (3 líneas)
grep -C 3 "responsabilidad" OCR_EXTRACCIONES/

# Contar ocurrencias
grep -ri "multa" OCR_EXTRACCIONES/ | wc -l

# Mostrar archivos que contienen el término
grep -l "incumplimiento" OCR_EXTRACCIONES/**/*.txt
```

## Búsqueda con Python

```python
from pathlib import Path

termino = "acuerdo"
resultado = []

for txt_file in Path('OCR_EXTRACCIONES').rglob('*.txt'):
    with open(txt_file, 'r', encoding='utf-8') as f:
        contenido = f.read()
        if termino.lower() in contenido.lower():
            resultado.append(txt_file)

print(f"Encontrado en {len(resultado)} archivos:")
for archivo in resultado:
    print(f"  ✅ {archivo}")
```

## Términos jurídicos comunes

### Contractuales
- acuerdo
- cláusula / clausula
- contrato
- términos y condiciones

### Financieros
- balance
- factura
- pago
- rentabilidad
- inversión

### Legales
- responsabilidad
- incumplimiento
- multa / penalidad
- garantía / garantia
- fianza
- seguro

### De Cumplimiento
- firma / firmas
- sello
- RUT
- representante legal

## Búsquedas avanzadas

```bash
# Múltiples términos (OR)
grep -ri "acuerdo\\|contrato\\|clausula" OCR_EXTRACCIONES/

# Excluir palabras
grep -ri "acuerdo" OCR_EXTRACCIONES/ | grep -v "desacuerdo"

# En archivo específico
grep "multa" OCR_EXTRACCIONES/Evaluacion_Financiera/**/*.txt

# Generar reporte
for termino in "acuerdo" "clausula" "responsabilidad"; do
  echo "=== $termino ===" >> reporte.txt
  grep -ri "$termino" OCR_EXTRACCIONES/ >> reporte.txt
done
```

## 📊 Búsqueda en GitHub Web

1. Ve a tu repo
2. Presiona `Ctrl+K` o `.` (punto)
3. Busca: `path:OCR_EXTRACCIONES/ término`

---

**¿Necesitas ayuda?** Ver: GENERAR_OCR.md
"""
        
        searcher_path = self.output_dir / 'BUSCADOR.md'
        with open(searcher_path, 'w', encoding='utf-8') as f:
            f.write(searcher_content)
        print(f"  ✅ Guía de búsqueda creada: {searcher_path}")

    def create_summary(self):
        """Crea resumen en JSON"""
        self.ocr_results["tiempo_fin"] = datetime.now().isoformat()
        
        summary_path = self.output_dir / 'resumen.json'
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(self.ocr_results, f, ensure_ascii=False, indent=2)
        print(f"  ✅ Resumen creado: {summary_path}")

    def run(self):
        """Ejecuta el proceso completo"""
        print("\n" + "="*80)
        print("🚀 EXTRACTOR OCR DE PDFs A TXT".center(80))
        print("="*80 + "\n")
        
        # Buscar PDFs
        pdf_files = list(Path('.').rglob('*.pdf'))
        pdf_files = [p for p in pdf_files if 'OCR_EXTRACCIONES' not in str(p)]
        
        self.ocr_results["total_pdfs"] = len(pdf_files)
        print(f"🔍 Encontrados {len(pdf_files)} archivos PDF\n")
        
        # Procesar cada PDF
        for pdf_path in sorted(pdf_files):
            self.extract_pdf(pdf_path)
        
        # Crear archivos de índice
        print("\n" + "-"*80)
        self.create_index()
        self.create_searcher_guide()
        self.create_summary()
        
        # Resumen final
        print("\n" + "="*80)
        print("✅ PROCESAMIENTO COMPLETADO".center(80))
        print("="*80)
        print(f"\n📊 RESULTADOS:")
        print(f"   Total PDFs: {self.ocr_results['total_pdfs']}")
        print(f"   Exitosos: {self.ocr_results['exitosos']} ✅")
        print(f"   Fallidos: {self.ocr_results['fallidos']} ❌")
        
        if self.ocr_results['total_pdfs'] > 0:
            tasa = (self.ocr_results['exitosos']/self.ocr_results['total_pdfs']*100)
            print(f"   Tasa de éxito: {tasa:.1f}%")
        
        print(f"\n📁 Archivos generados en: {self.output_dir}/")
        print(f"   - INDEX.md (índice completo)")
        print(f"   - BUSCADOR.md (guía de búsqueda)")
        print(f"   - resumen.json (estadísticas)")
        print(f"   - [Carpetas] (archivos TXT por categoría)")
        print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    extractor = PDFtoTXTExtractor()
    extractor.run()
