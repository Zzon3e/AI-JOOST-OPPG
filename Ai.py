import sqlite3
import requests
from datetime import datetime

# Opprett eller koble til databasen hvis den ikke eksisterer
conn = sqlite3.connect('products.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        current_version TEXT,
        last_checked TEXT
    )
''')
conn.commit()

def get_vlc_latest_version():
    """Henter siste versjon av VLC fra nettbasert kilde"""
    try:
        response = requests.get('https://www.videolan.org/releases/vlc/latest.html', timeout=5)
        # Enkel parsing - du kan bruke BeautifulSoup for bedre resultat
        if '3.' in response.text:
            return response.text.split('3.')[1][:3]
    except:
        return None

def check_vlc_update():
    """Sjekker om VLC har oppdateringer"""
    latest = get_vlc_latest_version()
    
    cursor.execute('SELECT current_version FROM products WHERE name = ?', ('VLC',))
    result = cursor.fetchone()
    
    if result:
        current = result[0]
        if latest and current != latest:
            cursor.execute('UPDATE products SET current_version = ?, last_checked = ? WHERE name = ?',
                          (latest, datetime.now(), 'VLC'))
            print(f"✓ Oppdatering tilgjengelig! {current} → {latest}")
            return True
    else:
        cursor.execute('INSERT INTO products VALUES (NULL, ?, ?, ?)',
                      ('VLC', latest, datetime.now()))
        print(f"✓ VLC {latest} registrert")
    
    conn.commit()
    return False

if __name__ == '__main__':
    check_vlc_update()
    conn.close()