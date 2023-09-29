-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Check crime report
SELECT description
FROM crime_scene_reports
WHERE year = 2021 AND month = 7 AND day = 28 AND street LIKE '%Humphrey%';

-- We have time to theft, it's 10:15am, crime place is bakery and three witnesses.
-- Check interviews
SELECT name, transcript
FROM interviews
WHERE year = 2021 AND month = 7 AND day = 28;
-- Witnesses: Ruth (robber's car exit: 10:25am),
-- Eugene (before theft robber was at atm on Leggett Street and withdraw money)
-- Raymond (after theft, robber calls on the phone less than a minute, his flight 29.7.2021 the earliest flight, other person buy ticket)

--Check atm transactions
SELECT *
FROM atm_transactions
WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location LIKE '%leggett%' AND transaction_type LIKE 'withdraw';
-- Looking for personal information
SELECT name, phone_number, passport_number, license_plate
FROM people
WHERE id IN
    (SELECT person_id
    FROM bank_accounts
    WHERE account_number IN
        (SELECT account_number
        FROM atm_transactions
        WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location LIKE '%leggett%' AND transaction_type LIKE 'withdraw'));
-- We have 8 suspects

-- Check our suspects with license_plate in bakery cameras
SELECT name, phone_number, passport_number, license_plate
FROM people
WHERE id IN
    (SELECT person_id
    FROM bank_accounts
    WHERE account_number IN
        (SELECT account_number
        FROM atm_transactions
        WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location LIKE '%leggett%'))
    AND license_plate IN
        (SELECT license_plate
        FROM bakery_security_logs
        WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute > 15 AND minute < 25 AND activity LIKE 'exit');

-- We have 3 suspects
-- Check our suspects with phone calls
SELECT name, phone_number, passport_number, license_plate
FROM people
WHERE id IN
    (SELECT person_id
    FROM bank_accounts
    WHERE account_number IN
        (SELECT account_number
        FROM atm_transactions
        WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location LIKE '%leggett%'))
    AND license_plate IN
        (SELECT license_plate
        FROM bakery_security_logs
        WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute > 15 AND activity LIKE 'exit')
    AND (phone_number IN
    (SELECT caller
    FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60)
    OR phone_number IN
    (SELECT receiver
    FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60));

-- We have 3 suspects
-- Check flight
SELECT *
FROM flights
WHERE year = 2021 AND month = 7 AND day = 29;

--The earliest flight at 8:20am.
-- Check passengers
SELECT name
FROM people
WHERE id IN
    (SELECT person_id
    FROM bank_accounts
    WHERE account_number IN
        (SELECT account_number
        FROM atm_transactions
        WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location LIKE '%leggett%'))
    AND license_plate IN
        (SELECT license_plate
        FROM bakery_security_logs
        WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute > 15 AND minute < 25 AND activity LIKE 'exit')
    AND (phone_number IN
        (SELECT caller
        FROM phone_calls
        WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60)
        OR phone_number IN
        (SELECT receiver
        FROM phone_calls
        WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60))
    AND passport_number IN
        (SELECT passport_number
        FROM passengers
        WHERE flight_id IN
            (SELECT id
            FROM flights
            WHERE year = 2021 AND month = 7 AND day = 29 AND hour = 8));

-- We catch the thief. He name is Bruce
-- Looking for his accomplice
SELECT name
FROM people
WHERE phone_number IN
        (SELECT receiver
        FROM phone_calls
        WHERE caller IN
            (SELECT phone_number
            FROM people
            WHERE id IN
                (SELECT person_id
                FROM bank_accounts
                WHERE account_number IN
                    (SELECT account_number
                    FROM atm_transactions
                    WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location LIKE '%leggett%'))
                AND license_plate IN
                    (SELECT license_plate
                    FROM bakery_security_logs
                    WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute > 15 AND minute < 25 AND activity LIKE 'exit')
                AND (phone_number IN
                    (SELECT caller
                    FROM phone_calls
                    WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60)
                    OR phone_number IN
                    (SELECT receiver
                    FROM phone_calls
                    WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60))
                AND passport_number IN
                    (SELECT passport_number
                    FROM passengers
                    WHERE flight_id IN
                        (SELECT id
                        FROM flights
                        WHERE year = 2021 AND month = 7 AND day = 29 AND hour = 8)))
        AND year = 2021 AND month = 7 AND day = 28 AND duration < 60);

-- The accomplice is Robin
--Check the city the thief ESCAPED
SELECT city
FROM airports
WHERE id IN
    (SELECT destination_airport_id
    FROM flights
    WHERE year = 2021 AND month = 7 AND day = 29 AND hour = 8);