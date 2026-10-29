-- 1. Усі завдання певного користувача (user_id = 1)
SELECT * FROM tasks WHERE user_id = 1;

-- 2. Завдання зі статусом 'new' (підзапит)
SELECT * FROM tasks
WHERE status_id = (SELECT id FROM status WHERE name = 'new');

-- 3. Оновити статус конкретного завдання (id = 1) на 'in progress'
UPDATE tasks
SET status_id = (SELECT id FROM status WHERE name = 'in progress')
WHERE id = 1;

-- 4. Користувачі, які не мають жодного завдання
SELECT * FROM users
WHERE id NOT IN (SELECT user_id FROM tasks);

-- 5. Додати нове завдання для конкретного користувача (user_id = 1)
INSERT INTO tasks (title, description, status_id, user_id)
VALUES (
    'New task',
    'Task added by query',
    (SELECT id FROM status WHERE name = 'new'),
    1
);

-- 6. Усі завдання, які ще не завершено
SELECT * FROM tasks
WHERE status_id <> (SELECT id FROM status WHERE name = 'completed');

-- 7. Видалити конкретне завдання (id = 2)
DELETE FROM tasks WHERE id = 2;

-- 8. Знайти користувачів з певною електронною поштою (за шаблоном)
SELECT * FROM users WHERE email LIKE '%@example.com';

-- 9. Оновити ім'я користувача (id = 1)
UPDATE users SET fullname = 'Yelyzaveta Perkova' WHERE id = 1;

-- 10. Кількість завдань для кожного статусу
SELECT s.name, COUNT(t.id) AS tasks_count
FROM status AS s
LEFT JOIN tasks AS t ON t.status_id = s.id
GROUP BY s.id, s.name;

-- 11. Завдання користувачів із певним доменом електронної пошти
SELECT t.*
FROM tasks AS t
JOIN users AS u ON u.id = t.user_id
WHERE u.email LIKE '%@example.com';

-- 12. Завдання без опису
SELECT * FROM tasks WHERE description IS NULL OR description = '';

-- 13. Користувачі та їхні завдання зі статусом 'in progress'
SELECT u.fullname, t.title, s.name AS status
FROM users AS u
INNER JOIN tasks AS t ON t.user_id = u.id
INNER JOIN status AS s ON s.id = t.status_id
WHERE s.name = 'in progress';

-- 14. Користувачі та кількість їхніх завдань (включно з тими, що без завдань)
SELECT u.id, u.fullname, COUNT(t.id) AS tasks_count
FROM users AS u
LEFT JOIN tasks AS t ON t.user_id = u.id
GROUP BY u.id, u.fullname;
