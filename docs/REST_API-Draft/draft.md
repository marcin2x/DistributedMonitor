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
| adres | wymagany | adres monitora | |
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
            adres : [string]
        },
        {
            id: [long],
            user_id: [long],
            name : [string],
            port : [string],
            adres : [string]
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
| monitor | wymagany | obiekt zawierajacy wszystkie dane monitora | |


```javascript
{
    monitor : [object]
}
```

Odpowiedź:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| monitor_id | wymagany | id nowo utworzonego monitora | |


```javascript
{
    measurement_id: [long]
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


# Operacja na zasobach
## Pomiary


### Pobranie wartości pomiarów
GET /measurements/values

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| measurement-names | opcjonalny | nazwa poszukiwanych pomiarów | |
| sensor-names | opcjonalny | nazwa sensorów, z których pochodzi pomiar | |
| time-from | opcjonalny | pomiary starsze niż podana data | |
| time-to | opcjonalny | pomiary młodsze niż podana data | |
| count | opcjonalny | ilosc pomiarów | 50 |
| offset | opcjonalny | ilosc ignorowanych pierwszych wyników(do stronnicowania) | 0 |
| only_complex | opcjonalny | tylko pomiary złożone | false |

Odpowiedź:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| sensor-name | wymagany | nazwa sensora |  |
| measurment_name | wymagany | nazwa pomiaru |  |
| value | wymagany | wartość pomiaru |  |
| date | wymagany | data pomiaru |  |

```javascript
{
    [     
                                     
        {
            sensor-name: [string],
            measurment_name : [string],
			value: [string],	
            date: [string]
        },
        {
            sensor-name: [string],
            measurment_name : [string],
			value: [string],	
            date: [string]
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
| name | wymagany | unikalna nazwa nowo tworzonego pomiaru | |
| type | wymagany | typ zlozonego pomiaru(avg, min, max) | |
| interval | wymagany | co ile minut obliczac pomiar | |
| time-from | wymagany | pomiary starsze niż podana data | |
| time-to | wymagany | pomiary młodsze niż podana data | |
| pattern | wymagany | nazwa pomiaru, z którego tworzony jest pomiar złożony | |
| sensors_id | opcjonalny | id sensorow, z których pobierac pomiary | |


```javascript
{
    name : [string],
    type : [string],
    interval : [long],
    time-from: [string],
    time-to: [string],
    pattern: [string],
    sensors_id: [longs]
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
* 404 nie znaleziono pomiaru o podanej nazwie
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
