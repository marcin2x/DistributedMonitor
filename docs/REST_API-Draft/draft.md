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

```javascript
{
    jwt:[string]
}
```

Statusy odpowiedzi:
* 200 wylogowanie powiodlo sie
* 400 brak wymaganych parametrow

# Operacja na zasobach
## Pomiary

### Pobranie pomiarów 
GET /measurements

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| names | opcjonalny | nazwa poszukiwanych pomiarów | |
| count | opcjonalny | ilosc pomiarów | 50 |
| offset | opcjonalny | ilosc ignorowanych pierwszych wyników(do stronnicowania) | 0 |

Odpowiedź:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| id | wymagany | id pomiaru | |
| name | wymagany | nazwa pomiaru |  |


```javascript
{
    [
        {
            id: [long],
            name : [string],
        },
        {
            id: [long],
            name : [string],
        },
    ]
}
```

Statusy odpowiedzi:
* 200 pobrano pomiary


### Pobranie wartości pomiarów
GET /measurements/values

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| measurement-names | opcjonalny | nazwa poszukiwanych pomiarów | |
| time-from | opcjonalny | pomiary starsze niż podana data | |
| time-to | opcjonalny | pomiary młodsze niż podana data | |
| count | opcjonalny | ilosc pomiarów | 50 |
| offset | opcjonalny | ilosc ignorowanych pierwszych wyników(do stronnicowania) | 0 |

Odpowiedź:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| measurment_id | wymagany | id pomiaru |  |
| measurment_name | wymagany | nazwa pomiaru |  |
| value | wymagany | wartość pomiaru |  |
| date | wymagany | data pomiaru |  |

```javascript
{
    [     
                                     
        {
            measurment_id: [long],
            measurment_name : [string], 
            values : 
            [
                {
                    value: [string],
                    date: [string]
                },
                {
                    value: [string],
                    date: [string]
                }
            ]
        },
        {
            measurment_id: [long],
            measurment_name : [string], 
            values : 
            [
                {
                    value: [string],
                    date: [string]
                },
                {
                    value: [string],
                    date: [string]
                }
            ]
        }   
    ]
}
```

Statusy odpowiedzi:
* 200 pobrano pomiary

### Pobranie ostatnich wartości pomiaru
GET /measurements/{id}/values

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| time-from | opcjonalny | pomiary starsze niż podana data | |
| time-to | opcjonalny | pomiary młodsze niż podana data | |
| count | opcjonalny | ilosc pomiarów | 50 |
| offset | opcjonalny | ilosc ignorowanych pierwszych wyników(do stronnicowania) | 0 |

Odpowiedź:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| value | wymagany | wartość pomiaru |  |
| date | wymagany | data pomiaru |  |

```javascript
{
   
	values : 
	[
		{
			value: [string],
			date: [string]
		},
		{
			value: [string],
			date: [string]
		}
	]
   
}
```

Statusy odpowiedzi:
* 200 pobrano pomiary


### Utworzenie nowego pomiaru złożonego
POST /measurements

Nalezy dołączyć nagłówek:

"Authorization" : [jwt]

jwt - JSON Web Token

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| measurements_id | wymagany | id pomiaru, na podstawie którego tworzony jest pomiar zlozony | |
| time-from | opcjonalny | pomiary starsze niż podana data | |
| time-to | opcjonalny | pomiary młodsze niż podana data | |


```javascript
{
    measurements_id : [long],
    time-from: [string],
    time-to: [string]
}
```

Odpowiedź:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| measurement_id | wymagany | id nowo utworzonego pomiaru | |


```javascript
{
    measurement_id: [long]
}    
```    

Statusy odpowiedzi:
* 201 utworzono pomiar złożony
* 404 nie znaleziono pomiaru o podanym id
* 401 brak autoryzacji uzytkownika


### Usuniecie pomiaru złożonego
DELETE /measurements/{measurements_id}

Nalezy dołączyć nagłówek:

"Authorization" : [jwt]

jwt - JSON Web Token

Statusy odpowiedzi:
* 200 usunieto pomiar pomyslnie
* 404 nie znaleziono pomiaru o podanym id
* 401 brak autoryzacji uzytkownika
* 403 uzytkownik nie ma odpowiednich uprawnien do usuniecia pomiaru
* 409 pomiar nie jest pomiarem zlozonym
