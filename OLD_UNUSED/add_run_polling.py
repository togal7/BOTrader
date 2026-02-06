with open('bot.py', 'r') as f:
    lines = f.readlines()

# Znajdź koniec funkcji main (przed if __name__)
for i in range(len(lines)-1, -1, -1):
    if 'if __name__ ==' in lines[i]:
        # Cofnij się do ostatniej linii main()
        insert_pos = i - 1
        
        # Usuń puste linie
        while insert_pos > 0 and lines[insert_pos].strip() == '':
            insert_pos -= 1
        
        # Wstaw run_polling PRZED if __name__
        lines.insert(insert_pos + 1, '\n')
        lines.insert(insert_pos + 2, '    # Start bot\n')
        lines.insert(insert_pos + 3, '    logger.info("🚀 Starting polling...")\n')
        lines.insert(insert_pos + 4, '    application.run_polling(allowed_updates=Update.ALL_TYPES)\n')
        lines.insert(insert_pos + 5, '\n')
        
        print(f"✅ Added run_polling at line {insert_pos + 2}")
        break

with open('bot.py', 'w') as f:
    f.writelines(lines)

