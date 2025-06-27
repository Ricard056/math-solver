Git Workflow - Guía de Comandos

# # 🔄 Workflow Básico (Crear Checkpoints)

# # Template Rápido - Copiar y Pegar <---------
git add .
git commit -m "CAMBIAR_ESTE_MENSAJE"
git push

# # Paso a Paso Detallado
# 1. Ver estado actual
git status

# 2. Agregar cambios
git add .                    # Todos los archivos
git add src/main.py         # Solo un archivo específico
git add src/                # Solo una carpeta

# 3. Crear commit (checkpoint)
git commit -m "Descripción del cambio"

# 4. Subir a GitHub
git push

# # 📝 Ejemplos de Mensajes de Commit
git commit -m "Agregar función de suma"
git commit -m "Corregir bug en división por cero"
git commit -m "Refactorizar código de entrada"
git commit -m "Agregar validación de inputs"
git commit -m "Mejorar interfaz de usuario"
git commit -m "Documentar funciones principales"

# # ⏮️ Regresar a Checkpoints Anteriores
Ver historial de commits
git log --oneline           # Ver lista corta
git log                     # Ver lista detallada

# Regresar temporalmente (para revisar)
git checkout COMMIT_HASH    # Ejemplo: git checkout a1b2c3d
git checkout main           # Regresar al último commit

# # Regresar permanentemente (¡CUIDADO!)
# Opción 1: Crear nuevo commit que deshace cambios
git revert COMMIT_HASH

# Opción 2: Eliminar commits (PELIGROSO)
git reset --hard COMMIT_HASH
git push --force

# # 🔍 Comandos de VERIFICACION <---------
# Al abrir VSCode (opcional)
git status              # Estado actual
git log --oneline       # Últimos commits
git branch             # Rama actual
# Para ver diferencias
git diff               # Cambios no guardados
git diff --staged      # Cambios en staging
git show              # Último commit

# # 🌿 Trabajo con Ramas (Branches)
# Crear nueva rama para experimentar
git branch nueva-feature      # Crear rama
git checkout nueva-feature    # Cambiar a la rama
# O hacer ambos en uno:
git checkout -b nueva-feature
# Cambiar entre ramas
git checkout main             # Ir a main
git checkout nueva-feature    # Ir a feature
# Fusionar rama con main
git checkout main
git merge nueva-feature
git push

# # 🆘 Comandos de Emergencia
# Si cometiste un error antes del commit
git restore archivo.py      # Deshacer cambios en un archivo
git restore .              # Deshacer todos los cambios
# Si cometiste un error después del add
git reset archivo.py       # Quitar archivo del staging
git reset                 # Quitar todos del staging
# Si necesitas hacer cambios al último commit
git add .
git commit --amend -m "Mensaje corregido"

# # 📊 Comandos Útiles Adicionales
# Ver archivos ignorados
cat .gitignore

# Ver configuración actual
git config --list

# Ver remotos configurados
git remote -v

# Verificar conexión con GitHub
git remote show origin

# # 🎯 Flujo Recomendado para Proyectos <---------
# 1. Antes de programar: git status (verificar estado)
# 2. Mientras programas: Guarda frecuentemente (Ctrl+S)
# 3. Cada feature completada:
git add .
git commit -m "Descripción clara"
git push

# Al final del día: Siempre hacer push de los commits pendientes

# # ⚠️ Notas Importantes

# Siempre hacer commit antes de experimentos grandes
# Mensajes de commit claros y descriptivos
# Hacer push regularmente para no perder trabajo
# No usar git reset --hard a menos que estés 100% seguro