# 🎮 Guía Rápida: Cómo Personalizar tu Perfil Solo Leveling

¡Hola! Esta guía está pensada para ti, para que puedas cambiar cualquier texto, nivel o habilidad en 2 minutos sin romper nada.

---

## 🧭 ¿Dónde está cada cosa?

```
raidenmercury/
├── README.md               <-- Textos principales, sobre mí, insignias y enlaces
└── assets/                 <-- Las tarjetas visuales estilo Solo Leveling
    ├── header.svg          <-- Banner superior con la barra de navegación
    ├── status_hud.svg      <-- Tu tarjeta de jugador (Avatar, Rango, Nivel, EXP)
    ├── habit_tracker.svg   <-- Gráfico semanal de hábitos y actividad
    ├── skill_tracker.svg   <-- Tus habilidades y barras de progreso
    ├── active_quests.svg   <-- Misiones activas y recompensas
    └── goal_completion.svg <-- Anillo de XP 70% y botellas de pociones
```

---

## 1. 📝 Editar los textos del perfil (README.md)
Abre el archivo [README.md](file:///home/rmercury/Proyectos/raidenmercury/README.md) en tu editor favorito (como VS Code):
- **Frases del efecto de máquina de escribir:** Busca `lines=...` en el enlace de `readme-typing-svg`. Puedes separar frases con punto y coma `;` (reemplaza espacios por `+`).
- **Sobre mí:** Modifica el bloque `[ REGISTRO DEL CAZADOR ]` con tu nombre, bio o metas.
- **Tus tecnologías:** En `[ ARSENAL & EQUIPAMIENTO ]`, puedes agregar o quitar insignias de [Shields.io](https://shields.io).
- **Redes y contacto:** Al final, reemplaza `tu-correo@ejemplo.com` por tu correo real o tu usuario de Discord.

---

## 2. ⚡ Cambiar tu Nivel, Rango o EXP en la Tarjeta

Abre el archivo [assets/status_hud.svg](file:///home/rmercury/Proyectos/raidenmercury/assets/status_hud.svg):
- **Tu Rango:** Busca el texto `E-Rank [Awakening]` y cámbialo por lo que quieras (ej: `D-Rank Hunter`, `Coder Lv. 2`, etc.).
- **Tu Nivel:** Busca `01` y cámbialo por tu nuevo nivel.
- **Tu barra de EXP:** Busca el texto `450 / 1000 XP` y la línea:
  ```xml
  <rect x="1" y="21" width="162" height="10" ... />
  ```
  (Aumenta `width="162"` hasta un máximo de `360` según cuánto quieras llenar la barra).

---

## 3. 🎯 Editar tus Habilidades

Abre el archivo [assets/skill_tracker.svg](file:///home/rmercury/Proyectos/raidenmercury/assets/skill_tracker.svg):
- Cada habilidad tiene su nombre (ej: `Python & Core Logic`) y su porcentaje (ej: `LVL 42 (68%)`).
- Para que la barra crezca o baje, cambia el `width="216"` de la etiqueta `<rect>` correspondiente (el ancho total es `318`).

---

## 4. ⚔️ Editar tus Misiones y Desafíos

Abre el archivo [assets/active_quests.svg](file:///home/rmercury/Proyectos/raidenmercury/assets/active_quests.svg):
- Puedes cambiar los nombres de las misiones (ej: `Daily Training: Code 1hr`, `Build Custom Bot`).
- También puedes cambiar el estado (`IN PROG`, `DONE`, `75%`) y las recompensas (`+150 EXP`).

---

## 🚀 ¿Cómo publicar los cambios en tu GitHub?

Siempre que hagas cambios, corre estos 3 comandos en tu terminal dentro de la carpeta:

```bash
cd ~/Proyectos/raidenmercury
git add .
git commit -m "✨ Actualizar perfil Solo Leveling"
git push
```

¡Y listo! Tu página de inicio en GitHub (`github.com/RaidenMercury`) se actualizará al instante con tu nuevo diseño.
