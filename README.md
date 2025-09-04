# ServiceNow Incident Ticket Fetcher

This Python script connects to the **ServiceNow API**, retrieves **incident ticket data**, and stores it into a **PostgreSQL database**.  
It is designed to run efficiently by fetching **only new tickets** while maintaining an activity log for auditing and monitoring.

---

## 🚀 Features
- **Incremental Data Fetching**: Only new incident tickets are retrieved; old tickets are skipped automatically.  
- **PostgreSQL Integration**: Seamlessly inserts fetched data into a PostgreSQL database.  
- **Activity Logging**: Maintains detailed logs of API calls, database inserts, and errors for debugging and traceability.  

---

## ⚙️ Requirements
- Python 3.8+
- PostgreSQL server
- Dependencies managed with [uv](https://github.com/astral-sh/uv)

---

## 🔧 Setup

1. **Install dependencies**  
   If you have a `pyproject.toml`:
   ```bash
   uv sync
   ```

   Or install directly:
   ```bash
   uv add requests psycopg2-binary python-dotenv
   ```

2. **Environment Variables**  
   Create a `.env` file (or configure system environment variables) with the following keys:

   ```ini
   SNOW_ENDPOINT=https://your-instance.service-now.com
   SNOW_USERNAME=your-username
   SNOW_PASSWORD=your-password

   PG_HOST=localhost
   PG_DB_NAME=ritmdb
   PG_USERNAME=your-db-user
   PG_PASSWORD=your-db-password
   PG_PORT=5432
   ```

3. **Database Setup**  
   Ensure the PostgreSQL database and required tables exist.  
   Example schema:
   ```sql
   CREATE TABLE ritm_data (
	id SERIAL PRIMARY KEY,
	ticket_type TEXT,
	company TEXT,
	sys_id VARCHAR(50) UNIQUE NOT NULL,
	number VARCHAR(50) NOT NULL,
	created_by TEXT,
	created_on TIMESTAMPTZ,
	opened_by TEXT,
	opened_at TIMESTAMPTZ,
	requested_for TEXT,
	category TEXT,
	subcategory TEXT,
	priority TEXT,
	impact TEXT,
	urgency TEXT,
	quantity TEXT,
	state TEXT,
	price TEXT,
	recurring_price TEXT,
	assignment_group TEXT,
	assigned_to TEXT,
	made_sla TEXT,
	approval TEXT,
	billable TEXT,
	catalog_item TEXT,
	escalation TEXT,
	short_description TEXT,
	description TEXT,
	closed_by TEXT,
	closed_at TIMESTAMPTZ,
	close_notes TEXT,
	work_notes TEXT,
	CONSTRAINT sys_id_not_blank CHECK (btrim(sys_id) <> ''),
	CONSTRAINT number_not_blank CHECK (btrim(number) <> ''));
ALTER TABLE ritm_data OWNER TO table_owner;
   ```

---

## ▶️ Usage
Run the script with uv:
```bash
uv run main.py
```

- On the first run, it will fetch all available incident tickets.  
- On subsequent runs, it will **only fetch new tickets** that are not already present in the database.  

---

## 📜 Logs
Logs are stored in `activity.log` (configurable).  
They include:
- Successful API calls
- Number of tickets fetched
- Database insert/update results
- Errors (API or DB failures)

---

## 🛠 Future Enhancements
- Support for ticket updates (not just new ones)
- Configurable scheduling with `cron` or `APScheduler`
- Dockerization for deployment

---

## 📝 License
This project is licensed under the MIT License.
