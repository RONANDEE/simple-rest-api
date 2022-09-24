from fastapi import FastAPI

app = FastAPI()



# New
hn_db = [
    {
	"barcode_type":"HN",
	"key":"570000027073",
	"hn":"07-14-027073",
	"prename":"เด็กหญิง",
	"firstname":"พสุดาภา",
	"lastname":"ข้อมูลทดสอบ",
	"birthdate":"2013-06-18",
	"gender":"Female"
    },
    {
        "title":"Learn Python the Hard Way",
        "price": 870
    },
    {
        "title":"JavaScript: The Definitive Guide",
        "price": 1369
    },
    {
        "title":"Python for Data Analysis",
        "price": 1394
    },
    {
        "title":"Clean Code",
        "price": 1500
    },
]

@app.get("/")
async def Homepage():
    return {"message": "Hello World"}

@app.get("/portal/api/ws/patient_info/{hn}")
async def get_hn(hn: int):
    return hn_db[hn-1]

@app.get("/portal/api/ws/patient/{hn}")
async def Test(hn: str):
    return {
	"barcode_type":"HN",
	"key":"570000027073",
	"hn":"07-14-027073",
	"prename":"เด็กหญิง",
	"firstname":"พสุดาภา",
	"lastname":"ข้อมูลทดสอบ",
	"birthdate":"2013-06-18",
	"gender":"Female"
    }
