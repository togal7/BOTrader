import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
import numpy as np
import pandas as pd
from io import BytesIO
import asyncio
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

def smart_price_format(price):
    """Format price - zachowuje wszystkie cyfry znaczące"""
    if price == 0:
        return "0"
    elif price >= 1000:
        return f"${price:,.2f}"
    elif price >= 1:
        return f"${price:.4f}"
    elif price >= 0.01:
        return f"${price:.6f}"
    else:
        return f"${price:.8f}"

def format_axis_price(price):
    """Format for Y axis labels"""
    if price == 0:
        return "0"
    elif price >= 1000:
        return f"{price:,.1f}"
    elif price >= 1:
        return f"{price:.3f}"
    elif price >= 0.01:
        return f"{price:.5f}"
    else:
        return f"{price:.7f}"

class ChartGenerator:
    def __init__(self):
        self.style = {
            'bg': '#0E1117',
            'panel': '#1C2127',
            'text': '#D1D4DC',
            'grid': '#2A2E39',
            'up': '#26A69A',
            'down': '#EF5350',
            'entry': '#FFD700',
            'tp': '#26A69A',
            'sl': '#EF5350',
            'ema1': '#2962FF',
            'ema2': '#FF6D00',
            'volume': '#363A45',
        }

    async def generate_signal_chart(
        self,
        symbol: str,
        timeframe: str,
        ohlcv_data: pd.DataFrame,
        entry_price: float,
        position_type: str = 'LONG',
        tp_levels: Optional[List[float]] = None,
        sl_price: Optional[float] = None,
        support_resistance: Optional[List] = None,
        liquidation_price: Optional[float] = None,
    ) -> bytes:
        try:
            return await asyncio.get_event_loop().run_in_executor(
                None,
                self._generate_sync,
                symbol, timeframe, ohlcv_data, entry_price,
                position_type, tp_levels, sl_price, support_resistance, liquidation_price
            )
        except Exception as e:
            logger.error(f"Chart generation error: {e}")
            raise

    def _generate_sync(self, symbol, timeframe, df, entry_price,
                       position_type, tp_levels, sl_price,
                       support_resistance, liquidation_price):

        s = self.style

        # Oblicz EMA i RSI
        df = df.copy()
        df['EMA20'] = df['close'].ewm(span=20).mean()
        df['EMA50'] = df['close'].ewm(span=50).mean()

        delta = df['close'].diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = (-delta.clip(upper=0)).rolling(14).mean()
        rs = gain / loss.replace(0, np.nan)
        df['RSI'] = 100 - (100 / (1 + rs))

        # === PREDYKCJA KIERUNKU ===
        n_pred = min(20, len(df) // 5)
        last_price = df['close'].iloc[-1]
        last_idx = len(df) - 1

        # Wyznacz predykowany kierunek
        if tp_levels and len(tp_levels) > 0:
            target = tp_levels[-1]
        else:
            target = entry_price * (1.05 if position_type == 'LONG' else 0.95)

        # Generuj krzywą predykcji (paraboliczna)
        pred_x = np.linspace(last_idx, last_idx + n_pred, n_pred + 1)
        mid_y = last_price + (target - last_price) * 0.5
        # Dodaj lekkie wygięcie
        t = np.linspace(0, 1, n_pred + 1)
        if position_type == 'LONG':
            pred_y = last_price + (target - last_price) * (t ** 0.7)
        else:
            pred_y = last_price + (target - last_price) * (t ** 0.7)

        # Zakres niepewności
        spread = abs(target - last_price) * 0.3
        pred_upper = pred_y + spread * t
        pred_lower = pred_y - spread * t

        # === LAYOUT ===
        fig = plt.figure(figsize=(14, 9), facecolor=s['bg'])
        fig.patch.set_facecolor(s['bg'])

        # Gridspec: główny wykres 60%, wolumen 15%, RSI 25%
        gs = fig.add_gridspec(3, 1, height_ratios=[6, 1.5, 2], hspace=0.04)

        ax_main = fig.add_subplot(gs[0])
        ax_vol  = fig.add_subplot(gs[1], sharex=ax_main)
        ax_rsi  = fig.add_subplot(gs[2], sharex=ax_main)

        for ax in [ax_main, ax_vol, ax_rsi]:
            ax.set_facecolor(s['panel'])
            ax.tick_params(colors=s['text'], labelsize=8)
            ax.spines[:].set_color(s['grid'])

        # === ŚWIECE ===
        n = len(df)
        x = np.arange(n)
        w = 0.6

        for i in range(n):
            o = df['open'].iloc[i]
            h = df['high'].iloc[i]
            l = df['low'].iloc[i]
            c = df['close'].iloc[i]
            color = s['up'] if c >= o else s['down']

            # Knot
            ax_main.plot([i, i], [l, h], color=color, linewidth=0.8, zorder=2)
            # Body
            body_h = abs(c - o)
            body_y = min(o, c)
            rect = patches.Rectangle(
                (i - w/2, body_y), w, max(body_h, entry_price * 0.0005),
                facecolor=color, edgecolor=color, linewidth=0.3, zorder=3
            )
            ax_main.add_patch(rect)

        # === EMA ===
        ax_main.plot(x, df['EMA20'], color=s['ema1'], linewidth=1.2,
                     alpha=0.8, label='EMA 20', zorder=4)
        ax_main.plot(x, df['EMA50'], color=s['ema2'], linewidth=1.2,
                     alpha=0.8, label='EMA 50', zorder=4)

        # === PREDYKCJA ===
        ax_main.plot(pred_x, pred_y,
                     color=s['entry'], linewidth=2, linestyle='--',
                     alpha=0.9, label='Predykcja', zorder=5)
        ax_main.fill_between(pred_x, pred_lower, pred_upper,
                             alpha=0.15, color=s['entry'], zorder=4)

        # Strzałka kierunku
        arrow_color = s['up'] if position_type == 'LONG' else s['down']
        ax_main.annotate(
            '',
            xy=(last_idx + n_pred, pred_y[-1]),
            xytext=(last_idx + n_pred * 0.7, pred_y[int(n_pred * 0.7)]),
            arrowprops=dict(
                arrowstyle='->', color=arrow_color,
                lw=2.5, mutation_scale=20
            ),
            zorder=6
        )

        # === LINIE TP / SL / ENTRY ===
        all_prices = []

        # Entry
        ax_main.axhline(y=entry_price, color=s['entry'], linewidth=2,
                        linestyle='-', alpha=0.9, zorder=5)
        ax_main.text(n + n_pred * 0.1, entry_price,
                     f'Entry\n{smart_price_format(entry_price)}',
                     color=s['entry'], fontsize=7.5, fontweight='bold',
                     va='center', ha='left')
        all_prices.append(entry_price)

        # TP levels (max 3)
        if tp_levels:
            tp_colors = ['#26A69A', '#00BCD4', '#4CAF50']
            for i, tp in enumerate(tp_levels[:3]):
                c = tp_colors[i]
                ax_main.axhline(y=tp, color=c, linewidth=1.5,
                                linestyle='--', alpha=0.8, zorder=5)
                ax_main.text(n + n_pred * 0.1, tp,
                             f'TP{i+1}\n{smart_price_format(tp)}',
                             color=c, fontsize=7.5, fontweight='bold',
                             va='center', ha='left')
                all_prices.append(tp)

        # SL
        if sl_price:
            ax_main.axhline(y=sl_price, color=s['sl'], linewidth=1.8,
                            linestyle='--', alpha=0.85, zorder=5)
            ax_main.text(n + n_pred * 0.1, sl_price,
                         f'SL\n{smart_price_format(sl_price)}',
                         color=s['sl'], fontsize=7.5, fontweight='bold',
                         va='center', ha='left')
            all_prices.append(sl_price)

        # === Y-AXIS FORMAT ===
        ax_main.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda v, _: format_axis_price(v))
        )

        # Ustaw zakres Y z marginesem
        if all_prices:
            y_min = min(min(df['low']), min(all_prices)) * 0.995
            y_max = max(max(df['high']), max(all_prices)) * 1.005
            ax_main.set_ylim(y_min, y_max)

        # Rozszerz X dla etykiet
        ax_main.set_xlim(-1, n + n_pred + 8)

        # === WOLUMEN ===
        for i in range(n):
            o = df['open'].iloc[i]
            c = df['close'].iloc[i]
            color = s['up'] if c >= o else s['down']
            ax_vol.bar(i, df['volume'].iloc[i], color=color, alpha=0.6, width=0.8)

        ax_vol.set_ylabel('Vol', color=s['text'], fontsize=7)
        vol_max = df['volume'].max()
        ax_vol.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda v, _: f'{v/1e6:.1f}M' if v >= 1e6 else f'{v/1e3:.0f}K')
        )

        # === RSI ===
        rsi_valid = df['RSI'].dropna()
        if len(rsi_valid) > 0:
            ax_rsi.plot(x, df['RSI'], color='#9C27B0', linewidth=1.5, zorder=3)
            ax_rsi.fill_between(x, df['RSI'], 50,
                                where=df['RSI'] >= 50, alpha=0.15,
                                color=s['up'], zorder=2)
            ax_rsi.fill_between(x, df['RSI'], 50,
                                where=df['RSI'] < 50, alpha=0.15,
                                color=s['down'], zorder=2)
            ax_rsi.axhline(70, color=s['down'], linewidth=0.8,
                           linestyle='--', alpha=0.6)
            ax_rsi.axhline(30, color=s['up'], linewidth=0.8,
                           linestyle='--', alpha=0.6)
            ax_rsi.axhline(50, color=s['grid'], linewidth=0.6, alpha=0.5)
            ax_rsi.set_ylim(0, 100)
            ax_rsi.set_ylabel('RSI', color=s['text'], fontsize=7)

            rsi_now = df['RSI'].iloc[-1]
            ax_rsi.text(n - 1, rsi_now, f' {rsi_now:.0f}',
                        color='#9C27B0', fontsize=8, fontweight='bold',
                        va='center')

        # === X-AXIS LABELS ===
        step = max(1, n // 8)
        tick_positions = list(range(0, n, step))
        tick_labels = [df.index[i].strftime('%m/%d %H:%M')
                       for i in tick_positions if i < n]
        ax_rsi.set_xticks(tick_positions[:len(tick_labels)])
        ax_rsi.set_xticklabels(tick_labels, rotation=30, ha='right',
                               fontsize=7, color=s['text'])
        ax_main.tick_params(labelbottom=False)
        ax_vol.tick_params(labelbottom=False)

        # === TYTUŁ ===
        direction_emoji = '🟢 LONG' if position_type == 'LONG' else '🔴 SHORT'
        fig.suptitle(
            f'{symbol}  |  {timeframe}  |  {direction_emoji}',
            color=s['text'], fontsize=13, fontweight='bold', y=0.98
        )

        # === LEGENDA ===
        legend_elements = [
            mpatches.Patch(color=s['ema1'], label='EMA 20'),
            mpatches.Patch(color=s['ema2'], label='EMA 50'),
            mpatches.Patch(color=s['entry'], label='Entry'),
        ]
        if tp_levels:
            legend_elements.append(mpatches.Patch(color=s['tp'], label='TP'))
        if sl_price:
            legend_elements.append(mpatches.Patch(color=s['sl'], label='SL'))
        legend_elements.append(
            mpatches.Patch(color=s['entry'], alpha=0.5, label='Predykcja')
        )

        ax_main.legend(handles=legend_elements, loc='upper left',
                       framealpha=0.3, fontsize=7,
                       facecolor=s['panel'], edgecolor=s['grid'],
                       labelcolor=s['text'])

        # === GRID ===
        for ax in [ax_main, ax_vol, ax_rsi]:
            ax.grid(True, color=s['grid'], linewidth=0.5, alpha=0.7)

        # === SAVE ===
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=150,
                    bbox_inches='tight', facecolor=s['bg'])
        plt.close(fig)
        buf.seek(0)
        return buf.getvalue()


chart_gen = ChartGenerator()
