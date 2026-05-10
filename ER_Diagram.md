# Mermaid ER Diagram

```mermaid
erDiagram
    STUDENT ||--o{ RSVP : makes
    EVENT ||--o{ RSVP : receives
    ORGANIZATION ||--o{ EVENT : hosts
    EVENTCATEGORY ||--o{ EVENT : groups

    STUDENT {
        int studentID PK
        text firstName
        text lastName
        text BMCCemail UK
        text major
        text yearLevel
    }

    ORGANIZATION {
        int orgID PK
        text orgName
        text orgType
        text category
        text contactEmail
        text description
    }

    EVENTCATEGORY {
        int categoryID PK
        text categoryName UK
        text description
    }

    EVENT {
        int eventID PK
        text title
        text eventDate
        text startTime
        text location
        text category FK
        text description
        int capacity
        int orgID FK
    }

    RSVP {
        int rsvpID PK
        int studentID FK
        int eventID FK
        text rsvpDate
        text status
    }
```

## Primary Key and Foreign Key Explanation

A primary key uniquely identifies each row in a table. For example, `studentID` uniquely identifies each student, and `eventID` uniquely identifies each event.

A foreign key connects one table to another table. For example, `Event.orgID` connects each event to the organization that hosts it. `RSVP.studentID` connects an RSVP to a student, and `RSVP.eventID` connects an RSVP to an event.

The RSVP table works as an associative table because students and events have a many-to-many relationship. One student can RSVP to many events, and one event can have many students.
