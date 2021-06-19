
dsmr telegram data types
=====

Electricity
-----

name                                                                       | key             | value
---------------------------------------------------------------------------|-----------------|-------------------------|
Equipment identifier                                                       | 0-0:96.1.1.255  | string
Meter Reading electricity delivered to client (low tariff) in 0,001 kWh    | 1-0:1.8.1.255   |
Meter Reading electricity delivered to client  (normaltariff) in 0,001 kWh | 1-0:1.8.2.255   |
Meter Reading electricity delivered by client  (lowtariff) in 0,001 kWh    | 1-0:2.8.1.255   |
Meter Reading electricity delivered by client  (normaltariff) in 0,001 kWh | 1-0:2.8.2.255   |
Tariff indicator electricity. The tariff indicator can be used to switch tariff dependent loads e.g boilers. This is responsibility of the P1 user   | 0-0:96.14.0.255    |
Actual electricity power delivered (+P) in 1 Watt resolution               | 1-0:1.7.0.255   |
Actual electricity power received (-P) in 1 Watt resolution                | 1-0:2.7.0.255   |
Number of power failures in any phases                                     | 0-0:96.7.21.255 |
Number of long power failures in any phases                                | 0-0:96.7. 9.255 |
Power failure event log                                                    | 1-0:99:97.0.255 |
Number of voltage sags in phase L1                                         | 1-0:32.32.0.255 |
Number of voltage sags in phase L2                                         | 1-0:52.32.0.255 |
Number of voltage sags in phase L3                                         | 1-0:72.32.0.255 |
Number of voltage swells in phase L1                                       | 1-0:32.36.0.255 |
Number of voltage swells in phase L2                                       | 1-0:52.36.0.255 |
Number of voltage swells in phase L3                                       | 1-0:72.36.0.255 |
Instantaneous voltage L1                                                   | 1-0:32.7.0.255  |
Instantaneous voltage L2                                                   | 1-0:52.7.0.255  |
Instantaneous voltage L3                                                   | 1-0:72.7.0.255  |
Instantaneous current L1                                                   | 1-0:31.7.0.255  |
Instantaneous current L2                                                   | 1-0:51.7.0.255  |
Instantaneous current L3                                                   | 1-0:71.7.0.255  |
Instantaneous active power L1 (+P)                                         | 1-0:21.7.0.255  |
Instantaneous active power L2 (+P)                                         | 1-0:41.7.0.255  |
Instantaneous active power L3 (+P)                                         | 1-0:61.7.0.255  |
Instantaneous active power L1 (-P)                                         | 1-0:22.7.0.255  |
Instantaneous active power L2 (-P)                                         | 1-0:42.7.0.255  |
Instantaneous active power L3 (-P)                                         | 1-0:62.7.0.255  |



Gas
-----




