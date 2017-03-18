# Autoryzacja

### Logowanie
POST /login

Parametry:
| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| login | wymagany | login uzytkownika | |
| password | wymagany | hasło uzytkownika | |
```javascript
{
    login : [string],
    password : [string]
}
```
Odpowiedz:
```javascript
{
    api-key : [string]
}
```

Statusy odpowiedzi:
* 200 logowanie powiodło się
* 401 nieprawidłowe dane logowania
* 400 brak wymaganych parametrow

### Wylogowanie
POST /logout

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| api-key | wymagany | aktualny klucz użytkownika | |

Parametry:
```javascript
{
    api-key:[string]
}
```

Statusy odpowiedzi:
* 200 wylogowanie powiodlo sie
* 400 brak wymaganych parametrow

### Tworzenie nowego uzytkownika
POST /register

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| login | wymagany | login uzytkownika | |
| password | wymagany | haslo uzytkownika| |
| password_confirmation | wymagany | powtorzone hasło użytkownika | |

```javascript
{
    login: [string],
    password : [string], 
    password_confirmation : [string]
}
```

Statusy odpowiedzi:
* 201 utworzono nowego uzytkownika
* 409 użytkownik o podanych danych istnieje
* 400 brak wymaganych parametrow

# Operacja na zasobach


## Zasoby

### Pobranie listy zasobów(monitorów)
GET /resources

Zwraca liste zasobów.

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| names | opcjonalny | nazwa poszukiwanych zasobów | |
| measurement_names | opcjonalny | nazwa poszukiwanych pomiarów | |
| count | opcjonalny | ilosc zasobów | 50 |

Odpowiedź:
```javascript
{
    [
        {
            id: [long],
            name : [string]
        },
        {
            id: [long],
            name : [string]
        },
    ]
}
```

Statusy odpowiedzi:
* 200 pobrano zasoby

## Pomiary

### Pobranie pomiarów 
GET /resources/measurements

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| names | opcjonalny | nazwa poszukiwanych pomiarów | |
| time-from | opcjonalny | pomiary starsze niż podana data | |
| time-to | opcjonalny | pomiary młodsze niż podana data | |
| count | opcjonalny | ilosc pomiarów | 50 |

Odpowiedź:
```javascript
{
    [
        {
            id: [long],
            resource_id: [long],
            name : [string],
            value: [string],
            date: [string]
        },
        {
            id: [long],
            resource_id: [long],
            name : [string],
            value: [string],
            date: [string]
        },
    ]
}
```

### Pobranie pomiarów dla wybranego zasobu(monitora)
GET /resources/{resource_id}/measurements

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| names | opcjonalny | nazwa poszukiwanych pomiarów | |
| time-from | opcjonalny | pomiary starsze niż podana data | |
| time-to | opcjonalny | pomiary młodsze niż podana data | |
| count | opcjonalny | ilosc pomiarów | 50 |

Odpowiedź:
```javascript
{
    [
        {
            id: [long],
            name : [string],
            value: [string],
            date: [string]
        },
        {
            id: [long],
            name : [string],
            value: [string],
            date: [string]
        },
    ]
}
```

Statusy odpowiedzi:
* 200 pobrano pomiary
* 404 nie znaleziono zasobu o podanym id

### Utworzenie nowego pomiaru złożonego
POST /resources/{resource_id}/measurements

Parametry:
```javascript
{
    measurements_id : [long]   
}
```

Statusy odpowiedzi:
* 201 utworzono pomiar złożony
* 404 nie znaleziono zasobu o podanym id
* 401 brak autoryzacji uzytkownika

Publikuj nowy pomiar zlozony

### Usuniecie pomiaru złożonego
DELETE /resources/{resource_id}/measurements/{measurements_id}

Statusy odpowiedzi:
* 200 usunieto pomiar pomyslnie
* 404 nie znaleziono pomiaru lub zasobu o podanym id
* 401 brak autoryzacji uzytkownika
* 403 uzytkownik nie ma odpowiednich uprawnien do usuniecia pomiaru
* 409 pomiar nie jest pomiarem zlozonym