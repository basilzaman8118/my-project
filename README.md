# Simple Chatbot Project (Angular + FastAPI + MySQL)

## 1. Setup Database
Import `database/schema.sql` into MySQL.

## 2. Run Backend
```
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs on http://127.0.0.1:8000

## 3. Run Frontend
Create Angular app in `frontend/` using:
```
ng new chatbot-frontend
```
Then add the files as shown in the guide.

Run frontend:
```
ng serve
```
Frontend runs on http://localhost:4200

## 4. Chat!
Ask questions like:
- What are your business hours?
- Where is your office located?
- What services do you offer?
