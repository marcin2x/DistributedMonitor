# Testowanie (Web-App - Monitor):

_______________________________________________________
## LOGOWANIE i REJESTRACJA:

1) V logowanie bez podania poprawnego maila (czyt. "@") -> poprawny komunikat informujący o tym
2) V logowanie bez podania poprawnego maila (czyt. brak znakow po "@") -> poprawny komunikat informujący o tym
=> X komunikaty są po polsku w przeciwieństwie do innych komunikatów i tekstów na stronie które są po angielsku

3) V logowanie bez posiadania konta -> poprawna informacja

4) V logowanie przy posiadaniu konta (błędne hasło) -> poprawny komunikat

5) V logowanie z poprawnymi danymi przekierowuje na stronę

6) ~ każde odświeżenie strony juz po zalogowaniu powraca do strony logowania

_______________________________________________________
## DODAWANIE/USUWANIE MONITORÓW:

1) X po dodaniu monitora, okno nie znika 

2) X trzeba odświezyć strone zeby zobaczyc nowo dodany monitor

3) X po próbie skasowania monitora, monitor nadal pozostaje

4) X podczas dodawania monitora "Simulate Error", nie symuluje błędu tylko dodaje monitor

5) ~ dodając monitor nie wysyła do niego requesta, nie sprawdza czy pod danym Ip monitor istnieje

_______________________________________________________
## WYŚWIETLANIE POMIARÓW Z MONITORA:

1) X po wybraniu jednego z monitorów w dashboardzie, wykres nieporawnie wyswietla dane (trzeba odczekać kilka sekund). Mimo iz jest zaznaczony "DESKTOP-LCHE7CL", wykres po kilku 	zmianach w wyglądzie, ostatecznie wyswietla wykres dla ostatniego z sensorów które sa na liście powyzej wykresu

2) X w tabeli "Last measurements" są zawsze dane nieaktualne, prawdopodobnie początkowe, a nie ostatnie.
Dane w tabeli nie zmieniają się po wybraniu zakładki innego sensora

3) V po wybraniu zakładki z sensorem, na wykresie wyświetlają się poprawnie dane, jeżeli sensor jest uruchomiony to wykres się aktualizuje, jeżeli nie to przychodzą ostatnie dane

_______________________________________________________
## WYŚWIETLANIE HOSTÓW Z MONITORA:

1) V Poprawne wyświetlanie hostów

_______________________________________________________
## WYŚWIETLANIE POMIARÓW WRAZ Z WYSZUKIWANIEM:

1) X Brak wyszukiwania w tabeli

_______________________________________________________
## WYŚWIETLANIE DANYCH NA WYKRESACH:

1) X niektóre dane po najechaniu myszką na kropkę na wykresie wyswietlanie są do drugiego bądź pierwszego miejsca po przecinku, a niektóre nie (np. 11.790000000000001) -> nalezy ujednolicić wyświetlanie danych

_______________________________________________________
## AUTOMATYCZNE ODŚWIEŻANIE WYKRESÓW:

1) V poprawnie odswieza wykresy co 5 sekund