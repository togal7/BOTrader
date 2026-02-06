with open('handlers.py', 'r') as f:
    content = f.read()

print("=== STEP 1: AI Summary w 10 językach ===\n")

# Znajdź i zamień TYLKO generate_ai_summary
old_func = """def generate_ai_summary(signal, technical, sentiment, lang='pl'):
    \"\"\"Generate simple AI summary in user's language\"\"\"

    direction = signal['direction']
    confidence = signal['confidence']
    rsi = technical['rsi']['14']
    price = technical['price']

    # Templates for each language
    templates = {
        'pl': {
            'LONG': f"📊 Analiza wskazuje na potencjalną okazję do KUPNA z pewnością {confidence}%. RSI na poziomie {rsi:.0f} {'sugeruje wyprzedanie - dobry moment na wejście' if rsi < 35 else 'jest w akceptowalnym zakresie'}. Cena wynosi ${price:.6f}. Rekomendujemy rozważenie pozycji długiej z zaproponowanymi poziomami TP/SL.",
            'SHORT': f"📊 Analiza wskazuje na potencjalną okazję do SPRZEDAŻY z pewnością {confidence}%. RSI na poziomie {rsi:.0f} {'sugeruje wykupienie - możliwa korekta' if rsi > 65 else 'jest w akceptowalnym zakresie'}. Cena wynosi ${price:.6f}. Rekomendujemy rozważenie pozycji krótkiej z zaproponowanymi poziomami TP/SL.",
            'NEUTRAL': f"📊 Analiza nie wskazuje wyraźnego kierunku (pewność {confidence}%). RSI na poziomie {rsi:.0f}. Cena wynosi ${price:.6f}. Rekomendujemy poczekać na lepszy setup lub potwierdzenie sygnału."
        },
        'en': {
            'LONG': f"📊 Analysis indicates potential BUY opportunity with {confidence}% confidence. RSI at {rsi:.0f} {'suggests oversold conditions - good entry point' if rsi < 35 else 'is within acceptable range'}. Price is ${price:.6f}. Consider long position with suggested TP/SL levels.",
            'SHORT': f"📊 Analysis indicates potential SELL opportunity with {confidence}% confidence. RSI at {rsi:.0f} {'suggests overbought conditions - correction possible' if rsi > 65 else 'is within acceptable range'}. Price is ${price:.6f}. Consider short position with suggested TP/SL levels.",
            'NEUTRAL': f"📊 Analysis shows no clear direction (confidence {confidence}%). RSI at {rsi:.0f}. Price is ${price:.6f}. Recommend waiting for better setup or signal confirmation."
        }
    }

    # Get template for language (fallback to English)
    lang_templates = templates.get(lang, templates['en'])
    summary = lang_templates.get(direction, lang_templates['NEUTRAL'])

    return summary"""

# Nowa wersja z WSZYSTKIMI 10 językami
new_func = """def generate_ai_summary(signal, technical, sentiment, lang='pl'):
    \"\"\"Generate AI summary in ALL 10 languages\"\"\"
    
    direction = signal['direction']
    confidence = signal['confidence']
    rsi = technical['rsi']['14']
    price = technical['price']
    
    templates = {
        'pl': {
            'LONG': f"📊 Analiza wskazuje na potencjalną okazję do KUPNA z pewnością {confidence}%. RSI na poziomie {rsi:.0f} {'sugeruje wyprzedanie - dobry moment na wejście' if rsi < 35 else 'jest w akceptowalnym zakresie'}. Cena wynosi ${price:.6f}. Rekomendujemy rozważenie pozycji długiej z zaproponowanymi poziomami TP/SL.",
            'SHORT': f"📊 Analiza wskazuje na potencjalną okazję do SPRZEDAŻY z pewnością {confidence}%. RSI na poziomie {rsi:.0f} {'sugeruje wykupienie - możliwa korekta' if rsi > 65 else 'jest w akceptowalnym zakresie'}. Cena wynosi ${price:.6f}. Rekomendujemy rozważenie pozycji krótkiej z zaproponowanymi poziomami TP/SL.",
            'NEUTRAL': f"📊 Analiza nie wskazuje wyraźnego kierunku (pewność {confidence}%). RSI na poziomie {rsi:.0f}. Cena wynosi ${price:.6f}. Rekomendujemy poczekać na lepszy setup lub potwierdzenie sygnału."
        },
        'en': {
            'LONG': f"📊 Analysis indicates potential BUY with {confidence}% confidence. RSI {rsi:.0f} {'suggests oversold - good entry' if rsi < 35 else 'acceptable range'}. Price ${price:.6f}. Consider long with suggested TP/SL.",
            'SHORT': f"📊 Analysis indicates potential SELL with {confidence}% confidence. RSI {rsi:.0f} {'suggests overbought - correction possible' if rsi > 65 else 'acceptable range'}. Price ${price:.6f}. Consider short with suggested TP/SL.",
            'NEUTRAL': f"📊 No clear direction ({confidence}% confidence). RSI {rsi:.0f}. Price ${price:.6f}. Wait for better setup."
        },
        'es': {
            'LONG': f"📊 Análisis indica oportunidad de COMPRA ({confidence}%). RSI {rsi:.0f} {'sobreventa - buen punto' if rsi < 35 else 'rango aceptable'}. Precio ${price:.6f}. Considere largo con TP/SL.",
            'SHORT': f"📊 Análisis indica oportunidad de VENTA ({confidence}%). RSI {rsi:.0f} {'sobrecompra - corrección posible' if rsi > 65 else 'rango aceptable'}. Precio ${price:.6f}. Considere corto con TP/SL.",
            'NEUTRAL': f"📊 Sin dirección clara ({confidence}%). RSI {rsi:.0f}. Precio ${price:.6f}. Espere mejor configuración."
        },
        'de': {
            'LONG': f"📊 Analyse zeigt KAUF-Chance ({confidence}%). RSI {rsi:.0f} {'Überverkauf - guter Punkt' if rsi < 35 else 'akzeptabel'}. Preis ${price:.6f}. Long mit TP/SL erwägen.",
            'SHORT': f"📊 Analyse zeigt VERKAUF-Chance ({confidence}%). RSI {rsi:.0f} {'Überkauf - Korrektur möglich' if rsi > 65 else 'akzeptabel'}. Preis ${price:.6f}. Short mit TP/SL erwägen.",
            'NEUTRAL': f"📊 Keine klare Richtung ({confidence}%). RSI {rsi:.0f}. Preis ${price:.6f}. Besseres Setup abwarten."
        },
        'fr': {
            'LONG': f"📊 Analyse montre opportunité ACHAT ({confidence}%). RSI {rsi:.0f} {'survente - bon point' if rsi < 35 else 'acceptable'}. Prix ${price:.6f}. Considérer long avec TP/SL.",
            'SHORT': f"📊 Analyse montre opportunité VENTE ({confidence}%). RSI {rsi:.0f} {'surachat - correction possible' if rsi > 65 else 'acceptable'}. Prix ${price:.6f}. Considérer short avec TP/SL.",
            'NEUTRAL': f"📊 Pas de direction claire ({confidence}%). RSI {rsi:.0f}. Prix ${price:.6f}. Attendre meilleure config."
        },
        'it': {
            'LONG': f"📊 Analisi indica opportunità ACQUISTO ({confidence}%). RSI {rsi:.0f} {'ipervenduto - buon punto' if rsi < 35 else 'accettabile'}. Prezzo ${price:.6f}. Considera long con TP/SL.",
            'SHORT': f"📊 Analisi indica opportunità VENDITA ({confidence}%). RSI {rsi:.0f} {'ipercomprato - correzione possibile' if rsi > 65 else 'accettabile'}. Prezzo ${price:.6f}. Considera short con TP/SL.",
            'NEUTRAL': f"📊 Nessuna direzione chiara ({confidence}%). RSI {rsi:.0f}. Prezzo ${price:.6f}. Aspetta migliore config."
        },
        'pt': {
            'LONG': f"📊 Análise indica oportunidade COMPRA ({confidence}%). RSI {rsi:.0f} {'sobrevenda - bom ponto' if rsi < 35 else 'aceitável'}. Preço ${price:.6f}. Considere longo com TP/SL.",
            'SHORT': f"📊 Análise indica oportunidade VENDA ({confidence}%). RSI {rsi:.0f} {'sobrecompra - correção possível' if rsi > 65 else 'aceitável'}. Preço ${price:.6f}. Considere curto com TP/SL.",
            'NEUTRAL': f"📊 Sem direção clara ({confidence}%). RSI {rsi:.0f}. Preço ${price:.6f}. Aguarde melhor config."
        },
        'ru': {
            'LONG': f"📊 Анализ показывает возможность ПОКУПКИ ({confidence}%). RSI {rsi:.0f} {'перепродано - хорошая точка' if rsi < 35 else 'приемлемо'}. Цена ${price:.6f}. Рассмотрите лонг с TP/SL.",
            'SHORT': f"📊 Анализ показывает возможность ПРОДАЖИ ({confidence}%). RSI {rsi:.0f} {'перекуплено - коррекция возможна' if rsi > 65 else 'приемлемо'}. Цена ${price:.6f}. Рассмотрите шорт с TP/SL.",
            'NEUTRAL': f"📊 Нет четкого направления ({confidence}%). RSI {rsi:.0f}. Цена ${price:.6f}. Ждите лучшей установки."
        },
        'tr': {
            'LONG': f"📊 Analiz ALMA fırsatı gösteriyor (%{confidence}). RSI {rsi:.0f} {'aşırı satım - iyi nokta' if rsi < 35 else 'kabul edilebilir'}. Fiyat ${price:.6f}. TP/SL ile uzun düşünün.",
            'SHORT': f"📊 Analiz SATMA fırsatı gösteriyor (%{confidence}). RSI {rsi:.0f} {'aşırı alım - düzeltme olası' if rsi > 65 else 'kabul edilebilir'}. Fiyat ${price:.6f}. TP/SL ile kısa düşünün.",
            'NEUTRAL': f"📊 Net yön yok (%{confidence}). RSI {rsi:.0f}. Fiyat ${price:.6f}. Daha iyi kurulum bekleyin."
        },
        'zh': {
            'LONG': f"📊 分析显示买入机会({confidence}%)。RSI {rsi:.0f} {'超卖 - 良好点位' if rsi < 35 else '可接受'}。价格${price:.6f}。考虑建议TP/SL的多头。",
            'SHORT': f"📊 分析显示卖出机会({confidence}%)。RSI {rsi:.0f} {'超买 - 可能回调' if rsi > 65 else '可接受'}。价格${price:.6f}。考虑建议TP/SL的空头。",
            'NEUTRAL': f"📊 无明确方向({confidence}%)。RSI {rsi:.0f}。价格${price:.6f}。等待更好设置。"
        }
    }
    
    lang_templates = templates.get(lang, templates['pl'])
    return lang_templates.get(direction, lang_templates['NEUTRAL'])"""

if old_func in content:
    content = content.replace(old_func, new_func)
    print("✅ Updated generate_ai_summary with 10 languages")
else:
    print("⚠️ Old function not found")

with open('handlers.py', 'w') as f:
    f.write(content)

