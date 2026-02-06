#!/usr/bin/env python3
"""
Manual Signal Scanner - Interaktywny skaner sygnałów
Użycie: python3 manual_scan.py
"""

import asyncio
import sys
from central_ai_analyzer import central_analyzer
from ai_signals_tracker import tracker
import time

# TOP 50 par
SYMBOLS = [
    'BTC/USDT:USDT', 'ETH/USDT:USDT', 'BNB/USDT:USDT', 'SOL/USDT:USDT',
    'XRP/USDT:USDT', 'ADA/USDT:USDT', 'AVAX/USDT:USDT', 'DOGE/USDT:USDT',
    'DOT/USDT:USDT', 'MATIC/USDT:USDT', 'LINK/USDT:USDT', 'UNI/USDT:USDT',
    'ATOM/USDT:USDT', 'LTC/USDT:USDT', 'NEAR/USDT:USDT', 'FTM/USDT:USDT',
    'ALGO/USDT:USDT', 'XLM/USDT:USDT', 'AAVE/USDT:USDT', 'CRV/USDT:USDT',
    'SHIB/USDT:USDT', 'PEPE/USDT:USDT', 'FLOKI/USDT:USDT', 'ARB/USDT:USDT',
    'OP/USDT:USDT', 'SUI/USDT:USDT', 'APT/USDT:USDT', 'SEI/USDT:USDT',
    'INJ/USDT:USDT', 'TIA/USDT:USDT', 'FIL/USDT:USDT', 'AR/USDT:USDT',
    'GRT/USDT:USDT', 'SAND/USDT:USDT', 'MANA/USDT:USDT', 'AXS/USDT:USDT',
    'GALA/USDT:USDT', 'BCH/USDT:USDT', 'XMR/USDT:USDT', 'VET/USDT:USDT',
    'THETA/USDT:USDT', 'HBAR/USDT:USDT', 'ICP/USDT:USDT', 'EOS/USDT:USDT',
    'TRX/USDT:USDT', 'FET/USDT:USDT', 'AGIX/USDT:USDT', 'ZEC/USDT:USDT',
    'DASH/USDT:USDT', 'OKB/USDT:USDT'
]

ALL_TIMEFRAMES = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '8h', '12h', '1d', '3d', '1w']

def print_header():
    print("\n" + "="*60)
    print("🚀 MANUAL SIGNAL SCANNER")
    print("="*60)

def select_timeframes():
    print("\n📊 WYBIERZ INTERWAŁY CZASOWE:")
    print("\nDostępne opcje:")
    print("  1. Szybkie (1m, 3m, 5m) - weryfikacja za 1-5 min")
    print("  2. Krótkie (15m, 30m) - weryfikacja za 15-30 min")
    print("  3. Średnie (1h, 2h, 4h) - weryfikacja za 1-4h")
    print("  4. Długie (1d, 3d, 1w) - weryfikacja za 1-7 dni")
    print("  5. Wszystkie (1m → 1w)")
    print("  6. Custom (wybierz ręcznie)")
    
    choice = input("\nWybór (1-6): ").strip()
    
    if choice == '1':
        return ['1m', '3m', '5m']
    elif choice == '2':
        return ['15m', '30m']
    elif choice == '3':
        return ['1h', '2h', '4h']
    elif choice == '4':
        return ['1d', '3d', '1w']
    elif choice == '5':
        return ALL_TIMEFRAMES
    elif choice == '6':
        print("\nDostępne TF:", ', '.join(ALL_TIMEFRAMES))
        custom = input("Wpisz TF oddzielone spacją (np: 1h 4h 1d): ").strip().split()
        return [tf for tf in custom if tf in ALL_TIMEFRAMES]
    else:
        print("❌ Nieprawidłowy wybór, używam: 1h 4h")
        return ['1h', '4h']

def select_symbols():
    print("\n🎯 WYBIERZ PARY:")
    print("  1. TOP 10 (najszybsze)")
    print("  2. TOP 20")
    print("  3. TOP 30")
    print("  4. Wszystkie 50")
    
    choice = input("\nWybór (1-4): ").strip()
    
    if choice == '1':
        return SYMBOLS[:10]
    elif choice == '2':
        return SYMBOLS[:20]
    elif choice == '3':
        return SYMBOLS[:30]
    else:
        return SYMBOLS

def select_min_confidence():
    print("\n📈 MINIMALNY CONFIDENCE DO ZAPISU:")
    print("  1. 60% (tylko mocne sygnały)")
    print("  2. 40% (średnie i mocne)")
    print("  3. 25% (wszystkie)")
    
    choice = input("\nWybór (1-3): ").strip()
    
    if choice == '1':
        return 60
    elif choice == '2':
        return 40
    else:
        return 25

async def scan_signals(timeframes, symbols, min_conf):
    total = len(timeframes) * len(symbols)
    success = 0
    skipped = 0
    
    print(f"\n🔥 START SKANOWANIA")
    print(f"   Interwały: {', '.join(timeframes)}")
    print(f"   Pary: {len(symbols)}")
    print(f"   Total analiz: {total}")
    print(f"   Min confidence: {min_conf}%")
    print(f"   Szacowany czas: {total * 0.5 / 60:.1f} min\n")
    
    start_time = time.time()
    
    for i, tf in enumerate(timeframes, 1):
        print(f"\n📊 TIMEFRAME {i}/{len(timeframes)}: {tf}")
        print("─" * 60)
        
        for j, symbol in enumerate(symbols, 1):
            try:
                # Progress
                progress = ((i-1) * len(symbols) + j) / total * 100
                print(f"  [{progress:5.1f}%] {symbol:15} {tf:4} ... ", end='', flush=True)
                
                # Analiza
                result = await central_analyzer.analyze_for_ai_signals(
                    symbol=symbol,
                    main_tf=tf,
                    exchange='mexc',
                    language='pl'
                )
                
                if result and result.get('confidence', 0) >= min_conf:
                    # Zapisz
                    tracker.record_signal(
                        symbol=symbol,
                        exchange='mexc',
                        timeframe=tf,
                        signal=result['signal'],
                        confidence=result['confidence'],
                        price=result['entry'],
                        indicators=result.get('analysis', {}).get('technical', {}),
                        ai_response=f"Manual scan: {result['signal']} {result['confidence']}%"
                    )
                    success += 1
                    print(f"✅ {result['signal']:5} {result['confidence']:2}%")
                else:
                    skipped += 1
                    conf = result.get('confidence', 0) if result else 0
                    print(f"⏭️  Skip ({conf}%)")
                
                # Rate limiting
                await asyncio.sleep(0.3)
                
            except Exception as e:
                print(f"❌ Error: {e}")
                skipped += 1
                await asyncio.sleep(1)
        
        # Progress summary
        elapsed = time.time() - start_time
        print(f"\n  ⏱️  Elapsed: {elapsed/60:.1f} min | Success: {success} | Skipped: {skipped}")
    
    # Final summary
    total_time = time.time() - start_time
    print("\n" + "="*60)
    print("🎉 SKANOWANIE ZAKOŃCZONE!")
    print("="*60)
    print(f"✅ Zapisano: {success}/{total} ({success/total*100:.1f}%)")
    print(f"⏭️  Pominięto: {skipped}/{total} ({skipped/total*100:.1f}%)")
    print(f"⏱️  Czas: {total_time/60:.1f} min")
    print(f"📊 Nowa baza: ~{success + 496} sygnałów")
    print("="*60)

async def main():
    print_header()
    
    timeframes = select_timeframes()
    symbols = select_symbols()
    min_conf = select_min_confidence()
    
    print("\n" + "="*60)
    print("PODSUMOWANIE:")
    print("="*60)
    print(f"  Interwały: {', '.join(timeframes)}")
    print(f"  Pary: {len(symbols)}")
    print(f"  Min confidence: {min_conf}%")
    print(f"  Total analiz: {len(timeframes) * len(symbols)}")
    print("="*60)
    
    confirm = input("\nRozpocząć skanowanie? (tak/nie): ").strip().lower()
    
    if confirm in ['tak', 't', 'yes', 'y']:
        await scan_signals(timeframes, symbols, min_conf)
    else:
        print("\n❌ Anulowano")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Przerwano przez użytkownika (Ctrl+C)")
        print("✅ Postęp zapisany w ai_signals_history.json")

