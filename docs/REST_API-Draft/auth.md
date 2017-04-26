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

### Wylogowanie
POST /logout

Nalezy dołączyć nagłówek:

"Authorization" : [jwt]

jwt - JSON Web Token

Statusy odpowiedzi:
* 200 wylogowanie powiodlo sie
