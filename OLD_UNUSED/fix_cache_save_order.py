with open('handlers.py', 'r') as f:
    lines = f.readlines()

# Znajdź sekcję z duplikacją (linie ~1133-1150)
found_first_cache = False
first_cache_start = -1
first_cache_end = -1
second_cache_start = -1

for i, line in enumerate(lines):
    # Szukaj pierwszego cached_scan_results
    if "user['cached_scan_results'] = [" in line and not found_first_cache:
        first_cache_start = i
        found_first_cache = True
        print(f"Znaleziono PIERWSZY cache w linii {i+1}")
    
    # Szukaj drugiego cached_scan_results (duplikat)
    elif "user['cached_scan_results'] = [" in line and found_first_cache:
        second_cache_start = i
        print(f"Znaleziono DRUGI cache (duplikat) w linii {i+1}")
        break

if second_cache_start > 0:
    # USUŃ cały drugi blok (od "# Zapisz context" do db.update_user)
    # Znajdź koniec drugiego bloku
    for i in range(second_cache_start - 5, second_cache_start + 20):
        if i < len(lines) and 'db.update_user' in lines[i]:
            # Usuń linie od "# Zapisz context" do db.update_user włącznie
            
            # Znajdź start (komentarz)
            delete_start = second_cache_start - 2  # "# Zapisz context"
            delete_end = i + 1  # po db.update_user
            
            print(f"Usuwam linie {delete_start+1} do {delete_end}")
            del lines[delete_start:delete_end]
            break
    
    # Teraz znajdź PIERWSZY cache i przenieś db.update_user NA KONIEC
    # Znajdź gdzie jest pierwszy logger.info("Cached...")
    for i, line in enumerate(lines):
        if 'logger.info(f"Cached' in line:
            # db.update_user powinno być 2 linie dalej
            if i + 2 < len(lines) and 'db.update_user' in lines[i + 2]:
                # Usuń db.update_user z tej linii
                db_update_line = lines[i + 2]
                del lines[i + 2]
                
                # Wstaw NA KOŃCU bloku cache (po logger.info)
                lines.insert(i + 1, db_update_line)
                print(f"✅ Przeniesiono db.update_user PRZED logger.info")
            break

with open('handlers.py', 'w') as f:
    f.writelines(lines)

print("✅ Naprawiono kolejność zapisu cache!")

