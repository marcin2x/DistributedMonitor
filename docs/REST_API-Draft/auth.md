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

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| jwt | wymagany | JSON Web Token | |
```javascript
{
    jwt : [string]
}
```

Statusy odpowiedzi:
* 200 logowanie powiodło się
* 401 nieprawidłowe dane logowania
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

### Wylogowanie
POST /logout

Nalezy dołączyć nagłówek:

"Authorization" : [jwt]

jwt - JSON Web Token

Statusy odpowiedzi:
* 200 wylogowanie powiodlo sie

## Monitory
### Pobranie monitorów 
GET /monitors

Nalezy dołączyć nagłówek:

"Authorization" : [jwt]

jwt - JSON Web Token

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| count | opcjonalny | ilosc monitorów | 50 |
| offset | opcjonalny | ilosc ignorowanych pierwszych wyników(do stronnicowania) | 0 |

Odpowiedź:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| address | wymagany | adres monitora | |
| port | wymagany | port monitora |  |
| name | wymagany | nazwa monitora |  |
| id | wymagany | id monitora |  |
| user_id | wymagany | id uzytkownika |  |


```javascript
{
    [
        {
            id: [long],
            user_id: [long],
            name : [string],
            port : [string],
            address : [string]
        },
        {
            id: [long],
            user_id: [long],
            name : [string],
            port : [string],
            address : [string]
        },
    ]
}
```

Statusy odpowiedzi:
* 200 pobrano monitory
* 401 brak autoryzacji uzytkownika

### Utworzenie nowego monitora
POST /monitors

Nalezy dołączyć nagłówek:

"Authorization" : [jwt]

jwt - JSON Web Token

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| name | wymagany | nazwa monitora | |
| port | wymagany | port monitora | |
| address | wymagany | adres monitora | |


```javascript
{
    
	name : [string],
	port : [string],
	address : [string]
	
}
```

Odpowiedź:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| monitor_id | wymagany | id nowo utworzonego monitora | |


```javascript
{
    monitor_id : [long]
}    
``` 

Statusy odpowiedzi:
* 201 utworzono monitor
* 409 monitor juz istnieje
* 401 brak autoryzacji uzytkownika

### Usuniecie monitora
DELETE /monitors/{monitors_id}

Nalezy dołączyć nagłówek:

"Authorization" : [jwt]

jwt - JSON Web Token

Statusy odpowiedzi:
* 200 usunieto monitor pomyslnie
* 404 nie znaleziono monitora o podanym id
* 401 brak autoryzacji uzytkownika
* 403 uzytkownik nie ma odpowiednich uprawnien do usuniecia monitora

