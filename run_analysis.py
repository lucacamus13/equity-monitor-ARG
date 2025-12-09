from equity_monitor import EquityMonitor
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# List of symbols from the original notebook
symbols = [
    'BBAR.BA',   # Banco Frances
    'BMA.BA',    # Banco Macro
    'BYMA.BA',   # Bolsas y Mercados Argentina
    'METR.BA',   # Metrogas
    'SUPV.BA',   # Banco Supervielle
    'TGNO4.BA',  # Transporte Gas del Norte
    'TGSU2.BA',  # Transporte Gas del Sur
    'VALO.BA',   # Mercado de Valores de Buenos Aires
    'YPFD.BA',   # YPF
    'ALUA.BA',   # Aluar
    'TXAR.BA',   # Ternium Argentina
    'GGAL.BA',   # Grupo Galicia
    'PAMP.BA',   # Pampa Energía
    'TECO2.BA',  # Telecom Argentina
    'EDN.BA',    # Edenor
    'COME.BA',   # Comercial del Plata
    'LOMA.BA',   # Loma Negra
    'TRAN.BA',   # Transener
    'CRES.BA',   # Cresud
    'IRSA.BA',   # IRSA
    'CEPU.BA',   # Central Puerto
    # Panel General
    'A3.BA',     # Matba Rofex
    'HARG.BA',   # Holcim
    'ECOG.BA',   # Ecogas
    'CVH.BA',    # Cablevision
    'MOLI.BA',   # Molinos
    'MOLA.BA',   # Molinos agro
    'DGCU2.BA',  # Distribuidora gas cuyana
    'LEDE.BA',   # Ledesma
    'SAMI.BA',   # San Miguel
    'CELU.BA',   # Celulosa
    'AGRO.BA',   # Agrometal
    'MIRG.BA',   # Mirgor
    'BHIP.BA',   # Banco Hipotecario
    'BPAT.BA',   # Banco Patagonia
]

def explain_score(row):
    """Provides a text breakdown of why a stock got its score."""
    explanation = []
    pe = row.get('P/E')
    ev_ebitda = row.get('EV/EBITDA')
    roe = row.get('ROE (%)')
    margin = row.get('Margin (%)')
    sma = row.get('Price vs SMA200 (%)')
    rsi = row.get('RSI')

    # Value
    if pe and isinstance(pe, (int, float)) and 0 < pe < 10: explanation.append("P/E atractivo (<10)")
    if ev_ebitda and isinstance(ev_ebitda, (int, float)) and 0 < ev_ebitda < 8: explanation.append("EV/EBITDA bajo (<8)")

    # Quality
    if roe and isinstance(roe, (int, float)) and roe > 20: explanation.append("ROE alto (>20%)")
    if margin and isinstance(margin, (int, float)) and margin > 15: explanation.append("Margen sólido (>15%)")

    # Momentum
    if sma and isinstance(sma, (int, float)) and sma > 0: explanation.append("Tendencia alcista (Sobre SMA200)")
    if rsi and isinstance(rsi, (int, float)) and 40 <= rsi <= 70: explanation.append("RSI saludable")

    return ", ".join(explanation) if explanation else "Métricas neutras o sin datos"

def main():
    print("Initializing Argentina Equity Monitor...")
    monitor = EquityMonitor(symbols)

    # Run analysis
    df = monitor.run_analysis()

    # Display simplified report in console
    print("\n--- Equity Monitor Report (Top Scored) ---")
    monitor.display_report()

    # Show detail for top stock
    if not df.empty:
        top_stock = df.iloc[0]
        print(f"\n[Análisis Profundo] Top Pick: {top_stock['Symbol']} (Score: {top_stock['Score']})")
        print(f"Razón: {explain_score(top_stock)}")

    # Save detailed report to CSV
    monitor.to_csv("equity_report.csv")

if __name__ == "__main__":
    main()
