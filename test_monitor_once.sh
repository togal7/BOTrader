#!/bin/bash

echo "═══════════════════════════════════════════════════════════"
echo "🧪 TEST MONITOR - Jedna analiza"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Czekam aż zrobisz analizę w bocie..."
echo "(Monitor automatycznie zakończy się po 1 analizie)"
echo ""
echo "───────────────────────────────────────────────────────────"

ANALYSIS_COUNT=0
ANALYSIS_STARTED=false

pm2 logs BOTrader --lines 0 --raw 2>/dev/null | while read line; do
    
    # Wykryj start
    if echo "$line" | grep -q "Starting FULL analysis" && [ "$ANALYSIS_STARTED" = false ]; then
        ANALYSIS_STARTED=true
        clear
        echo "═══════════════════════════════════════════════════════════"
        echo "🎯 ANALIZA WYKRYTA!"
        echo "═══════════════════════════════════════════════════════════"
        echo ""
        echo "$line" | grep -o "Starting FULL.*"
        echo ""
        echo "📊 Śledzę wydarzenia..."
        echo "───────────────────────────────────────────────────────────"
        echo ""
    fi
    
    # Pokaż ważne wydarzenia
    if [ "$ANALYSIS_STARTED" = true ]; then
        T=$(date +%H:%M:%S)
        
        if echo "$line" | grep -q "Tracked signal"; then
            echo "[$T] 📊 SIGNAL TRACKED: $(echo "$line" | grep -o "Tracked signal.*")"
        fi
        
        if echo "$line" | grep -q "Calling DeepSeek"; then
            echo "[$T] 🤖 Calling DeepSeek API..."
        fi
        
        if echo "$line" | grep -q "DeepSeek response received"; then
            echo "[$T] ✅ DeepSeek response received"
        fi
        
        if echo "$line" | grep -q "Learning enhancement"; then
            echo "[$T] 🧠 Learning enhancement applied"
        fi
        
        if echo "$line" | grep -q "Weighted confidence"; then
            echo "[$T] ⚖️  $(echo "$line" | grep -o "Weighted.*" | head -1)"
        fi
        
        if echo "$line" | grep -qE "ERROR.*ai_trader|ERROR.*tracker"; then
            echo "[$T] 🔴 $(echo "$line" | grep -o "ERROR.*" | head -1)"
        fi
        
        if echo "$line" | grep -q "Analysis complete"; then
            echo "[$T] ✅ $(echo "$line" | grep -o "Analysis complete.*")"
            
            # Zakończ po tej analizie
            sleep 2
            
            echo ""
            echo "═══════════════════════════════════════════════════════════"
            echo "📊 FINALNE PODSUMOWANIE:"
            echo "═══════════════════════════════════════════════════════════"
            echo ""
            
            # Sprawdź wynik
            python3 << 'PYEND'
import os
import json

if os.path.exists('ai_signals_history.json'):
    with open('ai_signals_history.json', 'r') as f:
        data = json.load(f)
    
    if data:
        print(f"✅ SYGNAŁ ZAPISANY DO BAZY!")
        print(f"   Liczba sygnałów: {len(data)}")
        
        last_id = list(data.keys())[-1]
        last = data[last_id]
        
        print(f"\n   📍 OSTATNI SYGNAŁ:")
        print(f"      ID: {last_id}")
        print(f"      Symbol: {last['symbol']}")
        print(f"      Signal: {last['signal']}")
        print(f"      Confidence: {last['confidence']}%")
        print(f"      Price: ${last['entry_price']}")
        
        ind = last.get('indicators', {})
        print(f"\n   📈 WSKAŹNIKI:")
        print(f"      RSI: {ind.get('rsi', 'N/A')}")
        print(f"      Volume: {ind.get('volume_ratio', 1.0):.2f}x")
        print(f"      EMA Cross: {ind.get('ema_cross', False)}")
        
        print(f"\n✅ LEARNING SYSTEM DZIAŁA!")
        print(f"   Za 24h bot sprawdzi wynik tego sygnału")
        
    else:
        print("❌ Baza pusta - sygnał nie został zapisany")
else:
    print("❌ Plik ai_signals_history.json nie istnieje")
    print("   Learning system NIE ZAPISAŁ sygnału")
    print("\n🔧 Potrzebna naprawa - tracker nie działa")

print("\n" + "="*60)

# Sprawdź czy są błędy w logach
import subprocess
result = subprocess.run(
    ["pm2", "logs", "BOTrader", "--lines", "50", "--nostream"],
    capture_output=True,
    text=True
)

errors = [line for line in result.stdout.split('\n') if 'ERROR' in line and 'ai_trader' in line.lower()]

if errors:
    print("🔴 ZNALEZIONE BŁĘDY:")
    for err in errors[-3:]:  # Ostatnie 3
        print(f"   {err}")
else:
    print("✅ Brak błędów w logach")

PYEND
            
            echo ""
            echo "═══════════════════════════════════════════════════════════"
            echo "Test zakończony!"
            echo "═══════════════════════════════════════════════════════════"
            
            # Zabij proces monitora
            pkill -P $$ tail
            exit 0
        fi
    fi
done

