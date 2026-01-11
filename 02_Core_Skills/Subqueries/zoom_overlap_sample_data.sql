-- Sample Data for dim_meetings_zoom
-- This creates meetings with various overlapping and non-overlapping time ranges

INSERT INTO
    dim_meetings_zoom (
        meeting_id,
        organizer_id,
        start_timestamp,
        end_timestamp
    )
VALUES
    -- User 1's meetings (organizer)
    (
        1001,
        1,
        '2022-12-06 09:00:00',
        '2022-12-06 10:00:00'
    ), -- Morning meeting
    (
        1002,
        1,
        '2022-12-06 14:00:00',
        '2022-12-06 15:30:00'
    ), -- Afternoon meeting

-- User 2's meetings (organizer)
(
    2001,
    2,
    '2022-12-06 09:30:00',
    '2022-12-06 11:00:00'
), -- Overlaps with 1001
(
    2002,
    2,
    '2022-12-06 13:00:00',
    '2022-12-06 14:00:00'
), -- No overlap

-- User 3's meetings (organizer)
(
    3001,
    3,
    '2022-12-06 14:15:00',
    '2022-12-06 15:00:00'
), -- Overlaps with 1002
(
    3002,
    3,
    '2022-12-06 16:00:00',
    '2022-12-06 17:00:00'
), -- No overlap

-- User 4's meetings (organizer)
(
    4001,
    4,
    '2022-12-06 10:00:00',
    '2022-12-06 11:00:00'
), -- No overlap
(
    4002,
    4,
    '2022-12-06 15:00:00',
    '2022-12-06 16:00:00'
);
-- Overlaps with 1002

-- Sample Data for fact_participations_zoom
-- This shows who was invited to which meetings

INSERT INTO
    fact_participations_zoom (
        meeting_id,
        participant_id,
        status
    )
VALUES
    -- Meeting 1001 (User 1 organizes, User 2 invited)
    (1001, 2, 'Confirmed'),

-- Meeting 2001 (User 2 organizes, User 1 invited) - OVERLAP with 1001!
(2001, 1, 'Confirmed'),

-- Meeting 1002 (User 1 organizes, User 3 and 4 invited)
(1002, 3, 'Confirmed'), (1002, 4, 'Not confirmed'),

-- Meeting 3001 (User 3 organizes, User 1 invited) - OVERLAP with 1002!
(3001, 1, 'Confirmed'),

-- Meeting 4002 (User 4 organizes, User 1 invited) - OVERLAP with 1002!
(4002, 1, 'Confirmed'),

-- Meeting 2002 (User 2 organizes, no overlaps)
(2002, 5, 'Confirmed'),

-- Meeting 3002 (User 3 organizes, no overlaps)
(3002, 6, 'Confirmed'),

-- Meeting 4001 (User 4 organizes, no overlaps)
(4001, 7, 'Confirmed');