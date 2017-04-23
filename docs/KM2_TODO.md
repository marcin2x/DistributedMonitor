# KM2 TODO
1. Najpierw aktualizacja REST API:
    * dodanie uwag od prowadzącego
    * dodanie obiektów dla TCP dla komunikacji Sensor -> Monitor
    * rozbicie na kilka plików

1. Mamy zrealizować wymagania 1-4, czyli:
    * Klient ma możliwość pobrania z Monitora listy wszystkich monitorowanych zasobów i dostarczanych dla nich pomiarów.
    * Klient może przeszukiwać Monitor przy pomocy zapytań:
        * wyszukiwać monitorowane zasoby spełniające określone kryteria, np. "wszystkie hosty, mają w nazwie ciąg ‘zeus’"
    * Pomiary proste (dostarczane bezpośrednio przez sensory) powinny być udostępniane przez Monitor jako lista wartości. Domyślnie zwracana jest lista kilku ostatnich pomiarów.
    * W przeglądarce można:
        * Przeglądać listy dostępnych zasobów i pomiarów.
        * Podglądać ostatnie wartości pomiarów.
        * Wyszukiwać dostępne zasoby i pomiary (np. po nazwie).
        * Wyświetlać wybrane pomiary na wykresie, uaktualnianym automatycznie co pewien czas (np. 5 sekund).

1. Prezentacja rozwiązania.

## API
1. Aktualizacja wg uwag ze spotkania
1. Modele dla komunikacji TCP lub UDP (JSON) (Sensor -> Monitor)
    * rejestracja Sensora w Monitorze z przesłaniem metadanych
    * przesłanie pomiarów z Sensora do Monitora
1. Rozbicie na kilka plików

## Sensor
1. Konfiguracja adresu Monitora oraz interwałów w pliku JSON
1. Obsługa komunikacji z Monitorem w wybranym protokole
1. Rejestracja Sensora w Monitorze
    * Unikalne ID Sensora (propozycja: adres MAC)
    * przesłanie metadanych
    * w określonych interwałach czasowych lub na starcie aplikacji
1. Zbieranie metryk CPU oraz RAM i przesłanie ich do Monitora (razem z ID)
    * w określonych interwałach

## Monitor
1. Konfiguracja bazy danych w pliku JSON
1. Obsługa komunikacji z Sensorem w wybranym protokole
1. Rejestracja metadanych hosta Sensora w bazie
1. Rejestracja pomiarów z Sensora w bazie
1. Udostępnianie listy hostów (Sensorów) przez REST
1. Udostępnianie listy pomiarów przez REST
    * wraz z przeszukiwaniem po nazwie

## WebApp
1. Logowanie
1. Dodanie monitora
1. Wyświetlenie monitorów
1. Przeglądanie listy hostów w Monitorze (Sensorów)
1. Przeglądanie ostatnich pomiarów w Monitorze
1. Przeszukiwanie hostów/pomiarów
1. Wyświetlanie na wykresie
1. Automatyczne odświeżanie wykresów co zadany interwał

## Autentykacja
1. Rejestracja użytkownika
1. Logowanie
1. Dodanie monitora
1. Zwrócenie listy monitorów

