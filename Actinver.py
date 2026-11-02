import yfinance as yf
import pandas as pd
import numpy as np
from yfinance.utils import auto_adjust
from scipy.optimize import minimize
import openpyxl
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", category=pd.errors.Pandas4Warning)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


path = DATA_DIR / "ACTINBLUE1_final.xlsx"
actinver_var_path = DATA_DIR / "ACTINVER_Variable_5y.xlsx"
actiner_fijo_path = DATA_DIR / "ACTINVER_precios_fijos.xlsx"

ftse_wgbi_path = DATA_DIR / "Price_FTSE_WGBI.xlsx"
fibras_path = DATA_DIR / "Price_FIBRAS_INDEX.xlsx"

tickers_benchmark = ["^GSPC", "^MXX"]

tickers_ETFs_fijo = ["DIABLOI10.MX", "ANGELD10.MX", "BIL", "SHV", "SHY", "TLT"]


tickers_ETFs_variable = ["FAZ", "SOXS", "TZA", "AAXJ", "ACWI", "BOTZ", "DIA", "EEM", "EWZ", #Tickers de ETF's internacionales de renta variable
    "FAS", "GDX", "GLD", "IAU", "ICLN", "INDA", "IVV", "KWEB", "LIT",
    "MCHI", "PSQ", "QCLN", "QLD", "QQQ", "SLV", "SOXL", "SOXX", "SPYM",
    "SPXL", "SPXS", "SPY", "SQQQ", "TAN", "TECL", "TECS", "TNA", "TQQQ",
    "USO", "VEA", "VGT", "VNQ", "VOO", "VT", "VTI", "VWO", "VYM",
    "XLE", "XLF", "XLK", "XLV"]

tickers_acciones_nacionales = ["ACTINVRB.MX", "SIGMAFA.MX", "ALPEKA.MX", "ALSEA.MX", #Tickers de acciones nacionales de renta variable
    "AMXB.MX", "ASURB.MX", "BIMBOA.MX", "BOLSAA.MX", "CEMEXCPO.MX",
    "CHDRAUIB.MX", "CUERVO.MX", "KOFUBL.MX", "GAPB.MX",
    "GCARSOA1.MX", "GCC.MX", "GENTERA.MX", "GFINBURO.MX", "GFNORTEO.MX",
    "GMEXICOB.MX", "GRUMAB.MX", "KIMBERA.MX", "KOFUBL.MX", "LABB.MX", "LIVEPOLC-1.MX", "MEGACPO.MX", "MFRISCOA-1.MX", "OMAB.MX",
    "ORBIA.MX", "PE&OLES.MX", "PINFRA.MX", "Q.MX", "RA.MX", "TLEVISACPO.MX", "VESTA.MX", "VOLARA.MX", "WALMEX.MX",
    "BBAJIOO.MX"]

tickers_acciones_int = ["AAL", "AAPL", "ABBV", "ABNB", "AFRM", "AGNC", "AMAT", "AMD", "AMZN", #Tickers de acciones internacionales
    "AVGO", "AXP", "BA", "BABAN.MX", "BAC", "BMY", "BRK-B", "C", "CAT",
    "CCL1N.MX", "CLF", "COST", "CRM", "CSCO", "CVS", "CVX", "DAL",
    "DIS", "DVN", "ETSY", "F", "FANG", "FCX", "FDX", "FSLR", "FUBO"
    , "GM", "GME", "GOOGL", "HD", "INTC", "JNJ", "JPM", "KO",
    "LCID", "LLY", "LUV", "LVS", "MA", "MCD", "MELIN.MX", "META",
    "MRK", "MRNA", "MPC", "MSFT", "MU", "NCLHN.MX", "NFLX", "NKE", "NUN.MX",
    "NVAX", "NVDA", "ORCL", "OXY", "PEP", "PFE", "PG", "PINS",
    "PLTR", "PYPL", "QCOM", "RCL", "RIOT", "RIVN", "SBUX", "SHOPN.MX",
    "SOFI", "SPCE", "T", "TGT", "TMO", "TSLA", "TSMN.MX", "TX", "UAL",
    "UBER", "UNH", "UPST", "V", "VZ", "WFC", "WMT", "XOM", "ZM"]

tickers_fibras = ["FIBRAMQ12.MX", "FIBRAPL14.MX", "FUNO11.MX"]

precios_actinver_variable = pd.read_excel(io=actinver_var_path)
precios_actinver_variable.set_index(precios_actinver_variable.columns[0], inplace=True) #Precios de actinver variable

precios_actinver_fijos = pd.read_excel(io=actiner_fijo_path)
precios_actinver_fijos.set_index(precios_actinver_fijos.columns[0], inplace=True) # Precios de actinver fijo

precios_ftse_wgbi = pd.read_excel(io=ftse_wgbi_path)
precios_ftse_wgbi.set_index(precios_ftse_wgbi.columns[0], inplace=True)

precios_fibras_index = pd.read_excel(io=fibras_path)
precios_fibras_index.set_index(precios_fibras_index.columns[0], inplace=True)

prices_benchmark = yf.download(tickers=tickers_benchmark, start="2021-01-01", end="2026-01-01", auto_adjust=True)["Close"]

prices_benchmark = pd.concat([precios_fibras_index, precios_ftse_wgbi, prices_benchmark], axis=1) # Precios de benchmarks

prices = yf.download(tickers=tickers_ETFs_variable + tickers_acciones_int + tickers_acciones_nacionales + tickers_fibras
                             +tickers_ETFs_fijo, start="2021-01-01", end="2026-01-01",auto_adjust=True)["Close"]
#Precios de ETF's variable y fijos, Acciones Internacionales y nacionales, FIBRAS,
precios_fx = yf.download(tickers="MXN=X", start="2021-01-01", end="2026-01-01", auto_adjust=True)["Close"] #Precios tipo de cambio

prices.drop(columns=["NUN.MX", "RIVN"], inplace=True)
precios_actinver_variable.drop(columns=["PROTEGE.MX", "ACTIRVT.MX"], inplace=True) #Limpiar activos que no aportan nada

# print(prices.count().sort_values())
# print(precios_actinver_fijos.count().sort_values())
# print(precios_actinver_variable.count().sort_values())
# print(prices_benchmark.count().sort_values())

precios_pf = pd.concat([prices, precios_actinver_fijos, precios_actinver_variable, prices_benchmark, precios_fx], axis=1)
precios_pf.ffill(inplace=True)
precios_pf.dropna(inplace=True)

precios_fx = precios_pf["MXN=X"] # Precios de tipo de cambio
precios_benchmark = pd.concat([precios_pf["^MXX"], precios_pf["FIBRAS INDEX"], precios_pf["^GSPC"], precios_pf["FTSE WGBI"]], axis=1) #Precios de benchmarks en pesos

log_rets = np.log(precios_pf / precios_pf.shift(1))

log_rets_fx = log_rets["MXN=X"] # Log_rets de tipo de cambio
log_rets_bm_mx = pd.concat([log_rets["^MXX"],log_rets["FIBRAS INDEX"]], axis=1) # Log_rets de benchmarks en pesos

cols_usd = [col for col in log_rets.columns if ".MX" not in col]
cols_mxn = [col for col in log_rets.columns if ".MX" in col]

log_rets_correcto = pd.concat([log_rets[cols_usd].add(log_rets_fx, axis=0), log_rets[cols_mxn]], axis=1)

log_rets_benchmarks = pd.concat([log_rets_bm_mx, log_rets_correcto["^GSPC"], log_rets_correcto["FTSE WGBI"]], axis=1)
# Log rets de benchmarks en pesos

log_rets_correcto.drop(columns=["^GSPC", "MXN=X", "FTSE WGBI", "^MXX", "FIBRAS INDEX"], inplace=True) # Log rets de puras acciones

precios_pf.drop(columns=["MXN=X", "^MXX", "FIBRAS INDEX", "^GSPC", "FTSE WGBI"], inplace=True) #Precios de puras acciones


renta_fija = ["ACTDUAL.MX", "ACTICO.MX", "ACTIG+.MX", "ACTIG+2.MX", "ACTIGOB.MX", "ACTIMED.MX", "ACTIPLU.MX", "ALTERN.MX",
              "ESCALA.MX", "MAXIMO.MX", "DIABLOI10.MX", "ANGELD10.MX", "BIL", "SHV", "SHY", "TLT"]
renta_variable = []

for col in log_rets_correcto.columns: #aqui puedo usar list comprehension
    if col not in renta_fija:
        renta_variable.append(col)

columns_ordenadas = renta_variable + renta_fija

log_rets_correcto = log_rets_correcto[columns_ordenadas]
log_rets_correcto.dropna(inplace=True)
matriz_cov = log_rets_correcto.cov() * 252

returns = log_rets_correcto
mu = returns.mean() * 252
var = returns.var() * 252
std = returns.std() * np.sqrt(252)

asset_stats = pd.DataFrame({
    "mu": mu,
    "var": var,
    "std": std
})

rf_mask = returns.columns.isin(renta_fija)
rv_mask = returns.columns.isin(renta_variable)
Sigma = returns.cov() * 252
Sigma = Sigma.loc[returns.columns, returns.columns]

n = len(returns.columns)
n_rv = rv_mask.sum()
n_rf = rf_mask.sum()
w0 = np.where(rv_mask, 0.4 / n_rv, 0.6 / n_rf)


def neg_return(w, mu):
    return -(w @ mu)

def var_constraint(w):
    ret_p = w @ mu.values
    sigma_p = np.sqrt(w.T @ Sigma.values @ w)
    VaR = ret_p - 1.645 * sigma_p
    return VaR + 0.025

constraints = [
    {"type": "eq", "fun": lambda w: np.sum(w) - 1},
    {"type": "eq", "fun": lambda w: np.sum(w[rf_mask]) - 0.6},
    {"type": "eq", "fun": lambda w: np.sum(w[rv_mask]) - 0.4},
    {"type": "ineq", "fun": var_constraint}
]

bounds = [(0, 0.1) for _ in range(n)]

res = minimize(
    neg_return,
    w0,
    args=(mu.values,),
    method="SLSQP",
    constraints=constraints,
    bounds=bounds
)
# if not res.success:
#     raise RuntimeError(f"Optimizacion fallida: {res.message}")

weights = pd.Series(res.x, index=returns.columns)
portfolio_ret = weights.values.T @ mu.values
portfolio_var = weights.values.T @ Sigma.values @ weights.values
portfolio_vol = np.sqrt(portfolio_var)
VaR = portfolio_ret - 1.645 * portfolio_vol


print(f"Retorno Anual: {portfolio_ret: .4%}")
print(f"Volatilidad Anual {portfolio_vol: .4%}")
print(f"VaR anual 95%: {VaR: .4%}")
print(f"Cumple VaR? {VaR >= -0.025}")
print(weights[weights > 0.001].sort_values(ascending=False))

# with pd.ExcelWriter(path=path, engine="openpyxl") as writer:
#     precios_pf.to_excel(writer, sheet_name="Precios Activos")
#     precios_benchmark.to_excel(writer, sheet_name="Precios Benchmark")
#     precios_fx.to_excel(writer, sheet_name="Precios MXN-USD")
# 
#     log_rets_correcto.to_excel(writer, sheet_name="Log_rets_activos")
#     log_rets_fx.to_excel(writer, sheet_name="Log_rets MXN-USD")
#     log_rets_benchmarks.to_excel(writer, sheet_name="Log-rets Benchmark")
#
#     asset_stats.to_excel(writer, sheet_name="Indicadores")
#
#     matriz_cov.to_excel(writer, sheet_name="Matriz de Covarianza")
#
#     weights.to_excel(writer, sheet_name="Portafolio")