with open('ai_signals_advanced.py', 'r') as f:
    content = f.read()

# Zmień próg z 30 na 20
old_threshold = """            # Minimum score 30 to show
            if score < 30:
                return None"""

new_threshold = """            # Minimum score 20 to show (obniżony próg)
            if score < 20:
                return None"""

content = content.replace(old_threshold, new_threshold)

# Dodaj też logowanie score przed return
old_return = """            return {
                'symbol': symbol,
                'signal': signal,
                'score': score,
                'confidence': confidence,"""

new_return = """            # Log final score
            logger.info(f"score_pair {symbol}: score={score}, signal={signal}, conf={confidence}%")
            
            return {
                'symbol': symbol,
                'signal': signal,
                'score': score,
                'confidence': confidence,"""

content = content.replace(old_return, new_return)

# Dodaj log jeśli score < 20
old_check = """            # Minimum score 20 to show (obniżony próg)
            if score < 20:
                return None"""

new_check = """            # Minimum score 20 to show (obniżony próg)
            if score < 20:
                logger.debug(f"score_pair {symbol}: score too low ({score}), skipping")
                return None"""

content = content.replace(old_check, new_check)

with open('ai_signals_advanced.py', 'w') as f:
    f.write(content)

print("✅ Obniżono próg 30→20 + dodano logi")

