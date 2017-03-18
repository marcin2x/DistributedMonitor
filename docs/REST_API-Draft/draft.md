# Autoryzacja

### Logowanie
POST /login

Parametry:

{
    login: [string],
    password : [string]
}

Odpowiedz:

{
    api-key : [string]
}

### Wylogowanie
POST /logout

Parametry:

{
    api-key:[string]
}

### Tworzenie nowego uzytkownika
POST /register

Parametry:

{
    login: [string],
    password : [string], 
    password_confirmation : [string]
}

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


## Pomiary

### Pobranie pomiarów dla wybranego zasobu(monitora)
GET /resources/{resource_id}/measurements

Zwraca liste pomiarów dla podanego zasobu.

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| names | opcjonalny | nazwa poszukiwanych pomiarów | |
| count | opcjonalny | ilosc pomiarów | 50 |

### Utworzenie nowego pomiaru złożonego
POST /resources/{resource_id}/measurements

Parametry:

{
    measurements_id : [long],    
}

Publikuj nowy pomiar zlozony

### Usuniecie pomiaru złożonego
DELETE /resources/{resource_id}/measurements/{measurements_id}

usuwa dany pomiar zlozony