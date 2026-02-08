# Portfolio Add Position - Debug Info

## PROBLEM
Gdy user kliknie "Add Position" i wpisze "BTC":
- ✅ Pokazuje się instrukcja Portfolio
- ❌ ALE RÓWNIEŻ uruchamia search handler
- Efekt: dwie wiadomości (Portfolio + Search)

## CO PRÓBOWALIŚMY (10+ rozwiązań):
1. ✅ Portfolio handler w handlers.py - działa
2. ❌ State check w bot.py - search ignoruje
3. ❌ Portfolio priority MessageHandler (group=-1) - search dalej działa
4. ❌ Custom BaseFilter - BaseFilter nie istnieje w tej wersji
5. ❌ filters.Create() - nie istnieje
6. ❌ Callable filter - błędy składni
7. ❌ Group priority (0 vs 1) - search dalej działa
8. ❌ ConversationHandler - search dalej działa
9. ❌ State check w search handler - nie zadziałało
10. ❌ Separate portfolio_filter.py - import errors

## DLACZEGO NIE DZIAŁA
Search handler prawdopodobnie:
- Jest zarejestrowany PRZED Portfolio
- Lub używa innego mechanizmu (command?)
- Lub nie sprawdza state przed działaniem

## ROZWIĄZANIE NA JUTRO

### Opcja A: Znajdź i usuń search MessageHandler
```python
# W bot.py - znajdź GDZIE jest search handler
grep -n "search\|Search" bot.py
# Usuń go i zastąp commandem /search
Opcja B: Przepisz search na command
# Zamiast MessageHandler(filters.TEXT)
# Użyj CommandHandler('search')
# User: /search BTC
Opcja C: Wyłącz text search całkowicie
# Search tylko przez przyciski (już działa)
# Usuń text search handler z bot.py
JAK TO NAPRAWIĆ (5 minut):
Znajdź search handler w bot.py:
grep -A 10 "MessageHandler.*TEXT" bot.py
Usuń lub zmień na:
# Zamiast: MessageHandler(filters.TEXT, search_function)
# Daj: CommandHandler('search', search_function)
Restart
EXPECTED RESULT
User wpisuje "BTC" w Portfolio → TYLKO Portfolio odpowiada
