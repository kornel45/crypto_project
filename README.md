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




