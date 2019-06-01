# Anonymous veto network
Anonymous veto network zaimplementowana w Pythonie 3.6

Grupa ludzi zebrała się, aby odpowiedzieć na trudne pytanie. Zanim będą mogli anonimowo odpowiedzieć na nie, 
przewodniczący powinien skonfigurować serwer, podać adres IP oraz przekazać certyfikat serwera innym członkom.

Przed uruchomieniem należy zmienić adres IP serwera z jakim chcemy się połączyć w pliku common.py 
w zmiennej o nazwie HOST. Aby uruchomić skrypt należy z polecenia linii komend:
path/to/python server.py
a następnie z trzech różnych komputerów (ewentualnie konsol)
path/to/python client.py

Należy pamiętać, aby HOST w każdym z plików common (jeśli uruchamiamy z innych komputerów) powinien mieć tego
samego HOSTa. Dodatkowo certyfikaty i klucze powinny być w tym samym folderze, z którego uruchamiamy skrypt.

Certyfikaty zostały wrzucone na gita i będą aktualne przez 360 dni. Aby wygenerować nowe certyfikaty należy mieć 
zainstalowanego openssl-a oraz wykonać z CMD następujące komendy:
openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout server.key -out server.crt
aby wygenerować certyfikat dla serwera
oraz 
openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout client.key -out client.crt
dla klienta.

Pamiętać też trzeba, że przy generowaniu klucza serwerowego należy w CommonName wpisać veto.com

W przypadku problemów związanych z openssl możliwa będzie potrzeba ustawienia ścieżki środowiskowej 
set OPENSSL_CONF=sciezka/do/openssl/libs/openssl-0.9.8k/openssl.cnf