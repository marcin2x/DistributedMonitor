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


Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| jwt | wymagany | JSON Web Token | |

```javascript
{
    jwt:[string]
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

### Zarejestrowanie pomiaru z sensora 
POST /measurements

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| sensor_name | wymagany | nazwa sensora | |
| measurement_name | wymagany | nazwa pomiaru |  |
| metadata  | wymagany | metadane o pomiarze |  |

```javascript
{
    sensor_name: [string],
    measurement_name : [string]
    metadata  : [object]
}
```
Odpowiedź:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| sensor_id | wymagany | id sensora | |
| measurement_id | wymagany | id pomiaru | |


```javascript

{
    sensor_id: [long],
    measurement_id: [long]
}    
```    

Statusy odpowiedzi:
* 201 utworzono nowy pomiar z sensora
* 409 pomiar o takiej nazwie z podanego sensora juz istnieje

### Aktualizacja metadanych pomiaru 
PUT /measurements/{measurement_id}

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| sensor_id | wymagany | id sensora | |
| metadata  | wymagany | metadane o pomiarze |  |

```javascript
{
    sensor_id: [long],
    metadata  : [object]
}
```
Statusy odpowiedzi:
* 20 zaktualizowano metadane sensora
* 404 sensor lub pomiar o podanym id nie istnieje

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

### Utworzenie nowej wartosci pomiaru
POST /measurements/{measurement_id}

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| sensor_id | wymagany | id sensora, z ktorego przychodzi pomiar | 
| value_id | wymagany | wartośc pomiaru | |
| date | wymagany | data pomiaru | |


```javascript
{
    sensor_id : [long],
    value : [string],
    date : [string]
    
}
```

Statusy odpowiedzi:
* 201 utworzono pomiar złożony
* 400 brak wymaganych danych
* 404 nie znaleziono sensora lub pomiaru o podanym id


### Utworzenie nowego pomiaru złożonego
POST /measurements/complex

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| measurements_id | wymagany | id pomiaru, na podstawie którego tworzony jest pomiar zlozony | |
| time-from | opcjonalny | pomiary starsze niż podana data | |
| time-to | opcjonalny | pomiary młodsze niż podana data | |
| jwt | wymagany | JSON Web Token | |


```javascript
{
    measurements_id : [long],
    time-from: [string],
    time-to: [string],
    jwt : [string]
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
DELETE /measurements/complex/{measurements_id}

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| jwt | wymagany | JSON Web Token | |

Statusy odpowiedzi:
* 200 usunieto pomiar pomyslnie
* 404 nie znaleziono pomiaru o podanym id
* 401 brak autoryzacji uzytkownika
* 403 uzytkownik nie ma odpowiednich uprawnien do usuniecia pomiaru
* 409 pomiar nie jest pomiarem zlozonym