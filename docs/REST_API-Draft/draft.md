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


## Zasoby

### Pobranie listy zasobów(monitorów)
GET /resources

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| names | opcjonalny | nazwa poszukiwanych zasobów | |
| count | opcjonalny | ilosc zasobów | 50 |
| offset | opcjonalny | ilosc ignorowanych pierwszych wyników(do stronnicowania) | 0 |

Odpowiedź:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| id | wymagany | id monitora | |
| name | wymagany | nazwa monitora | 50 |


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
| resource-names | opcjonalny | nazwa przeszukiwanych zasobów | |
| count | opcjonalny | ilosc pomiarów | 50 |
| offset | opcjonalny | ilosc ignorowanych pierwszych wyników(do stronnicowania) | 0 |

Odpowiedź:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| id | wymagany | id pomiaru | |
| resource_id | wymagany | id monitora z ktorego pochodzi pomiar | |
| name | wymagany | nazwa pomiaru |  |


```javascript
{
    [
        {
            id: [long],
            resource_id: [long],
            name : [string],
        },
        {
            id: [long],
            resource_id: [long],
            name : [string],
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
* 404 nie znaleziono zasobu o podanym id



### Pobranie wartości pomiarów
GET /resources/measurements/values

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| resource-names | opcjonalny | nazwa poszukiwanych zasobow | |
| measurement-names | opcjonalny | nazwa poszukiwanych pomiarów | |
| time-from | opcjonalny | pomiary starsze niż podana data | |
| time-to | opcjonalny | pomiary młodsze niż podana data | |
| count | opcjonalny | ilosc pomiarów | 50 |
| offset | opcjonalny | ilosc ignorowanych pierwszych wyników(do stronnicowania) | 0 |

Odpowiedź:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| resource_id | wymagany | id monitora | |
| resource_name | wymagany | nazwa monitora |  |
| measurment_id | wymagany | id pomiaru |  |
| measurment_name | wymagany | nazwa pomiaru |  |
| value | wymagany | wartość pomiaru |  |
| date | wymagany | data pomiaru |  |

```javascript
{
    [ 
        {
            resource_id: [long],
            resource_name : [string],
            measurments : 
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
        }, 
        {
            resource_id: [long],
            resource_name : [string],
            measurments : 
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
        },
    ]
}
```

Statusy odpowiedzi:
* 200 pobrano pomiary


### Utworzenie nowego pomiaru złożonego
POST /resources/{resource_id}/measurements

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| measurements_id | wymagany | id pomiaru, na podstawie którego tworzony jest pomiar zlozony | |
| jwt | wymagany | JSON Web Token | |


```javascript
{
    measurements_id : [long],
    jwt : [string]
}
```

Statusy odpowiedzi:
* 201 utworzono pomiar złożony
* 404 nie znaleziono zasobu lub pomiaru o podanym id
* 401 brak autoryzacji uzytkownika

Publikuj nowy pomiar zlozony

### Usuniecie pomiaru złożonego
DELETE /resources/{resource_id}/measurements/{measurements_id}

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| jwt | wymagany | JSON Web Token | |

Statusy odpowiedzi:
* 200 usunieto pomiar pomyslnie
* 404 nie znaleziono pomiaru lub zasobu o podanym id
* 401 brak autoryzacji uzytkownika
* 403 uzytkownik nie ma odpowiednich uprawnien do usuniecia pomiaru
* 409 pomiar nie jest pomiarem zlozonym