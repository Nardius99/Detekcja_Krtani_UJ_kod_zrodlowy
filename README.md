# Detekcja_Krtani_UJ_kod_zrodlowy
    - poniżej znajduje się podział oraz krótki opis działania danego skryptu

1. PRZYGOTOWANIE DANYCH
split_dataset.ps1 - budowa zbioru: rozpakowanie eksportów, próbkowanie, podział po nagraniach, balansowanie tła
data.yaml - konfiguracja zbioru

2. TRENING
train.py - trening YOLOv8n, model bazowy
train_yolov8s.py - trening YOLOv8s, eksperyment porównawczy

3. EWAULACJA
evaluate_test.py - ewaluacja na zbiorze testowym
measure_fps.py - pomiar czasu przetwarzania

4. AUDYT BŁĘDÓW
znajdz_bledy.py - podstawa podrozdziału 4.6
