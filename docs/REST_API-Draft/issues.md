## Rzeczy do dodania:
### Do serwisu autoryzacyjnego
1.  Pobranie listy monitorów dla danego użytkownika:
    * Monitor zawiera: adres, port, nazwę, jakieś id i nazwę użytkownika, który go utworzył (albo jego ID)
    * na wejściu jwt
    * na wyjściu lista monitorów
1. Użytkownik może dodać monitor
    * na wejściu jwt i monitor
1. Użytkownik może usunąć monitor
    * na wejściu jwt i monitor (lub id monitora)

## Propozycje
### Komunikcja Sensor -> Monitor
1. "Zarejestrowanie pomiaru z sensora"
    * Zamieniłbym na "Zarejestrowanie sensora"
    * Przekazać nazwę sensora i jego metadane
    * w odpowiedzi dostajemy Id Sensora
1. "Aktualizacja metadanych pomiaru"
    * to nie wiem czy będzie potrzebne
    * do czego to planowałeś użyć?
1. "Utworzenie nowej wartosci pomiaru"
    * tutaj bym przerobił trochę
    * na wejściu sensor_id i lista: 
        [{measurement_name, date, value}, ...]
    * data może być zbędna 

* Komunikacja by wyglądała tak:
    * Sensor łączy się do Monitora i rejestruje siebie, dostaje "sensor_id"
    * Jak w bazie Monitora już istnieje taki Sensor, to zwracane jest jego id,
    * przeciwnie jest tworzony nowy i zwracane nowe id
    * po zarejestrowaniu Sensor wysyła swoje dane do Monitora w określonych interwałach czasowych
    * Monitor wrzuca dane do bazy
    * wtedy nie musimy tworzyć id dla pomiarów, posługujemy się tylko nazwą


### Komunikacja WebApka -> Monitor
1. "Pobranie pomiarów"
    * to bym wyrzucił

1. "Pobranie wartości pomiarów"
    * jako parametr wejściowy (opcjonalny) dodałbym nazwę sensora
        * jest wymaganie "Klient może przeszukiwać Monitor przy pomocy zapytań: np""wszystkie hosty, mają w nazwie ciąg ‘zeus’".
    * możemy chcieć pobrać pomiary tylko dla danego sensora
    * odpowiedź:
        * powinniśmy zwracać:
            {sensor_name, measurment_name, value, datetime}
        * wtedy mamy prostą możliwość wyświetlenia danych na wykresach
        * albo zrobić z tego płaską listę (jak wyżej)
        * albo zrobić drzewko:
            Sensor -> [pomiar (nazwa)] -> [wartości]
        * głosuję za płaską listą, bo prościej
        * ale decyzja ostateczna do Ciebie

1. "Pobranie sensorow"
    * jest ok
    * ewentualnie można dorzucić te metadane w odpowiedzi jakby ktoś chciał wyświetlić, że ta maszyna ma 9GB RAMu, nazywa się "XXX" i ma i5-3570K CPU

1. "Utworzenie nowego pomiaru złożonego"
    * tutaj trzeba trochę przerobić, bo źle zrozumiałem na początku wymaganie
    * pomiar złożony musi mieć:
        * nazwa : unikalna
        * typ : min, max, avg
        * interwał : co ile minut
        * okno czasowe : z którego ma brać pomiary
        * pattern : nazwę pomiaru, którego ma dotyczyc
        * listę sensorów : opcjonalne
        * jwt : jak teraz
    * i obsługa tego (stworzenie tych pomiarów) będzie w Monitorze na podstawie danych już istniejących
    * czyli możemy stworzyć pomiar, który pokaże średnią z zużycia CPU z ostatnich 5 minut obliczaną co minutę

1. "Usunięcie pomiaru złożonego"
    * jest ok

1. "Pobranie pomiarów złożonych"
    * na wejściu:
        * opcjonalne id pomiaru złożonego
    * na wyjściu:
        * dane pomiaru (te same co przy tworzeniu)
        * id użytkownika, który jest właścicielem
        * id pomiaru złożonego

1. "Pobranie wartości pomiarów złożonych"
    * to coś co bym dodał, żeby rozróżnić normalne pomiary od tych złożonych
    * na wejściu 
        * nazwa pomiaru (opcjonalnie)
        * id pomiaru (opcjonalnie)
        * time-from (opcjonalnie)
        * time-to (opcjonalnie)
        * count (jw)
        * offset (jw)
    * na wyjściu:
        * lista z wartościami pomiarów:
            * [nazwa, wartość, datetime]


* Komunikacja dla normalnych pomiarów by wyglądała tak:
    * wyświetlenie pomiarów na wykresie dla Monitora:
        * zawołaj "Pobranie wartości pomiarów"
        * narysuj wynik
    * wyświetlenie pomiarów złożonych na wykresie dla Monitora:
        * zawołaj "Pobranie wartości pomiarów złożonych"
        * narysuj wynik
    * stworzenie pomiaru złożonego:
        * wybierz parametry
        * zawołaj "Utworzenie nowego pomiaru złożonego"
    * usunięcie pomiaru złożonego:
        * zawołaj "Pobranie pomiarów złożonych"
        * wybierz wybrany
        * zawołaj "Usunięcie pomiaru złożonego"

    * "Pobranie sensorow"
        * to bym zostawił, bo w projekcie UI jes