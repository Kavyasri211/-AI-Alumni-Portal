import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash

DB = Path(__file__).resolve().parent / "alumni.db"

def get_db():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    c = get_db()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS users(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL,
      role TEXT NOT NULL DEFAULT 'alumni', department TEXT, skills TEXT,
      experience REAL DEFAULT 0, job_role TEXT, interests TEXT, location TEXT,
      previous_role TEXT, bio TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS news(
      id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS events(
      id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT,
      event_date TEXT, location TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS messages(
      id INTEGER PRIMARY KEY AUTOINCREMENT, sender_id INTEGER, receiver_id INTEGER,
      content TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    c.commit()
    c.close()

def seed_db():
    c = get_db()
    if c.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        rows = [
          ("Admin User","admin@gradious.com","admin123","admin","HR","HR,Recruitment,Leadership",8,"HR Manager","People,Networking","Hyderabad","HR Executive","Portal administrator"),
          ("Rahul Kumar","alumni@gradious.com","alumni123","alumni","Engineering","Python,AWS,Docker,Flask",5,"Software Engineer","Cloud,AI,Open Source","Hyderabad","Backend Developer","Cloud and backend enthusiast"),
          ("Priya Sharma","priya@gradious.com","alumni123","alumni","Engineering","Python,Azure,SQL,Machine Learning",4,"Cloud Engineer","AI,Cloud,Data","Bengaluru","Software Engineer","Cloud technology professional"),
          ("Arjun Rao","arjun@gradious.com","alumni123","alumni","Data","Python,SQL,Power BI,ML",6,"Data Analyst","Analytics,AI,Finance","Hyderabad","Data Analyst","Analytics professional"),
          ("Sneha Reddy","sneha@gradious.com","alumni123","alumni","Commerce","Excel,Finance,SQL,Communication",3,"Business Analyst","Finance,Networking,Startups","Chennai","Finance Associate","Business and finance professional"),
          ("Vikram Singh","vikram@gradious.com","alumni123","alumni","Engineering","Java,Spring,AWS,Kubernetes",7,"Senior Developer","Cloud,DevOps,Technology","Pune","Java Developer","Enterprise software engineer"),
          ("Ananya Das","ananya@gradious.com","alumni","alumni","Marketing","SEO,Content,Analytics,CRM",5,"Marketing Manager","Branding,Startups,Media","Mumbai","Marketing Executive","Digital marketing professional")
        ]
        # Correct the intentionally simple demo row format.
        rows[-1] = ("Ananya Das","ananya@gradious.com","alumni123","alumni","Marketing","SEO,Content,Analytics,CRM",5,"Marketing Manager","Branding,Startups,Media","Mumbai","Marketing Executive","Digital marketing professional")
        c.executemany("""INSERT INTO users
        (name,email,password,role,department,skills,experience,job_role,interests,location,previous_role,bio)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        [(r[0],r[1],generate_password_hash(r[2]),*r[3:]) for r in rows])
    if c.execute("SELECT COUNT(*) FROM news").fetchone()[0] == 0:
        c.executemany("INSERT INTO news(title,content) VALUES (?,?)", [
          ("Gradious Alumni Network Launch","Our AI-powered alumni portal is live."),
          ("Annual Tech Meetup","Registration is open for the annual technology alumni meetup."),
          ("Career Mentorship Program","Alumni can volunteer as mentors.")
        ])
    if c.execute("SELECT COUNT(*) FROM events").fetchone()[0] == 0:
        c.executemany("INSERT INTO events(title,description,event_date,location) VALUES (?,?,?,?)", [
          ("Alumni Networking Night","Reconnect with former colleagues and expand your network.","2026-10-15","Hyderabad"),
          ("AI & Cloud Careers","Discussion on AI, cloud and future skills.","2026-11-05","Online"),
          ("Annual Alumni Meet","A celebration and networking event.","2026-12-20","Gradious Campus")
        ])
    c.commit()
    c.close()
