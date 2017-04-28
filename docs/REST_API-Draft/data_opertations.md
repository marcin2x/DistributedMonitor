# Operacja na zasobach
## Pomiary

### Pobranie pomiarów złożonych
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
| type | wymagany | typ zlozonego pomiaru(avg, min, max) | |
| interval | wymagany | co ile minut obliczany pomiar złożony | |
| window | wymagany | w jakim okresie tworzony byl pomiar | |
| measurement_id | wymagany | id pomiaru z którego tworzony jest pomiar złożony | |
| user_id | wymagany | id użytkownika do którego należy pomiar | |


```javascript
{
    [
        {
            id: [long],
            name : [string],
			type : [string],
			interval : [long],
			window : [date interval]
			measurement_id : [long],
			user_id: [long]
        },
        {
            id: [long],
            name : [string],
			type : [string],
			interval : [long],
			window : [date interval]
			measurement_id : [long],
			user_id: [long]
        },
    ]
}
```

Statusy odpowiedzi:
* 200 pobrano pomiary złożone

### Pobranie wartości pomiarów
GET /measurements/values

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| measurement_id | opcjonalny | id poszukiwanego pomiarów | |
| host_name | opcjonalny | nazwa hosta, z których pochodzi pomiar | |
| time_from | opcjonalny | pomiary starsze niż podana data | |
| time_to | opcjonalny | pomiary młodsze niż podana data | |
| count | opcjonalny | ilosc pomiarów | 50 |
| offset | opcjonalny | ilosc ignorowanych pierwszych wyników(do stronnicowania) | 0 |
| only_complex | opcjonalny | tylko pomiary złożone | false |

Odpowiedź:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| host_name | wymagany | nazwa hosta |  |
| measurement_id | wymagany | id pomiaru |  |
| value | wymagany | wartość pomiaru |  |
| date | wymagany | data pomiaru |  |

```javascript
{
    [     
                                     
        {
            host_name: [string],
            measurement_id : [string],
			value: [double],	
            date: [string]
        },
        {
            host_name: [string],
            measurement_id : [string],
			value: [double],	
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
| time_from | opcjonalny | pomiary starsze niż podana data | |
| time_to | opcjonalny | pomiary młodsze niż podana data | |
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
| measurement_id | wymagany | id pomiaru z którego tworzony jest pomiar złożony | |


```javascript
{
    name : [string],
    type : [string],
    interval : [long],
    measurement_id : [long]
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

### Pobranie hostów 
GET /hosts

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| name | opcjonalny | nazwa poszukiwanych hostów | |
| count | opcjonalny | ilosc hostów | 50 |
| offset | opcjonalny | ilosc ignorowanych pierwszych wyników(do stronnicowania) | 0 |

Odpowiedź:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| id | wymagany | id hosta | |
| name | wymagany | nazwa hosta |  |
| measurements | wymagany | pomiary hosta |  |
| metadata | wymagany | metadane hosta |  |


```javascript
{
    [
        {
            id: [long],
            name : [string],
            measurements : [{
								id: [long],
								description : [string]
							},
							{
								id: [long],
								description : [string]
							}],
			metadata: [{
							key : [string],
							value: [string]
						},
						{
							key : [string],
							value: [string]
						}]
        },
        {
            id: [long],
            name : [string],
            measurements : [{
								id: [long],
								description : [string]
							},
							{
								id: [long],
								description : [string]
							}],
			metadata: [{
							key : [string],
							value: [string]
						},
						{
							key : [string],
							value: [string]
						}]
        },
    ]
}
```

Statusy odpowiedzi:
* 200 pobrano sensory
