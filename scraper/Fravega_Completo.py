import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re
import os
import glob
from datetime import datetime, timedelta

# ==========================================
# 1. LISTA DE CATEGORÍAS
# ==========================================
categorias_estrategicas = [
    # --- TECNOLOGÍA ---
    {"url": "https://www.fravega.com/l/celulares/celulares-liberados/", "nombre": "Smartphones"},
    {"url": "https://www.fravega.com/l/tv-y-video/tv/", "nombre": "Televisores"},
    {"url": "https://www.fravega.com/l/informatica/notebooks/", "nombre": "Notebooks"},
    {"url": "https://www.fravega.com/l/videojuegos/", "nombre": "Gaming y Videojuegos"}, # NUEVA: Clave para análisis de precios altos
    
    # --- ELECTRODOMÉSTICOS ---
    {"url": "https://www.fravega.com/l/heladeras-freezers-y-cavas/", "nombre": "Heladeras"},
    {"url": "https://www.fravega.com/l/lavado/", "nombre": "Lavado"},
    {"url": "https://www.fravega.com/l/climatizacion/aire-acondicionado/", "nombre": "Aires Acondicionados"},
    {"url": "https://www.fravega.com/l/pequenos-electrodomesticos/", "nombre": "Pequeños Electrodomésticos"}, # NUEVA: Mueve mucho volumen (licuadoras, pavas, etc.)
    
    # --- HOGAR Y ESTILO DE VIDA ---
    {"url": "https://www.fravega.com/l/muebles/", "nombre": "Muebles"},
    {"url": "https://www.fravega.com/l/colchones-y-sommiers/", "nombre": "Colchones y Sommiers"}, # NUEVA: Muchísima guerra de descuentos acá
    {"url": "https://www.fravega.com/l/deportes-y-fitness/", "nombre": "Deportes y Fitness"},
    {"url": "https://www.fravega.com/e/belleza-y-cuidado-personal/", "nombre": "Belleza y Cuidado Personal"},
    {"url": "https://www.fravega.com/l/herramientas/", "nombre": "Herramientas"},
    
    # --- ENTRETENIMIENTO Y NIÑOS ---
    {"url": "https://www.fravega.com/l/audio/", "nombre": "Audio"},
    {"url": "https://www.fravega.com/l/juguetes-y-juegos/", "nombre": "Juguetes"},
    
    # ---BEBÉS---
   {"url": "https://www.fravega.com/l/bebes-y-primera-infancia/cochecitos/", "nombre": "Bebés y Primera Infancia"},
    {"url": "https://www.fravega.com/l/bebes-y-primera-infancia/cunas-practicunas-y-corralitos/", "nombre": "Bebés y Primera Infancia"}
]

# ==========================================
# 2. DICCIONARIO DE MARCAS
# ==========================================
marcas_conocidas = [
    'SAMSUNG', 'MOTOROLA', 'APPLE', 'XIAOMI', 'TCL', 'LG', 'PHILIPS', 'NOBLEX', 
    'HISENSE', 'BGH', 'SONY', 'LENOVO', 'HP', 'DELL', 'ASUS', 'ACER', 'WHIRLPOOL', 
    'DREAN', 'PHILCO', 'MABE', 'GAFA', 'PATRICK', 'OSTER', 'LILIANA', 'ATMA', 
    'MIDEA', 'SURREY', 'ALCATEL', 'ZTE', 'BANGHO', 'PIONEER', 'BOSCH', 'BLACK+DECKER',
    'GAMA', 'REMINGTON', 'CHICCO', 'KIDDY', 'MACLAREN'
]

def aplicar_politica_retencion(carpeta='data', dias_retencion=30):
    print(f"\n🧹 Iniciando limpieza de CSVs mayores a {dias_retencion} días...")
    if not os.path.exists(carpeta): return
    fecha_limite = datetime.now() - timedelta(days=dias_retencion)
    archivos_csv = glob.glob(f"{carpeta}/fravega_*.csv")
    eliminados = 0
    for archivo in archivos_csv:
        try:
            nombre_base = os.path.basename(archivo)
            fecha_str = nombre_base.replace('fravega_', '').replace('.csv', '')
            if datetime.strptime(fecha_str, '%Y-%m-%d') < fecha_limite:
                os.remove(archivo)
                eliminados += 1
                print(f"   🗑️ Eliminado: {nombre_base}")
        except: pass
    print(f"   ✅ Limpieza exitosa: {eliminados} eliminados." if eliminados > 0 else "   ✨ Nada para limpiar hoy.")

def extraer_fravega_robusto(max_paginas=5):
    # Recuperamos la clave secreta desde GitHub Actions
    API_KEY = os.environ.get('SCRAPER_API_KEY')
    if not API_KEY:
        print("❌ ERROR: No se encontró la SCRAPER_API_KEY en las variables de entorno.")
        return

    datos_totales = []

    for cat in categorias_estrategicas:
        url_base = cat["url"]
        nombre_categoria = cat["nombre"]
        sub_categoria = url_base.strip('/').split('/')[-1].replace('-', ' ').title()
        print(f"\n🚀 PROCESANDO: {nombre_categoria.upper()} ({sub_categoria})")
        
        for p in range(1, max_paginas + 1):
            url = url_base if p == 1 else f"{url_base}?page={p}"
            
            # 🚀 MEJORA NIVEL ARQUITECTO: Sistema de Reintentos (Retries)
            max_reintentos = 3
            exito_conexion = False
            
            for intento in range(max_reintentos):
                try:
                    time.sleep(random.uniform(2, 5))
                    # 🚀 Pasamos la petición por ScraperAPI
                    payload = {'api_key': API_KEY, 'url': url, 'country_code': 'ar'}
                    response = requests.get('http://api.scraperapi.com', params=payload, timeout=60)
                    
                    if response.status_code == 200:
                        exito_conexion = True
                        break # ¡La conexión funcionó! Salimos del bucle de reintentos
                    else:
                        print(f"  ⚠️ Status {response.status_code} (Intento {intento + 1}/{max_reintentos}). Reintentando en 3s...")
                        time.sleep(3)
                        
                except requests.exceptions.RequestException as e:
                    # Atrapamos micro-cortes, timeouts y "Response ended prematurely"
                    print(f"  🔄 Micro-corte detectado (Intento {intento + 1}/{max_reintentos}). Esperando 5s para reintentar...")
                    time.sleep(5) 
            
            # Si después de los 3 intentos no logró conectarse, abortamos la página
            if not exito_conexion:
                print(f"  ❌ Se agotaron los {max_reintentos} reintentos. Saltando a la siguiente categoría por seguridad.")
                break 

            # Parseo HTML
            try:
                soup = BeautifulSoup(response.text, 'html.parser')
                enlaces_productos = soup.find_all('a', href=re.compile(r'/p/'))
                
                urls_vistas = set()
                productos_en_pagina = 0
                
                for link in enlaces_productos:
                    url_producto = link['href']
                    if not url_producto.startswith('http'):
                        url_producto = f"https://www.fravega.com{url_producto}"
                        
                    if url_producto in urls_vistas: continue
                    urls_vistas.add(url_producto)

                    contenedor = link.find_parent(['article', 'div', 'li'])
                    if not contenedor: continue

                    # 1. Extraer SKU
                    partes_url = [part for part in url_producto.split('?')[0].split('/') if part]
                    sku_crudo = partes_url[-1] if partes_url else str(hash(url_producto))
                    sku_final = f"FRA-{sku_crudo[:40]}"

                    # 🚀 MEJORA 1: Extraer el Nombre del Producto sin la basura de precios
                    nombre_bruto = link.text.strip()
                    
                    # Usamos una expresión regular para cortar el texto cuando aparece el signo $, "Vendido por" o "Llega en"
                    nombre_limpio = re.split(r'\$|Vendido por|Precio s/imp|Llega en|Retiralo', nombre_bruto)[0].strip()
                    nombre_producto = nombre_limpio
                    
                    if len(nombre_producto) < 5:
                        span_titulo = contenedor.find('span', string=re.compile(r'[a-zA-Z]'))
                        nombre_producto = span_titulo.text.strip() if span_titulo else sku_crudo.replace('-', ' ').title()

                    # 2. Detección de Marca
                    marca = "OTRAS"
                    for m in marcas_conocidas:
                        if m.lower() in url_producto.lower() or m.lower() in nombre_producto.lower():
                            marca = m
                            break

                    # 🚀 MEJORA 2: Extraer Cuotas (Si existen)
                    texto_cuotas = contenedor.find(string=re.compile(r'(?i)cuotas?'))
                    cuotas_detectadas = 1
                    if texto_cuotas:
                        nums_cuota = re.findall(r'\d+', texto_cuotas)
                        if nums_cuota: cuotas_detectadas = int(nums_cuota[0])

                    # 3. Extracción de Precios (Parseo Argentino + Filtro de Impuestos)
                    textos_precios = contenedor.find_all(string=re.compile(r'\$'))
                    valores = []
                    
                    for t in textos_precios:
                        texto_limpio = t.lower()
                        # Ignoramos si el texto habla de cuotas, envío o impuestos
                        if 'imp' in texto_limpio or 'cuota' in texto_limpio or 'envío' in texto_limpio:
                            continue
                            
                        # Extraemos el número respetando puntos y comas
                        match = re.search(r'\$\s*([\d\.,]+)', t)
                        if match:
                            num_str = match.group(1)
                            # Quitamos el punto de los miles y cambiamos la coma por punto decimal
                            num_str = num_str.replace('.', '').replace(',', '.')
                            try:
                                valores.append(float(num_str))
                            except:
                                pass
                    
                    hay_stock = True
                    precio_regular = 0.0
                    precio_oferta = 0.0

                    if not valores:
                        # Si no hay precio, asumimos que no hay stock (Agotado)
                        hay_stock = False
                    else:
                        valores_unicos = sorted(list(set(valores)), reverse=True)
                        if len(valores_unicos) >= 2:
                            precio_regular = valores_unicos[0]
                            precio_oferta = valores_unicos[1]
                        else:
                            precio_regular = valores_unicos[0]
                            precio_oferta = valores_unicos[0]

                    # Guardamos el registro
                    datos_totales.append({
                        "sku_original": sku_final,
                        "competidor": "Fravega",
                        "marca": marca,
                        "categoria": nombre_categoria,
                        "nombre_producto": nombre_producto,
                        "url_producto": url_producto,
                        "precio_regular": precio_regular,
                        "precio_oferta": precio_oferta,
                        "cuotas": cuotas_detectadas,
                        "hay_stock": hay_stock
                    })
                    productos_en_pagina += 1
                
                if productos_en_pagina == 0:
                    print(f"  🏁 Fin del catálogo en página {p}.")
                    break
                else:
                    print(f"  ✅ {productos_en_pagina} productos capturados en pág {p}.")
                    
            except Exception as e:
                print(f"  ❗ Error en el parseo de datos: {str(e)[:50]}")
                break

    if datos_totales:
        df = pd.DataFrame(datos_totales)
        carpeta_destino = 'data'
        os.makedirs(carpeta_destino, exist_ok=True)
        nombre_archivo = f"{carpeta_destino}/fravega_{datetime.now().strftime('%Y-%m-%d')}.csv"
        df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig')
        print(f"\n🏆 EXITOSO: {len(datos_totales)} productos en {nombre_archivo}")
        aplicar_politica_retencion(carpeta_destino, 30)
    else:
        print("\n❌ No se obtuvieron datos.")

if __name__ == "__main__":
    extraer_fravega_robusto(max_paginas=5)
