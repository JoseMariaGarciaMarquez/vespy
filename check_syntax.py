# Script de verificación de VESPY
# Este script verifica que el código Python sea sintácticamente correcto

import sys
import os
from pathlib import Path

def check_python_syntax(file_path):
    """Verificar la sintaxis de un archivo Python."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        compile(code, file_path, 'exec')
        print(f"✓ {file_path}: Sintaxis correcta")
        return True
    except SyntaxError as e:
        print(f"✗ {file_path}: Error de sintaxis - {e}")
        return False
    except Exception as e:
        print(f"? {file_path}: Error al verificar - {e}")
        return False

def main():
    print("=== VERIFICACIÓN DE SINTAXIS DE VESPY ===\n")
    
    # Archivos a verificar
    files_to_check = [
        "src/vespy.py",
        "src/data_analysis.py", 
        "src/load.py",
        "src/plot_ves.py",
        "src/invert_ves.py",
        "src/preprocessing.py",
        "src/classified_ves.py",
        "src/gui_ves.py",
        "src/help_window.py",
        "src/welcome.py"
    ]
    
    total_files = 0
    passed_files = 0
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            total_files += 1
            if check_python_syntax(file_path):
                passed_files += 1
        else:
            print(f"⚠ {file_path}: Archivo no encontrado")
    
    print(f"\n=== RESULTADO ===")
    print(f"Archivos verificados: {total_files}")
    print(f"Archivos con sintaxis correcta: {passed_files}")
    print(f"Archivos con errores: {total_files - passed_files}")
    
    if passed_files == total_files:
        print("\n🎉 ¡Todos los archivos tienen sintaxis correcta!")
        print("\nLas líneas rojas que ves son errores de importación porque")
        print("las dependencias no están instaladas. Para solucionarlo:")
        print("\n1. Ejecuta: install.bat (o install.ps1)")
        print("2. Activa el entorno: conda activate pg")
        print("3. Ejecuta: python src/vespy.py")
    else:
        print("\n❌ Hay errores de sintaxis que necesitan corrección.")

if __name__ == "__main__":
    main()
