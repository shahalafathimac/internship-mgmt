# Internship Management Platform - Scalability, Query Optimization & System Design

## SECTION C - SCALABILITY & PROBLEM SOLVING (20 Marks)

### Question 3

### Scenario

* 1000 internships are published.
* Within 1 hour, 50,000 students apply.

---

## 1. How will your system handle this traffic?

To handle high traffic:

### Load Balancer

* Use Nginx or AWS Application Load Balancer.
* Distribute requests across multiple backend servers.

### Horizontal Scaling

* Run multiple Django application instances.
* Use Docker containers and Kubernetes (EKS) for scaling.

### Database Optimization

* Use PostgreSQL with proper indexing.
* Use read replicas for heavy read operations.

### Asynchronous Processing

* Move heavy tasks to background workers:

  * Email notifications
  * SMS notifications
  * Analytics updates
  * Application processing

### Caching

* Use Redis to reduce database load.

---

## 2. How will you prevent duplicate applications?

### Database Constraint

Create a composite unique constraint:

```python
class Application(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'internship')
```

### Validation Layer

Before creating an application:

```python
Application.objects.filter(
    student=student,
    internship=internship
).exists()
```

Even if two requests arrive simultaneously, the database constraint prevents duplicates.

---

## 3. How will you keep response time below 500ms?

### API Optimization

* Use pagination.
* Select only required fields.
* Avoid unnecessary joins.

### Database Indexing

* Create indexes on frequently searched columns.

### Redis Cache

* Cache internship details.
* Cache frequently accessed dashboards.

### Background Processing

Move:

* Emails
* SMS
* Notifications
* Analytics

to Celery workers.

### Connection Pooling

Use:

```text
PgBouncer
```

to reduce database connection overhead.

---

## 4. What indexes will you create?

### Applications Table

```sql
CREATE INDEX idx_application_student
ON applications(student_id);

CREATE INDEX idx_application_internship
ON applications(internship_id);

CREATE INDEX idx_application_created
ON applications(created_at);

CREATE INDEX idx_application_internship_created
ON applications(internship_id, created_at DESC);
```

### Internship Table

```sql
CREATE INDEX idx_internship_status
ON internships(status);

CREATE INDEX idx_internship_company
ON internships(company_id);
```

### Users Table

```sql
CREATE INDEX idx_user_email
ON users(email);
```

---

## 5. Will you use Redis?

### Yes.

Redis will be used for:

* Caching internship details
* Session storage
* Rate limiting
* Frequently accessed dashboards
* Celery broker (optional)

### Benefits

* Reduces database load
* Faster response time
* Supports high traffic

---

## 6. Will you use Queue Systems (RabbitMQ/Kafka)?

### Yes.

### RabbitMQ

Use RabbitMQ for:

* Email notifications
* SMS notifications
* Application processing
* Background jobs

### Kafka

Use Kafka when:

* Real-time analytics
* Event streaming
* Millions of events per day

For this platform, RabbitMQ is sufficient.

---

## 7. How will you scale the system?

### Application Layer

Scale horizontally:

```text
Django App 1
Django App 2
Django App 3
Django App N
```

Behind a Load Balancer.

### Database Layer

* Primary Database
* Read Replicas

```text
Primary DB
   |
Read Replica 1
Read Replica 2
```

### Cache Layer

Multiple Redis nodes.

### Queue Layer

Multiple Celery workers.

### Infrastructure

Deploy on:

* AWS EC2
* AWS ECS
* AWS EKS (Kubernetes)

Auto Scaling enabled.

---

# SECTION D - QUERY OPTIMIZATION (10 Marks)

## Question 4

### Query

```sql
SELECT *
FROM applications
WHERE internship_id = 100
ORDER BY created_at DESC;
```

Applications table contains more than 10 million records.

---

## 1. Why is the query slow?

Reasons:

### Full Table Scan

Without an index:

```text
Database checks all 10 million records.
```

### Sorting Cost

```sql
ORDER BY created_at DESC
```

requires sorting large data.

### Returning All Columns

```sql
SELECT *
```

retrieves unnecessary data.

---

## 2. How will you optimize it?

### Create Composite Index

```sql
CREATE INDEX idx_application_internship_created
ON applications(internship_id, created_at DESC);
```

### Select Required Columns

Instead of:

```sql
SELECT *
```

Use:

```sql
SELECT id,
       student_id,
       status,
       created_at
FROM applications
WHERE internship_id = 100
ORDER BY created_at DESC;
```

### Pagination

```sql
LIMIT 50;
```

Example:

```sql
SELECT id,
       student_id,
       status,
       created_at
FROM applications
WHERE internship_id = 100
ORDER BY created_at DESC
LIMIT 50;
```

---

## 3. What indexes will you create?

### Composite Index

```sql
CREATE INDEX idx_application_internship_created
ON applications(internship_id, created_at DESC);
```

### Individual Index

```sql
CREATE INDEX idx_application_internship
ON applications(internship_id);
```

---

## 4. How will you measure performance improvement?

### PostgreSQL Explain

```sql
EXPLAIN ANALYZE
SELECT *
FROM applications
WHERE internship_id = 100
ORDER BY created_at DESC;
```

Measure:

* Execution time
* Index usage
* Rows scanned

### Monitoring Tools

* PostgreSQL pg_stat_statements
* AWS CloudWatch
* New Relic
* Datadog

Example:

```text
Before Optimization : 2.5 sec
After Optimization  : 50 ms
```

---

# SECTION E - SYSTEM DESIGN (10 Marks)

## Question 5

### Backend Architecture for Internship Management Platform

---

## Modules

### Authentication Module

Responsibilities:

* Registration
* Login
* JWT Authentication
* Role Management

### Internship Management

Responsibilities:

* Create Internship
* Update Internship
* Delete Internship
* Search Internship

### Application Management

Responsibilities:

* Apply Internship
* Track Status
* Withdraw Application

### Notification Module

Responsibilities:

* Email
* SMS
* Push Notifications

### Analytics Dashboard

Responsibilities:

* Total Applications
* Internship Statistics
* User Statistics

---

# Architecture Diagram

```text
                    Users
                      |
                      |
              Load Balancer
                      |
                      |
                API Gateway
                      |
       --------------------------------
       |              |               |
       |              |               |
 Authentication  Internship     Application
    Service       Service         Service
       |              |               |
       --------------------------------
                      |
                PostgreSQL
                      |
              ----------------
              |              |
            Redis         RabbitMQ
              |              |
              |              |
            Cache      Celery Workers
                             |
                     ----------------
                     |              |
                  Email           SMS
                  Service       Service
```

---

# API Layer

Responsibilities:

* REST APIs
* Authentication
* Validation
* Rate Limiting

Technologies:

* Django REST Framework
* JWT Authentication

---

# Database Layer

Database:

```text
PostgreSQL
```

Stores:

* Users
* Internships
* Applications
* Notifications

Features:

* ACID Compliance
* Indexing
* Read Replicas

---

# Cache Layer

Technology:

```text
Redis
```

Stores:

* Frequently accessed internships
* Dashboard data
* User sessions

Benefits:

* Reduced database load
* Faster responses

---

# Queue Layer

Technology:

```text
RabbitMQ
```

Processes:

* Email sending
* SMS sending
* Analytics updates

Workers:

```text
Celery Workers
```

---

# Notification Service

Responsibilities:

### Email

* Registration Email
* Approval Email
* Rejection Email

Using:

```text
Amazon SES
```

### SMS

Using:

```text
Fast2SMS / AWS SNS
```

### Push Notifications

Using:

```text
Firebase Cloud Messaging (FCM)
```

---

# Final Technology Stack

| Layer           | Technology            |
| --------------- | --------------------- |
| Backend         | Django REST Framework |
| Database        | PostgreSQL            |
| Cache           | Redis                 |
| Queue           | RabbitMQ              |
| Background Jobs | Celery                |
| Email           | Amazon SES            |
| SMS             | AWS SNS               |
| Authentication  | JWT                   |
| Deployment      | AWS ECS / EKS         |
| Monitoring      | CloudWatch, Datadog   |
| Load Balancer   | Nginx / AWS ALB       |

## Conclusion

The platform can efficiently handle 50,000+ applications per hour using horizontal scaling, Redis caching, RabbitMQ queues, PostgreSQL indexing, and asynchronous processing through Celery workers while maintaining response times below 500ms.
