/*
 Найти всех студентов выпускного курса (10-й семестр), которые претендуют на получение красного диплома,
 если известно, что для получения красного диплома у студента должно быть не более 15% отметок
 «хорошо» по экзаменам и диф. зачетам (остальные отметки «отлично»).
 */

 WITH StudentMarks AS (
    SELECT
        st."IDStudent",
        st."IDPerson",
        COUNT(*) AS TotalMarks,
        COUNT(CASE WHEN m."Mark" = 4 THEN 1 END) AS GoodMarks,
        COUNT(CASE WHEN m."Mark" = 5 THEN 1 END) AS ExcellentMarks
    FROM
        "StudentsT" st
    JOIN
        "StudPlany" sp ON st."IDStudent" = sp."Student"
    JOIN
        "Mark" m ON sp."IDStudPlan" = m."TStudPlan"
    WHERE
        st."Semestr" = 10 -- Выпускной курс (10-й семестр)
        AND (m."ExamType" = 'экзамен' OR m."ExamType" = 'диф. зачет') -- Учитываем только экзамены и диф. зачеты
    GROUP BY
        st."IDStudent", st."IDPerson"
)
SELECT
    sm."IDStudent",
    p."Фам",
    p."Имя",
    p."Отч",
    sm.TotalMarks,
    sm.GoodMarks,
    sm.ExcellentMarks,
    ROUND((sm.GoodMarks * 100.0 / sm.TotalMarks), 2) AS GoodMarksPercentage
FROM
    StudentMarks sm
JOIN
    "Persons" p ON sm."IDPerson" = p."IDPersons"
WHERE
    sm.GoodMarks * 100.0 / sm.TotalMarks <= 15; -- Условие для красного диплома