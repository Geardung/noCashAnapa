from fastapi import FastAPI
import database

app = FastAPI()

@app.get("/api/v1/login")
async def login(phone):
    user = database.Select().where(database.Users.phone == phone).first()
    
    if user:
        # Смс или иная верификация
        verificated = True
        
        if verificated:
            return {"success": True}
        
        else:
            return {"success": False, "message": "User not registered"}
    
    else:
        return {"success": False, "message": "User not registered"}