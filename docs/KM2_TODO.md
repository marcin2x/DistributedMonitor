# KM2 TODO

## API
1. Aktualizacja wg uwag ze spotkania
1. Modele dla komunikacji TCP lub UDP (JSON) (Sensor -> Monitor)
    * rejestracja Sensora w Monitorze z przesłaniem metadanych
    * przesłanie pomiarów z Sensora do Monitora

## Sensor
1. Rejestracja Sensora w Monitorze
    * Unikalne ID Sensora (propozycja: adres MAC)
    * przesłanie metadanych
    * w określonych interwałach czasowych lub na starcie aplikacji
1. Zbieranie metryk CPU oraz RAM i przesłanie ich do Monitora (razem z ID)
    * w określonych interwałach
1. Obsługa komunikacji z Monitorem w wybranym protokole
1. Konfiguracja adresu Monitora oraz interwałów w pliku JSON

## Monitor
1. Obsługa komunikacji z Sensorem w wybranym protokole
1. Rejestracja metadanych hosta Sensora w bazie
1. Rejestracja pomiarów z Sensora w bazie
1. Konfiguracja bazy danych w pliku JSON
1. Udostępnianie listy hostów (Sensorów) przez REST
1. Udostępnianie listy pomiarów przez REST
    * wraz z przeszukiwaniem po nazwie

## WebApp
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

