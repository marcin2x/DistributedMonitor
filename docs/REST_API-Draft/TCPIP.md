# Flow:
Cała komunikacja jest realizowana po warstwie TCP/IP.
Sensor startuje i wysyła message typu "register". Monitor rejestruje dane w bazie i przydziela unikalne id dla pomiarów z danego monitora
(pomiary CPU dla dwóch różnych monitorów mają mieć różne ID - wymaganie od prowadzącego). 
Jeśli monitor o takim "identifier" już istnieje - dane są zwracane z bazy i aktualizowane w razie potrzeby.
W odpowiedzi Sensor dostaje swoje ID oraz ID pomiarów, które przechowuje w pamięci i używa ich przy wysyłaniu pomiarów.
Nazwa pomiaru musi być unikalna dla Sensora.
Pomiary są wysyłane co zadaną ilość czasu używając ID Sensora nadanego przy rejestracji oraz ID pomiarów.




### Rejestracja Sensora:

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| type | wymagany | typ operacji | |
| body | wymagany | dane operacji |  |
| identifier | wymagany | unikalny adres MAC sensora |  |
| name | wymagany | nazwa  sensora |  |
| measurements | wymagany | pomiary sensora |  |
| name | wymagany | unikalna nazwa pomiaru | |
| metadata | wymagany | metadane sensora | |
| key | wymagany | nazwa metadanej | |
| value | wymagany | wartość metadanej | |

{
    "type": "register",
    "body":
    {
        "identifier":"00:0A:E6:3E:FD:E1",
        "name": "Some PC Name", 
        "measurements":
        [
            {
                "name":"CPU" 
            },
            {
                "name":"RAM"
            }
        ],
        "metadata":
        [
            {
                "key": "CPU Core count",
                "value": "4"
            },
            {
                "key": "Total RAM",
                "value": "4GB"
            }
        ]
    }

}

Odpowiedź:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| type | wymagany | typ operacji | |
| body | wymagany | dane operacji |  |
| sensor_id | wymagany | id sensora |  |
| measurements | wymagany | pomiary sensora |  |
| measurements_name | wymagany | unikalna nazwa pomiaru | |
| measurements_id | wymagany | unikalne id pomiaru | |

{
    "type": "register",
    "body":
    {
        "sensor_id": 12,
        "measurements":
        [
            {
                "measurements_name":"CPU",
                "measurements_id":19
            },
            {
                "measurements_name":"RAM",
                "measurements_id":20
            }
        ],
    }
}



### Wysłanie pomiarów

Parametry:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| type | wymagany | typ operacji | |
| body | wymagany | dane operacji |  |
| sensor_id | wymagany | id sensora |  |
| values | wymagany | wartości pomiaru |  |
| measurement_id | wymagany | id pomiaru |  |
| measurement_value | wymagany | wartości pomiaru |  |


{
    "type": "data",
    "body":
    {
        "sensor_id": 12,
        "values":
        [
            {
                "measurement_id": 19, // ID pomiaru nadane przy rejestracji
                "measurement_value": "95" /// w procentach
            },
            {
                "measurement_id": 20,  // ID pomiaru nadane przy rejestracji
                "measurement_value": "15" /// w procentach
            }
        ]
    }
}

Odpowiedź:

| Nazwa | Wymagany | Opis | Domyślnie |
|-------|----------|------|-----------|
| type | wymagany | typ operacji | |
| body | wymagany | informacja o wyniku operacji(lub opis błedu) |  |

{
    "type": "data",
    "body": "OK" 
}