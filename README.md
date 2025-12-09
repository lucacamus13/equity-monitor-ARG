# Equity Monitor ARG

Este proyecto en Python permite monitorear semanalmente el estado de valuación de las principales acciones argentinas listadas en el exterior, utilizando datos financieros extraídos con `yfinance`.
![Título del gráfico](images/monitor.png)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lucacamus13/equity-monitor-ARG/blob/main/Equity_Monitor_Enhanced.ipynb)

## Objetivo

Automatizar un reporte de equity semanal para:

- Evaluar empresas argentinas mediante múltiplos clave (EV/EBITDA, P/E, P/B, etc.).
- Comparar valuaciones contra promedios históricos y sectoriales.
- Detectar oportunidades o anomalías en la valuación de mercado.
- Facilitar la publicación de informes en redes sociales (GitHub / LinkedIn).

## Herramientas Utilizadas

- Python 3.10+
- Yahoo Finance API (`yfinance`)
- Pandas / Numpy
- Matplotlib / Seaborn
- Plotly (opcional para gráficos interactivos)
- Google Colab

## Algunos Múltiplos Analizados

- EV/EBITDA
- Price to Earnings (P/E)
- Price to Book (P/B)
- Market Cap / Ventas
- Otros según disponibilidad del ticker

## Estructura del Proyecto

- `equity_monitor.py`: Módulo principal con la clase `EquityMonitor`.
- `run_analysis.py`: Script para ejecutar el análisis y generar el reporte.
- `Equity_Monitor_Enhanced.ipynb`: Notebook mejorado listo para ejecutar en Google Colab.
- `/images`: Carpeta donde se guardan las visualizaciones exportadas.
- `README.md`: Este archivo de documentación.

## Ejecución en Google Colab

Para ejecutar este proyecto en Google Colab, haz clic en el botón "Open in Colab" de arriba, o sigue estos pasos manualmente:

1.  **Usar el Notebook Mejorado**:
    -   Abre `Equity_Monitor_Enhanced.ipynb` en GitHub y haz clic en el botón "Open in Colab" (si tienes la extensión) o copia la URL y ábrela en [colab.research.google.com](https://colab.research.google.com/).
    -   Ejecuta las celdas secuencialmente. El notebook instalará las dependencias necesarias y ejecutará el análisis.

2.  **Usar los Scripts Python**:
    -   Abre un nuevo notebook en Colab.
    -   Clona este repositorio:
        ```python
        !git clone https://github.com/lucacamus13/equity-monitor-ARG.git
        %cd equity-monitor-ARG
        ```
    -   Instala las dependencias:
        ```python
        !pip install pandas yfinance matplotlib numpy
        ```
    -   Ejecuta el script:
        ```python
        !python run_analysis.py
        ```

## Próximas mejoras

- Automatizar modelos de valuación DCF.
- Dashboard interactivo con Streamlit.
- Scoring de acciones por múltiplos y momentum. (Implementado)
- Exportación semanal a PDF + Post en LinkedIn.

## Contribuciones

Este proyecto está en desarrollo. Si te interesa colaborar, proponer mejoras o integraciones, no dudes en abrir un `issue` o enviar un `pull request`.

## Contacto

Luca Camus, estudiante de economía y algunas cositas de finanzas.
 [LinkedIn](https://www.linkedin.com/in/luca-camus/)  
 luca.camus@fce.uncu.edu.ar
