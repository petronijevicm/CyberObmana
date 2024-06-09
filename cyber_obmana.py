#!/usr/bin/env python3

# Cyber Obmana

### Konfiguracija ###
# Koliko linkova ce biti generisano po strani ( od 4 do 8 )
LINKOVA_PO_STRANI = (4, 10)
# Kolika je duzina linkova
DUZINA_LINKOVA = (1, 3)
# broj porta gde ce se pokrenuti web server
PORT = 8888
# koliko brzo ce server odgovarati na zahtev za stranicu ( 400 milisekudi do 1 sekunde ) da bi se dodatno izbegli filteri, ovaj delay treba da bude isti illi malo kraci ili duzi u poredjenu sa normalnim radom
DELAY = (1000)
# Reci od kojih ce se imena linkova sastojati, ove kljucne reci su nesto sto bi napadac voleo da vidi 
WORD_SPACE = ['login', 'admin_panel', 'register', 'profile', 'config', 'wp_admin', 'temp', 'backup', 'logs', '.hidden', 'dev', 'private', 'error_logs', 'uploads', 'database', 'cache','sessions']
CHAR_SPACE = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-/'
### Kraj konfiguracije ###


# Sys i random su potrebni za pozivanje sistemskih komandi i generisanja IMENA nasumicnih linkova
import sys
import random 
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

class Handler(BaseHTTPRequestHandler):
  webpages = None
  
  def generate_page(self, seed):
    """Generise html kod koji ce se injektovati u web stranicu"""
    
    html = '<html>\n<body>\n'
    
    random.seed(seed)
    # broj linkova koji ce se generisati na strani ( zavisi od promenijve LINKOVA_PO_STRANI i bice ih od 4 do 10
    num_pages = random.randint(*LINKOVA_PO_STRANI)
    
    # Sama generacija linkova, bice odvojeni sa _ i na kraju ce im biti dodat CHAR_SPACE nasumicno u duzini od 5 do 10 karaktera
    for i in range(num_pages):
        address = '_'.join([random.choice(WORD_SPACE) for _ in range(random.randint(*DUZINA_LINKOVA))])
        char_space_length = random.randint(5, 10)
        char_space = ''.join(random.choices(CHAR_SPACE, k=char_space_length))
        address += '_' + char_space  # Dodavanje CHAR_SPACE na kraj linka
        html += '<a href="' + address + '.html">' + address + '</a><br>\n'
      
    html += '</body>\n</html>'
    
    return html

    
  def do_HEAD(self):
    """Salje se 200 ili OK signal u html da je stranica dostupna"""
    
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()

  def do_GET(self):
    """Svaki zahtev za stranicu na WEB serveru ce biti odgovoren sa kodom 200 (OK) cak i ako on ne postoji npr localhost:8888/nasumicantekst/ i za njega ce se generisati stranica"""
    
    # DELAY koji je definisan na pocetku namenjen je da uspori samu pretragu na 1 sekundu po odgovoru
    time.sleep(DELAY/1000.0)
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    # dodavanje rand funkciji trenutnu URL lokaciju (nepostojecu)
    self.wfile.write(self.generate_page(self.path).encode())
  

def print_usage():
  print('Usage: ' + sys.argv[0] + ' [FILE]\n')
  print('FILE is file containing a list of webpage names to serve, one per line.  If no file is provided, random links will be generated.')

    
def main():
  if '-h' in sys.argv or '--help' in sys.argv:
    print_usage()
    exit()
# Prost try-catch blok namenjen da proveri da li je server pokrenut/stopiran i da li je port otvoren
  try:
    print('Starting server on port %d...' % PORT)
    server = HTTPServer(('', PORT), Handler)
    print('Server started.  Use <Ctrl-C> to stop.')
    server.serve_forever()
  except KeyboardInterrupt:
    print('Stopping server...')
    server.socket.close()
    print('Server stopped')
  except:
    print('Error starting http server on port %d.' % PORT)
    print('Make sure you are root, if needed, and that port %d is open.' % PORT)
  
  
if __name__ == '__main__':
  main()
