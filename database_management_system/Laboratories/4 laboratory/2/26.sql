/*
 По каждому студенту вывести отношение количества пустых оценок к общему количеству оценок для этого студента.
 Формат вывода: номер з/к, % пустых.
 */
SELECT 
    pt."Номер зачетки",
    ROUND(
        COUNT(CASE WHEN sp."ResultMark" IS NULL THEN 1 END) * 100.0 / 
        NULLIF(COUNT(sp."ResultMark"), 0), 2
    ) AS "% пустых"
FROM 
    "PersonT" pt
JOIN 
    "StudentsT" st ON pt."IDPerson" = st."IDPerson"
LEFT JOIN 
    "StudPlany" sp ON st."IDStudent" = sp."Student"
GROUP BY 
    pt."Номер зачетки";