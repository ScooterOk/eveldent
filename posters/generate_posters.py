import os
import subprocess

OUT_DIR = "/Users/scooterok/www/eveldent/posters"
os.makedirs(OUT_DIR, exist_ok=True)

def convert_pdf_to_tiff_cmyk(pdf_path, tif_path, dpi=150):
    tmp_prefix = f"/tmp/render_{os.path.basename(pdf_path)}"
    # 1. Render high-res PNG via pdftoppm
    subprocess.run(["pdftoppm", "-png", "-r", str(dpi), pdf_path, tmp_prefix], check=True)
    rendered_png = f"{tmp_prefix}-1.png"
    # 2. Convert to CMYK TIFF with LZW compression via ImageMagick
    subprocess.run(["magick", rendered_png, "-colorspace", "CMYK", "-compress", "lzw", tif_path], check=True)
    if os.path.exists(rendered_png):
        os.remove(rendered_png)
    print(f"Generated TIFF (CMYK {dpi} DPI): {tif_path}")

# -------------------------------------------------------------
# POSTER 1: СХЕМА (ОБ'ЄКТ ЗАБЕЗПЕЧЕНИЙ УКРИТТЯМ / НЕ ЗАБЕЗПЕЧЕНИЙ)
# -------------------------------------------------------------
def make_poster1(is_provided=True):
    title_line2 = "ЗАБЕЗПЕЧЕНИЙ" if is_provided else "НЕ ЗАБЕЗПЕЧЕНИЙ"
    filename_base = "poster_1_zabezpecheniy" if is_provided else "poster_1_ne_zabezpecheniy"
    
    line2_font_size = 49 if is_provided else 43
    line2_y_offset = 66
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000mm" height="600mm" viewBox="0 0 1000 600">
  <defs>
    <style>
      .bold-condensed {{
        font-family: "Arial Black", "Arial", "Helvetica Neue", sans-serif;
        font-weight: 900;
        fill: #111111;
      }}
      .addr-title {{
        font-family: "Arial", "Helvetica Neue", sans-serif;
        font-weight: 700;
        font-size: 25px;
        fill: #222222;
      }}
      .addr-text {{
        font-family: "Arial Black", "Arial", sans-serif;
        font-weight: 900;
        font-size: 38px;
        fill: #000000;
      }}
      .addr-sub {{
        font-family: "Arial", "Helvetica Neue", sans-serif;
        font-weight: 700;
        font-size: 27px;
        fill: #C62828;
      }}
    </style>
  </defs>

  <!-- Background -->
  <rect width="1000" height="600" fill="#FFFFFF" />

  <!-- Outer Rounded Frame -->
  <rect x="25" y="25" width="950" height="550" rx="28" ry="28" fill="none" stroke="#111111" stroke-width="8" />

  <!-- ================= TOP SECTION ================= -->
  <!-- Warning Triangle (Left) -->
  <g id="warning-triangle" transform="translate(75, 75)">
    <!-- Red Triangle Base -->
    <path d="M 125,22 L 235,212 A 16,16 0 0,1 221,232 L 29,232 A 16,16 0 0,1 15,212 L 125,22 Z" 
          fill="#E52222" stroke="#E52222" stroke-width="16" stroke-linejoin="round" />
    <!-- Inner White Triangle Outline -->
    <path d="M 125,48 L 217,212 L 33,212 Z" 
          fill="none" stroke="#FFFFFF" stroke-width="6.5" stroke-linejoin="round" />
    <!-- White Exclamation Mark -->
    <rect x="115.5" y="82" width="19" height="76" rx="9.5" ry="9.5" fill="#FFFFFF" />
    <circle cx="125" cy="186" r="11" fill="#FFFFFF" />
  </g>

  <!-- Title Text -->
  <g class="bold-condensed" transform="translate(370, 142)">
    <text x="0" y="0" font-size="52" letter-spacing="1.5">ОБ'ЄКТ</text>
    <text x="0" y="{line2_y_offset}" font-size="{line2_font_size}" letter-spacing="0.5">{title_line2}</text>
    <text x="0" y="134" font-size="52" letter-spacing="1.5">УКРИТТЯМ!</text>
  </g>

  <!-- ================= DIVIDER LINE ================= -->
  <line x1="55" y1="355" x2="945" y2="355" stroke="#111111" stroke-width="5" />

  <!-- ================= BOTTOM SECTION ================= -->
  <!-- Left: "Найближче укриття знаходиться за адресою:" -->
  <g class="addr-title" transform="translate(65, 435)">
    <text x="0" y="0">Найближче укриття</text>
    <text x="0" y="38">знаходиться за адресою:</text>
  </g>

  <!-- Right: Address Details -->
  <g transform="translate(425, 435)">
    <text class="addr-text" x="0" y="0">пр-т Відрадний, 16/50</text>
    <text class="addr-sub" x="0" y="40">у цьому будинку (біля 8-го під'їзду)</text>
  </g>

</svg>
'''
    svg_path = os.path.join(OUT_DIR, f"{filename_base}.svg")
    pdf_path = os.path.join(OUT_DIR, f"{filename_base}.pdf")
    tif_path = os.path.join(OUT_DIR, f"{filename_base}.tif")
    
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)
    
    cmd = [
        "rsvg-convert",
        "-f", "pdf",
        "-o", pdf_path,
        "--page-width", "1000mm",
        "--page-height", "600mm",
        "-w", "1000mm",
        "-h", "600mm",
        "-b", "#FFFFFF",
        svg_path
    ]
    subprocess.run(cmd, check=True)
    print(f"Generated PDF: {pdf_path}")
    
    convert_pdf_to_tiff_cmyk(pdf_path, tif_path, dpi=150)
    return pdf_path, tif_path, svg_path

# -------------------------------------------------------------
# POSTER 2: ЖИВИЙ ЗРАЗОК (УВАГА! ШАНОВНІ КЛІЄНТИ!)
# -------------------------------------------------------------
def make_poster2():
    filename_base = "poster_2_uvaga_kliyenty"
    
    # EXACT USER-PROVIDED VECTOR SVG
    user_megaphone_markup = '''
  <!-- User-provided Vector Megaphone -->
  <g id="user-megaphone" transform="translate(195, 25) scale(0.26)">
    <path fill="#333" fill-rule="nonzero" d="M402.812 182.968c-217.191-596.587 192.196 527.965 0 0zM.008 282.185c-.347-30.717 11.293-58.339 38.451-69.204 1.007-1.521 1.996-2.7 3.756-4.174 3.137-2.633 5.986-3.412 9.675-4.819C182.096 156.09 232.065 81.455 260.485 39.008c8.297-12.391 14.915-22.275 21.744-29.092 3.787-3.782 6.766-6.213 11.242-7.894 4.628-1.738 8.934-1.896 14.932-.932 13.17 2.114 26.678 10.899 39.881 24.577 29.237 30.287 60.067 87.689 81.809 147.411 21.847 60.015 34.777 123.219 28.092 164.834-2.755 17.163-8.831 31.248-18.889 40.957l-.015-.016a14.568 14.568 0 01-1.917 1.55c-6.909 4.695-13.426 6.52-20.17 6.777-5.83.224-10.934-.768-16.606-1.946-10.214-2.122-19.99-4.91-30.529-7.914-34.313-9.782-77.12-21.978-145.136-13.998-1.355 4.506-2.35 9.319-2.392 13.615-.027 2.857.262 5.124 1.094 5.886l1.15 1.048c6.365 5.79 9.501 8.636 11.381 15.661 1.466 5.494.853 10.227-.353 19.544l-.404 3.136c-.679 5.345 2.066 6.518 4.808 7.686 8.034 3.426 16.068 6.851 20.424 18.483a14.46 14.46 0 01.978 8.592c-3.49 17.929-14.072 27.027-24.648 36.121-2.079 1.787-4.161 3.579-6.02 5.339l-.025-.026c-.3.284-.613.559-.942.822-25.219 20.166-42.758 14.158-56.326-2.811-8.65-10.816-14.128-25.92-19.241-40.018l-2.104-5.71c-7.3-19.758-12.777-43.381-18.312-67.97l-1.394.429a774.382 774.382 0 00-16.738 5.168c-.548.175-.833.29-1.065.382-4.974 1.978-7.47 2.966-11.478 1.53-33.127 8.506-60.671-7.634-79.174-33.526-7.553-10.569-13.529-22.835-17.64-35.615C2.415 308.376.153 295.016.008 282.185z"/>
    <path fill="#EDECF1" d="M48.129 224.977c-68.53 20.161-23.638 177.137 56.636 149.671 3.091 1.932 3.048 1.022 6.66-.142a747.833 747.833 0 0133.346-9.933c6.645 29.302 12.675 58.117 21.173 81.116 10.84 29.337 22.131 68.508 54.994 42.229 10.366-9.816 23.234-17.381 26.405-33.672-5.275-15.828-29.801-6.495-26.322-33.853 2.409-18.946 2.94-17.593-7.171-26.827-10.238-9.352-4.905-30.609.43-43.519 35.695-4.94 64.884-4.644 89.641-1.854-31.356-35.466-53.557-73.01-67.28-112.163-13.772-39.295-18.964-80.035-16.269-121.767-34.121 35.771-84.524 74.319-163.48 103.366-6.425 2.365-5.1 1.504-8.763 7.348z"/>
    <path fill="#333" fill-rule="nonzero" d="M359.598 374.605c-8.545-2.353-38.568-8.094-44.078-13.823-37.545-39.132-63.522-80.935-78.879-124.752-15.969-45.566-20.405-93.074-14.381-141.819.013.001 2.553-6.582 2.956-7.104 9.569-12.413 19.14-26.092 27.842-38.528 11.83-16.907 22.151-31.656 29.171-38.663 3.787-3.782 6.766-6.213 11.242-7.894 4.628-1.738 8.934-1.896 14.932-.932 13.17 2.114 26.678 10.899 39.881 24.577 29.237 30.287 60.067 87.689 81.809 147.411 21.847 60.015 34.777 123.219 28.092 164.834-2.755 17.163-8.831 31.248-18.889 40.957l-.015-.016a14.568 14.568 0 01-1.917 1.55c-6.91 4.697-13.428 6.518-20.17 6.775-5.832.224-10.934-.767-16.606-1.944-9.698-2.015-25.14-6.267-40.99-10.629z"/>
    <path fill="#FD6974" d="M325.978 350.723c14.694 3.485 34.903 9.262 52.241 13.954-35.477-35.542-64.45-90.148-84.041-146.05-20.91-59.671-31.192-121.716-27.392-164.393-9.375 13.391-19.851 28.459-30.089 41.739-11.321 91.591 15.853 178.217 89.281 254.75z"/>
    <path fill="#DBD9E5" d="M144.628 364.458c5.525 24.562 14.126 61.771 21.316 81.231 10.839 29.337 22.131 68.508 54.994 42.229 10.366-9.816 23.234-17.381 26.405-33.672-5.275-15.828-29.801-6.495-26.322-33.853 2.409-18.946 2.94-17.593-7.171-26.827-9.858-9.004-5.28-29.043-.164-42.044 13.381-6.566 49.716-7.206 89.724-3.219-25.144-28.452-44.149-55.033-61.129-96.489-38.28 33.581-59.372 79.064-97.653 112.644z"/>
    <path fill="#333" fill-rule="nonzero" d="M274.829 20.012c2.38-5.696 5.618-10.166 9.606-13.488 8.913-7.426 19.577-8.306 31.311-3.687 8.464 3.334 17.63 9.88 27.011 18.999 21.114 20.518 45.152 55.812 65.117 96.91 25.42 52.323 46.094 114.063 53.328 163.758 3.558 24.438 3.892 46.367.023 63.482-4.662 20.631-15.215 34.882-33.057 39.815-6.117 1.689-12.814 2.147-20.108 1.236a14.48 14.48 0 01-7.69-3.382c-45.607-32.618-82.664-97.893-106.192-165.028-27.581-78.704-36.678-161.551-19.349-198.615z"/>
    <path fill="#fff" d="M288.225 25.624c14.866-35.699 68.106 20.245 106.576 99.431C447.244 233 478.894 381.239 409.822 372.6 315.864 306.748 258.123 87.821 288.225 25.624z"/>
    <path fill="#EDECF1" d="M403.564 143.912c46.963 105.514 71.386 236.834 6.258 228.688-29.31-20.542-55.094-55.983-75.789-96.913-37.74-86.051-53.578-187.205-34.64-226.333 14.559-34.962 65.92 17.977 104.171 94.558z"/>
    <path fill="#333" d="M366.848 221.162c0 22.754-27.78 68.398-37.167 48.868-14.435-30.035-26.172-61.078-33.599-94.307-2.371-10.656 70.766-9.243 70.766 45.439z"/>
  </g>
  <!-- 5 Radiating Sound Rays matching style -->
  <g stroke="#333333" stroke-width="6" stroke-linecap="round">
    <line x1="325" y1="42" x2="345" y2="28" />
    <line x1="337" y1="60" x2="361" y2="48" />
    <line x1="343" y1="80" x2="369" y2="72" />
    <line x1="343" y1="102" x2="368" y2="99" />
    <line x1="336" y1="122" x2="359" y2="124" />
  </g>
'''
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000mm" height="600mm" viewBox="0 0 1000 600">
  <defs>
    <style>
      .font-header {{
        font-family: "Arial Black", "Arial", "Helvetica Neue", sans-serif;
        font-weight: 900;
      }}
      .font-body {{
        font-family: "Arial", "Helvetica Neue", sans-serif;
        font-weight: 700;
      }}
    </style>
  </defs>

  <!-- Background -->
  <rect width="1000" height="600" fill="#FFFFFF" />

  <!-- Outer Border Frame -->
  <rect x="25" y="25" width="950" height="550" rx="25" ry="25" fill="none" stroke="#222222" stroke-width="6" />

  <!-- ================= TOP HEADER ================= -->
  {user_megaphone_markup}

  <!-- Red Big Word "УВАГА!" -->
  <text class="font-header" x="415" y="132" font-size="78" fill="#C62828" letter-spacing="4">УВАГА!</text>

  <!-- ================= MAIN NOTICE TEXT ================= -->
  <g class="font-body" fill="#212121" text-anchor="middle">
    <!-- Greeting -->
    <text class="font-header" x="500" y="200" font-size="44" letter-spacing="0.5">Шановні клієнти!</text>

    <!-- Message Lines (5 lines) -->
    <text x="500" y="252" font-size="34">У випадку оголошення</text>
    <text x="500" y="296" font-size="34">повітряної тривоги, просимо</text>
    <text x="500" y="340" font-size="34" font-weight="900" fill="#B71C1C">негайно покинути приміщення</text>
    <text x="500" y="384" font-size="34" font-weight="900" fill="#111111">та пройти в укриття!</text>
  </g>

  <!-- ================= SEPARATOR LINE ================= -->
  <line x1="100" y1="420" x2="900" y2="420" stroke="#CCCCCC" stroke-width="3" stroke-linecap="round" />

  <!-- ================= BOTTOM LOCATION / SHELTER INFO ================= -->
  <text class="font-body" x="500" y="454" font-size="24" fill="#424242" text-anchor="middle" font-weight="bold">
    Найближче укриття знаходиться за адресою:
  </text>

  <!-- Shelter Card / Callout Box -->
  <g transform="translate(100, 472)">
    <rect x="0" y="0" width="800" height="85" rx="14" fill="#F5F5F5" stroke="#E0E0E0" stroke-width="2" />
    
    <!-- Shelter Icon Badge -->
    <rect x="22" y="12" width="60" height="60" rx="12" fill="#795548" />
    <path d="M 52,24 L 69,39 L 64,39 L 64,58 L 40,58 L 40,39 L 35,39 Z" fill="#FFFFFF" />
    <rect x="47" y="46" width="10" height="12" fill="#795548" />

    <!-- Address Text -->
    <g transform="translate(100, 38)">
      <text class="font-header" x="0" y="0" font-size="27" fill="#1A1A1A">
        Підвал: <tspan fill="#000000">пр-т Відрадний, 16/50</tspan>
        <tspan font-family="Arial" font-size="23" font-weight="bold" fill="#616161"> (у цьому будинку)</tspan>
      </text>
      <text class="font-body" x="0" y="30" font-size="22" fill="#C62828" font-weight="bold">
        ➔ Вхід навпроти 8-го під'їзду
      </text>
    </g>
  </g>

</svg>
'''
    svg_path = os.path.join(OUT_DIR, f"{filename_base}.svg")
    pdf_path = os.path.join(OUT_DIR, f"{filename_base}.pdf")
    tif_path = os.path.join(OUT_DIR, f"{filename_base}.tif")
    
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)
    
    cmd = [
        "rsvg-convert",
        "-f", "pdf",
        "-o", pdf_path,
        "--page-width", "1000mm",
        "--page-height", "600mm",
        "-w", "1000mm",
        "-h", "600mm",
        "-b", "#FFFFFF",
        svg_path
    ]
    subprocess.run(cmd, check=True)
    print(f"Generated PDF: {pdf_path}")
    
    convert_pdf_to_tiff_cmyk(pdf_path, tif_path, dpi=150)
    return pdf_path, tif_path, svg_path

if __name__ == "__main__":
    make_poster1(is_provided=True)
    make_poster1(is_provided=False)
    make_poster2()
    print("ALL FILES GENERATED WITH USER EXACT SVG CODE!")
