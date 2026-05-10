# Sample SQL Queries Used in the App

## Show all events with organization name
```sql
SELECT e.title, e.eventDate, e.startTime, e.location, o.orgName
FROM Event e
JOIN Organization o ON e.orgID = o.orgID
ORDER BY e.eventDate, e.startTime;
```

## Show RSVP list with student and event information
```sql
SELECT s.firstName, s.lastName, s.BMCCemail, e.title, e.eventDate, r.status
FROM RSVP r
JOIN Student s ON r.studentID = s.studentID
JOIN Event e ON r.eventID = e.eventID
ORDER BY e.eventDate;
```

## Count RSVPs per event
```sql
SELECT e.title, COUNT(r.rsvpID) AS totalRSVPs
FROM Event e
LEFT JOIN RSVP r ON e.eventID = r.eventID
GROUP BY e.eventID, e.title;
```

## Calculate seats left per event
```sql
SELECT e.title, e.capacity,
       e.capacity - COUNT(r.rsvpID) AS seatsLeft
FROM Event e
LEFT JOIN RSVP r ON e.eventID = r.eventID AND r.status = 'Confirmed'
GROUP BY e.eventID, e.title, e.capacity;
```

## Count events by category
```sql
SELECT category, COUNT(*) AS eventCount
FROM Event
GROUP BY category
ORDER BY eventCount DESC;
```

## Students with multiple RSVPs
```sql
SELECT s.firstName, s.lastName, COUNT(r.rsvpID) AS rsvpCount
FROM Student s
JOIN RSVP r ON s.studentID = r.studentID
GROUP BY s.studentID, s.firstName, s.lastName
HAVING COUNT(r.rsvpID) >= 2;
```
