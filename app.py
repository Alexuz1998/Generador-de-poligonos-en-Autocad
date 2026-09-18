from pathlib import Path
from PIL import Image
import base64, io, zipfile, ast

src = Path("/mnt/data/Pikachu_atlas.gif")
if not src.exists():
    raise FileNotFoundError("No se encontró el GIF base Pikachu_atlas.gif.")

def make_transparent_frame(im, tolerance=28):
    """Quita solo el fondo claro conectado con los bordes."""
    rgba = im.convert("RGBA")
    w, h = rgba.size
    px = rgba.load()

    # Fondo de referencia tomado de las esquinas.
    bg = rgba.getpixel((0, 0))[:3]

    def close_to_bg(rgb):
        return max(abs(rgb[i] - bg[i]) for i in range(3)) <= tolerance

    # Flood fill desde todos los bordes, conservando zonas blancas internas
    # que formen parte del personaje.
    seen = bytearray(w * h)
    stack = []

    for x in range(w):
        stack.append((x, 0))
        stack.append((x, h - 1))
    for y in range(h):
        stack.append((0, y))
        stack.append((w - 1, y))

    while stack:
        x, y = stack.pop()
        idx = y * w + x
        if seen[idx]:
            continue

        rgb = px[x, y][:3]
        if not close_to_bg(rgb):
            continue

        seen[idx] = 1
        px[x, y] = (rgb[0], rgb[1], rgb[2], 0)

        if x > 0:
            stack.append((x - 1, y))
        if x < w - 1:
            stack.append((x + 1, y))
        if y > 0:
            stack.append((x, y - 1))
        if y < h - 1:
            stack.append((x, y + 1))

    return rgba

im = Image.open(src)
frames = []
durations = []

for n in range(im.n_frames):
    im.seek(n)
    frame = make_transparent_frame(im)
    frames.append(frame)
    durations.append(im.info.get("duration", 80))

transparent_gif = Path("/mnt/data/Pikachu_atlas_transparente.gif")
frames[0].save(
    transparent_gif,
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=0,
    disposal=2,
    transparency=0,
    optimize=False
)

# Verificación del primer frame.
check = Image.open(transparent_gif).convert("RGBA")
corners = [
    check.getpixel((0, 0)),
    check.getpixel((check.width - 1, 0)),
    check.getpixel((0, check.height - 1)),
]
print("Transparencia verificada en esquinas:", corners)

# Generar una versión actualizada del app.py con el GIF transparente incrustado
app_old = Path("/mnt/data/app_generador_predios_fijo.py")
app = app_old.read_text(encoding="utf-8")

gif_b64 = base64.b64encode(transparent_gif.read_bytes()).decode("ascii")

# Sustituye el GIF incrustado existente.
marker_start = '# GIF del encabezado\n'
marker_end = '\n\n# ============================================================'
start = app.find(marker_start)
end = app.find(marker_end, start)
if start == -1 or end == -1:
    raise RuntimeError("No se encontró el bloque del GIF en app.py.")

new_gif_block = f'''# GIF del encabezado
# El GIF transparente está incrustado para que Streamlit Cloud
# no dependa de un archivo externo.
GIF_BASE64 = "{gif_b64}"
'''
app = app[:start] + new_gif_block + app[end:]

# Duplica el tamaño visible y elimina el efecto que pudiera dar apariencia de fondo.
app = app.replace(
    "    width: 88px;\n    height: 88px;",
    "    width: 176px;\n    height: 176px;"
)
app = app.replace(
    "    filter: drop-shadow(0 0 12px rgba(138, 99, 201, 0.5));\n",
    ""
)
app = app.replace(
    "    border-radius: 18px;\n",
    ""
)

# Actualiza el alt para que refleje el nuevo recurso.
app = app.replace(
    'alt="Animación de Pikachu"',
    'alt="Pikachu animado"'
)

fixed2 = Path("/mnt/data/app_generador_predios_pikachu_transparente.py")
fixed2.write_text(app, encoding="utf-8")
ast.parse(app)

zip2 = Path("/mnt/data/Generador_LISP_ATLAS_PIKACHU.zip")
with zipfile.ZipFile(zip2, "w", compression=zipfile.ZIP_DEFLATED) as z:
    z.write(fixed2, "app.py")

print(f"GIF transparente: {transparent_gif}")
print(f"App actualizada: {fixed2}")
print(f"ZIP: {zip2}")
