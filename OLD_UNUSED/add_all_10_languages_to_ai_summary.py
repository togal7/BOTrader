with open('handlers.py', 'r') as f:
    content = f.read()

print("=== ADDING ALL 10 LANGUAGES TO generate_ai_summary ===\n")

# Znajdź i zamień generate_ai_summary
old_function = """def generate_ai_summary(signal, technical, sentiment, lang='pl'):
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

new_function = """def generate_ai_summary(signal, technical, sentiment, lang='pl'):
    \"\"\"Generate AI summary in ALL 10 languages\"\"\"

    direction = signal['direction']
    confidence = signal['confidence']
    rsi = technical['rsi']['14']
    price = technical['price']

    # RSI conditions for all languages
    rsi_low = 'oversold' if rsi < 35 else 'acceptable'
    rsi_high = 'overbought' if rsi > 65 else 'acceptable'

    # Templates for ALL 10 languages
    templates = {
        'pl': {
            'LONG': f"📊 Analiza wskazuje na potencjalną okazję do KUPNA z pewnością {confidence}%. RSI na poziomie {rsi:.0f} {'sugeruje wyprzedanie - dobry moment na wejście' if rsi < 35 else 'jest w akceptowalnym zakresie'}. Cena wynosi ${price:.6f}. Rekomendujemy rozważenie pozycji długiej z zaproponowanymi poziomami TP/SL.",
            'SHORT': f"📊 Analiza wskazuje na potencjalną okazję do SPRZEDAŻY z pewnością {confidence}%. RSI na poziomie {rsi:.0f} {'sugeruje wykupienie - możliwa korekta' if rsi > 65 else 'jest w akceptowalnym zakresie'}. Cena wynosi ${price:.6f}. Rekomendujemy rozważenie pozycji krótkiej z zaproponowanymi poziomami TP/SL.",
            'NEUTRAL': f"📊 Analiza nie wskazuje wyraźnego kierunku (pewność {confidence}%). RSI na poziomie {rsi:.0f}. Cena wynosi ${price:.6f}. Rekomendujemy poczekać na lepszy setup lub potwierdzenie sygnału."
        },
        'en': {
            'LONG': f"📊 Analysis indicates potential BUY opportunity with {confidence}% confidence. RSI at {rsi:.0f} {'suggests oversold - good entry' if rsi < 35 else 'is acceptable'}. Price is ${price:.6f}. Consider long position with suggested TP/SL.",
            'SHORT': f"📊 Analysis indicates potential SELL opportunity with {confidence}% confidence. RSI at {rsi:.0f} {'suggests overbought - correction possible' if rsi > 65 else 'is acceptable'}. Price is ${price:.6f}. Consider short position with suggested TP/SL.",
            'NEUTRAL': f"📊 Analysis shows no clear direction ({confidence}% confidence). RSI at {rsi:.0f}. Price is ${price:.6f}. Recommend waiting for better setup."
        },
        'es': {
            'LONG': f"📊 El análisis indica oportunidad de COMPRA con {confidence}% de confianza. RSI en {rsi:.0f} {'sugiere sobreventa - buen punto de entrada' if rsi < 35 else 'está en rango aceptable'}. Precio ${price:.6f}. Considere posición larga con niveles TP/SL sugeridos.",
            'SHORT': f"📊 El análisis indica oportunidad de VENTA con {confidence}% de confianza. RSI en {rsi:.0f} {'sugiere sobrecompra - posible corrección' if rsi > 65 else 'está en rango aceptable'}. Precio ${price:.6f}. Considere posición corta con niveles TP/SL sugeridos.",
            'NEUTRAL': f"📊 El análisis no muestra dirección clara ({confidence}% confianza). RSI en {rsi:.0f}. Precio ${price:.6f}. Recomendamos esperar mejor configuración."
        },
        'de': {
            'LONG': f"📊 Analyse zeigt potenzielle KAUF-Gelegenheit mit {confidence}% Konfidenz. RSI bei {rsi:.0f} {'deutet auf Überverkauf - guter Einstieg' if rsi < 35 else 'ist akzeptabel'}. Preis ${price:.6f}. Erwägen Sie Long-Position mit vorgeschlagenen TP/SL.",
            'SHORT': f"📊 Analyse zeigt potenzielle VERKAUF-Gelegenheit mit {confidence}% Konfidenz. RSI bei {rsi:.0f} {'deutet auf Überkauf - Korrektur möglich' if rsi > 65 else 'ist akzeptabel'}. Preis ${price:.6f}. Erwägen Sie Short-Position mit vorgeschlagenen TP/SL.",
            'NEUTRAL': f"📊 Analyse zeigt keine klare Richtung ({confidence}% Konfidenz). RSI bei {rsi:.0f}. Preis ${price:.6f}. Empfehlung: auf besseres Setup warten."
        },
        'fr': {
            'LONG': f"📊 L'analyse indique opportunité d'ACHAT avec {confidence}% de confiance. RSI à {rsi:.0f} {'suggère survente - bon point d'entrée' if rsi < 35 else 'est acceptable'}. Prix ${price:.6f}. Considérez position longue avec niveaux TP/SL suggérés.",
            'SHORT': f"📊 L'analyse indique opportunité de VENTE avec {confidence}% de confiance. RSI à {rsi:.0f} {'suggère surachat - correction possible' if rsi > 65 else 'est acceptable'}. Prix ${price:.6f}. Considérez position courte avec niveaux TP/SL suggérés.",
            'NEUTRAL': f"📊 L'analyse ne montre pas de direction claire ({confidence}% confiance). RSI à {rsi:.0f}. Prix ${price:.6f}. Recommandons d'attendre meilleure configuration."
        },
        'it': {
            'LONG': f"📊 L'analisi indica opportunità di ACQUISTO con {confidence}% di confidenza. RSI a {rsi:.0f} {'suggerisce ipervenduto - buon ingresso' if rsi < 35 else 'è accettabile'}. Prezzo ${price:.6f}. Considera posizione lunga con livelli TP/SL suggeriti.",
            'SHORT': f"📊 L'analisi indica opportunità di VENDITA con {confidence}% di confidenza. RSI a {rsi:.0f} {'suggerisce ipercomprato - correzione possibile' if rsi > 65 else 'è accettabile'}. Prezzo ${price:.6f}. Considera posizione corta con livelli TP/SL suggeriti.",
            'NEUTRAL': f"📊 L'analisi non mostra direzione chiara ({confidence}% confidenza). RSI a {rsi:.0f}. Prezzo ${price:.6f}. Raccomandiamo attendere migliore configurazione."
        },
        'pt': {
            'LONG': f"📊 Análise indica oportunidade de COMPRA com {confidence}% de confiança. RSI em {rsi:.0f} {'sugere sobrevenda - boa entrada' if rsi < 35 else 'está aceitável'}. Preço ${price:.6f}. Considere posição longa com níveis TP/SL sugeridos.",
            'SHORT': f"📊 Análise indica oportunidade de VENDA com {confidence}% de confiança. RSI em {rsi:.0f} {'sugere sobrecompra - correção possível' if rsi > 65 else 'está aceitável'}. Preço ${price:.6f}. Considere posição curta com níveis TP/SL sugeridos.",
            'NEUTRAL': f"📊 Análise não mostra direção clara ({confidence}% confiança). RSI em {rsi:.0f}. Preço ${price:.6f}. Recomendamos aguardar melhor configuração."
        },
        'ru': {
            'LONG': f"📊 Анализ указывает на возможность ПОКУПКИ с уверенностью {confidence}%. RSI на {rsi:.0f} {'указывает на перепроданность - хорошая точка входа' if rsi < 35 else 'в допустимом диапазоне'}. Цена ${price:.6f}. Рассмотрите длинную позицию с предложенными TP/SL.",
            'SHORT': f"📊 Анализ указывает на возможность ПРОДАЖИ с уверенностью {confidence}%. RSI на {rsi:.0f} {'указывает на перекупленность - возможна коррекция' if rsi > 65 else 'в допустимом диапазоне'}. Цена ${price:.6f}. Рассмотрите короткую позицию с предложенными TP/SL.",
            'NEUTRAL': f"📊 Анализ не показывает четкого направления (уверенность {confidence}%). RSI на {rsi:.0f}. Цена ${price:.6f}. Рекомендуем дождаться лучшей установки."
        },
        'tr': {
            'LONG': f"📊 Analiz %{confidence} güvenle ALMA fırsatı gösteriyor. RSI {rsi:.0f} {'aşırı satım - iyi giriş noktası' if rsi < 35 else 'kabul edilebilir'}. Fiyat ${price:.6f}. Önerilen TP/SL seviyeleriyle uzun pozisyon düşünün.",
            'SHORT': f"📊 Analiz %{confidence} güvenle SATMA fırsatı gösteriyor. RSI {rsi:.0f} {'aşırı alım - düzeltme olası' if rsi > 65 else 'kabul edilebilir'}. Fiyat ${price:.6f}. Önerilen TP/SL seviyeleriyle kısa pozisyon düşünün.",
            'NEUTRAL': f"📊 Analiz net yön göstermiyor (%{confidence} güven). RSI {rsi:.0f}. Fiyat ${price:.6f}. Daha iyi kurulum bekleyin."
        },
        'zh': {
            'LONG': f"📊 分析显示潜在买入机会，置信度{confidence}%。RSI在{rsi:.0f} {'表明超卖 - 良好入场点' if rsi < 35 else '处于可接受范围'}。价格${price:.6f}。考虑建议TP/SL水平的多头头寸。",
            'SHORT': f"📊 分析显示潜在卖出机会，置信度{confidence}%。RSI在{rsi:.0f} {'表明超买 - 可能回调' if rsi > 65 else '处于可接受范围'}。价格${price:.6f}。考虑建议TP/SL水平的空头头寸。",
            'NEUTRAL': f"📊 分析未显示明确方向（置信度{confidence}%）。RSI在{rsi:.0f}。价格${price:.6f}。建议等待更好的设置。"
        }
    }

    # Get template for language (fallback to Polish)
    lang_templates = templates.get(lang, templates['pl'])
    summary = lang_templates.get(direction, lang_templates['NEUTRAL'])

    return summary"""

content = content.replace(old_function, new_function)
print("✅ Added ALL 10 languages to generate_ai_summary")

with open('handlers.py', 'w') as f:
    f.write(content)

