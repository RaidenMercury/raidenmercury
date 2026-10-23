# ⚡ Guía: Cómo Funciona tu Perfil Automatizado

¡Tu perfil ahora está **100% automatizado**! No tienes que editar archivos a mano cada vez que subes código.

---

## 🤖 ¿Cómo se actualiza solo?

Dentro del repositorio configuramos un **GitHub Action** (`.github/workflows/update-profile.yml`) y un script en Python (`scripts/generate_dashboard.py`):

1. **Cada 6 horas** (o cada vez que hagas un `git push`), GitHub ejecuta el script en sus servidores.
2. El script lee tus repositorios públicos, mide cuántos bytes de código tienes en cada lenguaje (**Python, Go, Bash, HTML, CSS, etc.**).
3. Calcula tus puntos de experiencia (**XP**), tu **Nivel de Desarrollador** y regenera las tarjetas con las barras de progreso exactas.
4. Las tarjetas de racha y estadísticas de GitHub (`streak-stats` y `github-readme-stats`) se actualizan en tiempo real directamente desde los servidores de GitHub.

---

## ✏️ ¿Qué puedes personalizar tú si quieres?

Si en algún momento quieres cambiar un texto, tus redes o tus proyectos:

1. **Tu biografía o enlaces:** Abre `README.md` y edita la sección `[ DEVELOPER CONSOLE // ABOUT ME ]` o `[ CONECTAR // CONTACTO ]`.
2. **Frases que se escriben solas:** En `README.md`, busca la línea `readme-typing-svg` y cambia las frases en el parámetro `lines=...`.
3. **Forzar una actualización inmediata de nivel:**
   - Ve a la pestaña **Actions** en tu repositorio en GitHub web (`github.com/RaidenMercury/raidenmercury/actions`).
   - Selecciona **Update Developer Dashboard & Metrics** y dale clic a **Run workflow**.

---

## 🚀 Guardar cambios manuales

Si haces alguna edición en `README.md`, solo corre:

```bash
cd ~/Proyectos/raidenmercury
git add .
git commit -m "📝 Actualizar bio"
git push
```
