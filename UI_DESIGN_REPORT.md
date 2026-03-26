# UI Design Report: Tirth's Prompt Garage

## 1. Aesthetic Theme & Visual Identity
The interface adopts a **Cyberpunk/Futuristic** aesthetic, characterized by a "dark mode" base with vibrant neon accents. The design focuses on high technology and creative engineering, mirroring the "Prompt Garage" metaphor.

## 2. Color Palette
The color scheme is meticulously defined using CSS variables for consistency:
- **Backgrounds:** `--bg` (#020810), `--surface` (#071525) - deep, dark blues and blacks providing high contrast.
- **Accents:** `--cyan` (#00f5ff), `--blue` (#0080ff) - electric, glowing blues used for primary highlights and interactive states.
- **Status/Feedback:** `--green` (#00ff88), `--red` (#ff3a5c) - used for successful actions (e.g., uploads) and errors.
- **Typography Colors:** `--text` (#c8e8ff), `--muted` (#8ec8e8) - light blue tints to maintain readability without harsh white-on-black contrast.

## 3. Typography
- **Headings & Accents:** **Orbitron** - A geometric sans-serif font that evokes a sci-fi, high-tech feel. Used for the main logo, section labels, and buttons.
- **Body Text:** **Exo 2** - A modern sans-serif with a futuristic edge, optimized for legibility in long-form descriptions and prompts.

## 4. 3D Interactive Background (Three.js)
A sophisticated 3D scene is rendered behind the content to deepen the immersive experience:
- **Environment:** A rainy neon city skyline with three layers of depth.
- **Buildings:** Procedurally generated skyscrapers with flickering light-blue windows (`WIN_COL`).
- **Atmosphere:** A fog effect (`0x020810`) and a downward-moving rain particle system.
- **Interactivity:** A spot searchlight follows the user's cursor, casting dynamic lighting on the scene. Flying vehicles with headlights zip through the city "lanes."

## 5. Procedural Sound Engine (Web Audio API)
The UI features a custom synthesized sound engine that generates SFX in real-time (no external audio files required):
- **Hover:** Electric flicker noise on interactive elements.
- **Copy Action:** A satisfying two-tone square-wave beep with a trailing shimmer.
- **System Alerts:** Power-up sweeps for dev mode unlocking and power-down sweeps for locking.
- **Engagement:** Deep thuds and shimmers when opening the image lightbox.

## 6. Motion Design & Animations
- **Scroll Pop:** Cards use an `IntersectionObserver` to trigger a "pop-in" animation (scaling and translation) as they enter the viewport.
- **Title Flow:** The main H1 heading features a sliding linear gradient animation to simulate flowing energy.
- **Scanline Effect:** A subtle `repeating-linear-gradient` overlay with a vertical animation mimics old CRT or HUD scanning.
- **Blinking Elements:** "Active Prompt" indicators and building antennas use CSS keyframe animations to pulse or blink.

## 7. Interface Components
- **Prompt Cards:** Glassmorphism-style containers with glow borders, numbered indices, and quick-copy functionality.
- **Image Lightbox:** A blur-backed modal for high-resolution AI preview viewing.
- **Toast Notifications:** Minimalist floating alerts for system feedback (e.g., "Prompt copied to buffer").
- **Developer Interface:** A hidden "secret trigger" (dot in the bottom corner) that reveals a password-protected dashboard for managing prompts and uploading new AI previews.

## 8. Responsiveness
- The layout uses a flexible flexbox/grid system to adapt from desktop to mobile screens.
- Typography scales using `clamp()` (e.g., `clamp(1.8rem, 5vw, 3.4rem)`) to ensure the branding remains impactful across all devices.
