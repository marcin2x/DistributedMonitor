# Complex

## Operation

- poprawne tworzenie pomiarów złożonych, jednak lista zasobów dla sensora nie zostaje odświezona po dodaniu (X)
- usuwanie pomiaru działa, jednak lista zasobów którą można rozwinąć dla danego sensora nie jest odświeżana, i usunięty pomiar dalej się na niej znajduje (X)
- pomiar złożony jest poprawnie wyświetlany dla wszystkich użytkowników dla wybranego monitora
- poprawnie przeszły testy z poziomu WebApp i Monitora (REST API)

***

## Calculation

- poprawne wyliczanie pomiarów złożonych 
- poprawnie wylicza pomiary dla każdego użytkownika
- poprawnie zwraca pomiary w widoku zasobow/hostow (+ GET /hosts)
- poprawnie zwraca pomiary złożone w "GET /measurements/values"
