# Autoryzacja

### Logowanie
POST /login

Parametry:
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

### Wylogowanie
POST /logout

Parametry:
```javascript
{
    api-key:[string]
}
```

Statusy odpowiedzi:
* 200 wylogowanie powiodlo sie

### Tworzenie nowego uzytkownika
POST /register

Parametry:
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

# Operacja na zasobach


## Zasoby

### Pobranie listy zasobów(monitorów)
GET /resources

Zwraca liste zasobóow.

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| names | opcjonalny | nazwa poszukiwanych zasobów | |
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
*200 pobrano zasoby

## Pomiary

### Pobranie pomiarów dla wybranego zasobu(monitora)
GET /resources/{resource_id}/measurements

Zwraca liste pomiarów dla podanego zasobu.

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| names | opcjonalny | nazwa poszukiwanych pomiarów | |
| count | opcjonalny | ilosc pomiarów | 50 |

Odpowiedź:
```javascript
{
    [
        {
            id: [long],
            name : [string],
            value: [string]
        },
        {
            id: [long],
            name : [string],
            value: [string]
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

{
    measurements_id : [long],    
}

Statusy odpowiedzi:
* 201 utworzono pomiar złożony
* 404 nie znaleziono zasobu o podanym id
* 401 brak autoryzacji uzytkownika

Publikuj nowy pomiar zlozony

### Usuniecie pomiaru złożonego
DELETE /resources/{resource_id}/measurements/{measurements_id}

usuwa dany pomiar zlozony

Statusy odpowiedzi:
* 200 usunieto pomiar pomyslnie
* 404 nie znaleziono pomiaru lub zasobu o podanym id
* 401 brak autoryzacji uzytkownika
* 403 uzytkownik nie ma odpowiednich uprawnien do usuniecia pomiaru
* 409 pomiar nie jest pomiarem zlozonym