# Chat with SQL

- [Deployment Link](https://gen-ai-8tyoexmjh3w9wlv33qrube.streamlit.app/)
- Connect to cloud or remote MySQL or Postgres SQL servers
- @TODO: Expose this Chat with SQL into REST API (Using FastAPI), allows other Typescript/Java Backend to query the ChatBot

## Installation

```zsh
pip install -r requirements.txt
```

## Environment

- create a `.env` file, with `GROQ_API_KEY`

## Running locally

```zsh
  streamlit run app.py
```

## Chat with Cloud Postgres DB

- Ask AI about which Home in Airbnb listing, with price less than 500$ a night, given a Postgres database

![PostgresChat](./PostgresChat.png)

- Give your own `Postgres` or `MySQL` connect, and ask AI about your data
- Use my Supabase Postgres DBs to test. Schema as following:
- ![HomeBookingDB](./HomeBookingDB.png)
- ![JobPostingDB](./JobPostingDB.png)

## SQLLite Chat with local DB

- Ask the AI about which students are studying data sciences (Using local SQLLite).
- Sample local SQLLite Database [student.db](./student.db)

```sql
  Krish,Data Science,A,90
  John,Data Science,B,100
  Mukesh,Data Science,A,86
  Jacob,DEVOPS,A,50
  Dipesh,DEVOPS,A,35
```

![Chat With SQL Lite](./ChatWithSQLLite.png)

## Possible usages

- Ecommerce: allows customers to ask about their orders, finding products

## Alternatives

- Using prompt template, to let AI knows the schema and context, and limit access to user-authorized data only
- Instead of chatting with SQL, we can also embed the whole SQL database entries into vectorstore. This will also allow `similarity search`
