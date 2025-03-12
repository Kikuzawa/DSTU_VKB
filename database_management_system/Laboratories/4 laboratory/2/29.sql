/*
 Найти всех братьев и сестер и вывести разницу в годах, которую посчитать как дата рождения самого младшего за вычетом
 даты рождения самого старшего. За признак родства принимать фамилию и отчество.
 */

WITH NormalizedPatronymics AS (
    SELECT
        "Фам",
        CASE 
            WHEN RIGHT("Отч", 1) = 'а' THEN LEFT("Отч", LENGTH("Отч") - 1) -- Убираем последнюю букву 'а' для женских отчеств
            ELSE "Отч" -- Оставляем мужские отчества без изменений
        END AS NormalizedОтч,
        "ДатаРожд"
    FROM
        "Persons"
),
Siblings AS (
    SELECT
        "Фам",
        "normalizedОтч",
        MIN("ДатаРожд") AS MinBirthDate,
        MAX("ДатаРожд") AS MaxBirthDate,
        COUNT(*) AS SiblingCount
    FROM
        NormalizedPatronymics
    GROUP BY
        "Фам", "normalizedОтч"
    HAVING
        COUNT(*) > 1 -- Учитываем только тех, у кого есть братья/сестры
)
SELECT
    "Фам",
    "normalizedОтч" AS "Отч",
    EXTRACT(YEAR FROM AGE(MaxBirthDate, MinBirthDate)) AS AgeDifference
FROM
    Siblings;