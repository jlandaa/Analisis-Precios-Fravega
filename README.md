# 📊 Retail Competitiveness & Pricing Strategy: End-to-End Data Pipeline

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=databricks&logoColor=white)]()
[![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)]()

## 📌 Visión General del Proyecto
Este proyecto es una solución integral de Business Intelligence diseñada para monitorear la competitividad diaria en el sector retail. A través de un pipeline automatizado, se realiza web scraping para extraer precios, stock y descuentos del e-commerce de **Frávega** (enfocado en las categorías de tecnología y electrodomésticos). Los datos se procesan en la nube y se disponibilizan en un dashboard interactivo para analizar su estrategia comercial.

🔗 **[Ver Dashboard Interactivo (Publicado en Power BI)](https://app.powerbi.com/view?r=eyJrIjoiNjljMGY0NDUtYjBjMC00ODkxLWFjYWYtNzU3ZDkxN2QwOWE3IiwidCI6IjZjYmMyOTllLWIxZDUtNDJjZi1hMWRjLTgwNjZmMTdiN2QwNyIsImMiOjR9)**


## 💼 Impacto de Negocio
En la industria del retail, la agilidad para ajustar precios frente a la competencia define la cuota de mercado. Esta herramienta permite a los equipos de Pricing y Comercial:
* **Analizar la agresividad de descuentos** por categoría de producto (Audio, Climatización, Smartphones, etc.).
* **Monitorear el posicionamiento de marcas** (ej. Samsung, Motorola, LG) frente a rebajas de competidores.
* **Detectar oportunidades de margen** mediante el análisis de dispersión entre el precio regular y el precio de oferta.

## 🏗️ Arquitectura de la Solución (ETL)

El pipeline de datos está construido en tres fases principales:

### 1. Extracción (Web Scraping con Python)
* Script desarrollado en **Python** para navegar y parsear el sitio web de **Frávega**.
* Extracción diaria de su catálogo de productos, capturando variables clave: SKU original, Marca, Categoría, Precio Regular, Precio de Oferta y URL del producto.
* Manejo de la estructura HTML específica del sitio, resolviendo la paginación y realizando la limpieza inicial de strings para los nombres de los productos.

### 2. Transformación (Databricks & SQL)
* Ingesta de los datos crudos en el entorno de **Databricks**.
* Procesamiento y transformación utilizando **SQL** y **PySpark** para generar el modelo dimensional.
* Creación de la tabla de hechos (`fact_precios_diarios`) y dimensiones (`dim_producto`), asegurando la integridad referencial y calculando métricas derivadas (ej. `% de Descuento`).

### 3. Visualización (Microsoft Power BI)
* Conexión directa al modelo semántico limpio.
* Diseño de un reporte de nivel ejecutivo aplicando mejores prácticas de **Data Storytelling** y UX.
* Medidas DAX optimizadas para el cálculo de promedios de venta y volumen de artículos relevados.

## 📂 Estructura del Repositorio
```text
├── dashboard/              # Archivo .pbix original del dashboard interactivo
├── notebooks/              # Notebooks de Databricks con la lógica de transformación (SQL/PySpark)
├── scraper/                # Scripts de Python para la extracción diaria de datos
├── README.md               # Documentación del proyecto
└── requirements.txt        # Dependencias de Python para ejecutar el scraper
```

## 1. 🚀 Cómo ejecutar este proyecto localmente
Clonar el repositorio:
```bash
git clone [https://github.com/tu-usuario/retail-pricing-pipeline.git](https://github.com/tu-usuario/retail-pricing-pipeline.git)
```
## 2. Instalar dependencias de Python:
```bash
pip install -r requirements.txt
```
## 3. Ejecutar el scraper:
```bash
python scraper/Fravega_Completo.py
```
## 4. Subir los datos resultantes a Databricks y ejecutar el notebook
```text
notebooks/Scraping_Retail.ipynb
```


## 👨‍💻 Sobre mí
**Juan Manuel Landa**
* **Ingeniero en Computación** | **Data Analyst & BI Consultant**
* 📍 Quilmes, Buenos Aires, Argentina
* 💼 [LinkedIn](https://ar.linkedin.com/in/juan-manuel-landa/en)
* 🌐 [Portfolio Personal](https://juan-manuel-landa.netlify.app/)

Este proyecto forma parte de mi búsqueda activa de nuevas oportunidades en el área de **Data & Business Intelligence**.
