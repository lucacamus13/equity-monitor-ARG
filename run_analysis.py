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

def main():
    print("Initializing Argentina Equity Monitor...")
    monitor = EquityMonitor(symbols)

    # Run analysis
    df = monitor.run_analysis()

    # Display simplified report in console
    print("\n--- Equity Monitor Report (Top Scored) ---")
    monitor.display_report()

    # Save detailed report to CSV
    monitor.to_csv("equity_report.csv")

if __name__ == "__main__":
    main()
