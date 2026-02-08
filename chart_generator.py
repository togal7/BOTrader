"""
Professional Trading Chart Generator
Generates TradingView-style charts with entry/TP/SL markers
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
from typing import Optional, List, Tuple
import logging

logger = logging.getLogger(__name__)

class ChartGenerator:
    """Generate professional trading charts"""
    
    def __init__(self):
        self.style = self._create_custom_style()
    
    def _create_custom_style(self):
        """Create custom TradingView-like style"""
        return mpf.make_mpf_style(
            base_mpf_style='charles',
            rc={
                'font.size': 10,
                'axes.labelsize': 10,
                'axes.titlesize': 12,
                'xtick.labelsize': 9,
                'ytick.labelsize': 9,
                'figure.facecolor': '#0E1117',
                'axes.facecolor': '#131722',
                'axes.edgecolor': '#2A2E39',
                'axes.labelcolor': '#B2B5BE',
                'xtick.color': '#787B86',
                'ytick.color': '#787B86',
                'grid.color': '#2A2E39',
                'grid.linestyle': '--',
                'grid.linewidth': 0.5,
            },
            marketcolors=mpf.make_marketcolors(
                up='#26A69A',
                down='#EF5350',
                edge='inherit',
                wick='inherit',
                volume='in',
                alpha=0.9,
            )
        )
    
    async def generate_signal_chart(
        self,
        symbol: str,
        timeframe: str,
        ohlcv_data: pd.DataFrame,
        entry_price: float,
        position_type: str,  # LONG or SHORT
        tp_levels: Optional[List[float]] = None,
        sl_price: Optional[float] = None,
        liquidation_price: Optional[float] = None,
        support_resistance: Optional[List[Tuple[float, str]]] = None,
    ) -> bytes:
        """
        Generate professional chart with trading markers
        
        Args:
            symbol: Trading pair (e.g., BTC/USDT)
            timeframe: Chart timeframe (5m, 15m, 1h, etc.)
            ohlcv_data: OHLCV pandas DataFrame
            entry_price: Entry price for the trade
            position_type: LONG or SHORT
            tp_levels: List of take-profit levels
            sl_price: Stop-loss price
            liquidation_price: Liquidation price (for leverage)
            support_resistance: List of (price, 'support'/'resistance')
        
        Returns:
            bytes: PNG image data
        """
        try:
            # Prepare data
            df = ohlcv_data.copy()
            df.index = pd.to_datetime(df.index)
            
            # Calculate indicators
            df['EMA_20'] = df['close'].ewm(span=20).mean()
            df['EMA_50'] = df['close'].ewm(span=50).mean()
            
            # Calculate RSI
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            
            # Create additional plots
            apds = []
            
            # Add EMAs
            apds.append(mpf.make_addplot(df['EMA_20'], color='#2962FF', width=1.5, label='EMA 20'))
            apds.append(mpf.make_addplot(df['EMA_50'], color='#FF6D00', width=1.5, label='EMA 50'))
            
            # Prepare markers for entry/TP/SL
            markers = []
            
            # Entry marker
            entry_color = '#26A69A' if position_type == 'LONG' else '#EF5350'
            entry_marker = '^' if position_type == 'LONG' else 'v'
            
            # Create figure
            fig, axes = mpf.plot(
                df,
                type='candle',
                style=self.style,
                volume=True,
                title=f'{symbol} - {timeframe} - {position_type}',
                ylabel='Price (USDT)',
                ylabel_lower='Volume',
                figsize=(14, 10),
                panel_ratios=(3, 1),
                addplot=apds,
                returnfig=True,
                warn_too_much_data=10000,
            )
            
            ax_main = axes[0]
            
            # Get y-axis limits for drawing lines
            ylim = ax_main.get_ylim()
            xlim = ax_main.get_xlim()
            
            # Draw horizontal lines for TP/SL/Liquidation
            if tp_levels:
                for i, tp in enumerate(tp_levels, 1):
                    ax_main.axhline(
                        y=tp,
                        color='#26A69A',
                        linestyle='--',
                        linewidth=1.5,
                        alpha=0.7,
                        label=f'TP{i}: ${tp:,.2f}'
                    )
            
            if sl_price:
                ax_main.axhline(
                    y=sl_price,
                    color='#EF5350',
                    linestyle='--',
                    linewidth=2,
                    alpha=0.8,
                    label=f'SL: ${sl_price:,.2f}'
                )
            
            if liquidation_price:
                ax_main.axhline(
                    y=liquidation_price,
                    color='#FF9800',
                    linestyle=':',
                    linewidth=2,
                    alpha=0.7,
                    label=f'Liq: ${liquidation_price:,.2f}'
                )
            
            # Entry price line
            ax_main.axhline(
                y=entry_price,
                color=entry_color,
                linestyle='-',
                linewidth=2.5,
                alpha=0.9,
                label=f'Entry: ${entry_price:,.2f}'
            )
            
            # Draw entry arrow at the last candle
            last_idx = len(df) - 1
            ax_main.annotate(
                'ENTRY',
                xy=(last_idx, entry_price),
                xytext=(last_idx - 10, entry_price * (1.02 if position_type == 'LONG' else 0.98)),
                arrowprops=dict(
                    arrowstyle='->',
                    color=entry_color,
                    lw=2.5,
                ),
                fontsize=12,
                fontweight='bold',
                color=entry_color,
            )
            
            # Support/Resistance zones
            if support_resistance:
                for level, sr_type in support_resistance:
                    color = '#4CAF50' if sr_type == 'support' else '#F44336'
                    ax_main.axhline(
                        y=level,
                        color=color,
                        linestyle='-',
                        linewidth=1,
                        alpha=0.3,
                    )
                    # Add filled zone
                    zone_height = level * 0.003  # 0.3% zone
                    ax_main.fill_between(
                        xlim,
                        level - zone_height,
                        level + zone_height,
                        color=color,
                        alpha=0.1,
                    )
            
            # Add legend
            ax_main.legend(loc='upper left', fontsize=9, framealpha=0.9)
            
            # Add RSI subplot
            ax_rsi = axes[2]
            ax_rsi.plot(df.index, df['RSI'], color='#9C27B0', linewidth=1.5)
            ax_rsi.axhline(y=70, color='#EF5350', linestyle='--', linewidth=1, alpha=0.5)
            ax_rsi.axhline(y=30, color='#26A69A', linestyle='--', linewidth=1, alpha=0.5)
            ax_rsi.fill_between(df.index, 70, 100, color='#EF5350', alpha=0.1)
            ax_rsi.fill_between(df.index, 0, 30, color='#26A69A', alpha=0.1)
            ax_rsi.set_ylabel('RSI', fontsize=10)
            ax_rsi.set_ylim(0, 100)
            ax_rsi.grid(True, alpha=0.3)
            
            # Tight layout
            fig.tight_layout()
            
            # Save to bytes
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='#0E1117')
            buf.seek(0)
            
            plt.close(fig)
            
            logger.info(f"✅ Chart generated for {symbol} {timeframe}")
            return buf.read()
            
        except Exception as e:
            logger.error(f"❌ Error generating chart: {e}")
            raise
    
    async def generate_simple_chart(
        self,
        symbol: str,
        timeframe: str,
        ohlcv_data: pd.DataFrame,
    ) -> bytes:
        """Generate simple chart without markers (for analysis)"""
        try:
            df = ohlcv_data.copy()
            df.index = pd.to_datetime(df.index)
            
            # Calculate EMAs
            df['EMA_20'] = df['close'].ewm(span=20).mean()
            df['EMA_50'] = df['close'].ewm(span=50).mean()
            
            apds = [
                mpf.make_addplot(df['EMA_20'], color='#2962FF', width=1.5),
                mpf.make_addplot(df['EMA_50'], color='#FF6D00', width=1.5),
            ]
            
            fig, axes = mpf.plot(
                df,
                type='candle',
                style=self.style,
                volume=True,
                title=f'{symbol} - {timeframe}',
                ylabel='Price (USDT)',
                ylabel_lower='Volume',
                figsize=(14, 8),
                addplot=apds,
                returnfig=True,
            )
            
            fig.tight_layout()
            
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='#0E1117')
            buf.seek(0)
            
            plt.close(fig)
            
            return buf.read()
            
        except Exception as e:
            logger.error(f"❌ Error generating simple chart: {e}")
            raise

# Global instance
chart_gen = ChartGenerator()

