
import database, uvicorn

from time import sleep
from fastapi import FastAPI
from threading import Thread
from pyqiwip2p import QiwiP2P


qiwi_api = QiwiP2P(auth_key="=")

app = FastAPI()
    
@app.get("/api/v1/checkbalance")
async def checkbalance(phone):
    
    user:database.Users = database.Users.select().where((database.Users.phone == phone)).first()
    
    if user:
        return {"success": True, "balance": user.coins}
    
    else:
        return {"success": False, "message": "User not registered"}
    
@app.get("/api/v1/supp")
async def createbill(phone, coins):
    user:database.Users = database.Users.select().where((database.Users.phone == phone)).first()
    
    if user:
        
        bills = database.Bills.select()
        a = qiwi_api.bill(amount=coins, lifetime=60, comment="!ВЫБРАТЬ ТЕКСТ ВЫБРАТЬ!")
        
        if not bills:
            new_bill = database.Bills.create(bill_id = 1, bill = a.bill_id, user=user, coins=coins)
        else:
            new_bill_id = database.Bills.select().order_by(-database.Bills.bill_id).first().bill_id+1
            new_bill = database.Bills.create(bill_id = new_bill_id, bill = a.bill_id, user=user, coins=coins)

        new_bill.save()
        # Проверка на пополнение
        
        def checkingBill():
            while True:
                sleep(5)
                
                bill_status = qiwi_api.check(new_bill.bill).status
                
                if bill_status == "PAID":
                    good_bill:database.Bills = database.Bills.select().where((database.Bills.bill_id == new_bill.bill_id)).first()
                    good_bill.is_payed = True
                    good_bill.save()
                    
                    user.coins += good_bill.coins
                    user.save()
                    break
                
                elif bill_status == "REJECTED":
                    new_bill.status = "REJECTED"
                    new_bill.save()
                    break
                
                elif bill_status == "EXPIRED":
                    new_bill.status = "EXPIRED"
                    new_bill.save()
                    break
                
                elif bill_status == "WAITING":
                    new_bill.status = "WAITING"
                    new_bill.save()
                    pass
            
        
        Thread(target=checkingBill).start()
        return {"success": True, "message": "Bill has created", "bill": new_bill.bill, "url": a.pay_url}
    
    else:
        return {"success": False, "message": "User not exist"}
    

if __name__ == '__main__':
    uvicorn.run("main_api:app", port=8080, host='45.8.230.89', reload=True)
