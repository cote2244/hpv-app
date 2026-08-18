from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. หมวดข้อมูล: ความเสี่ยงต่ำ ---
data_negative = {
    "result_type": "Negative",
    "risk_level": "✅ ต่ำ", 
    "color_theme": "#28a745", 
    "message": "ผลตรวจไม่พบเชื้อไวรัส HPV สายพันธุ์เสี่ยงสูง บริเวณปากมดลูกอยู่ในเกณฑ์ปกติ มีความเสี่ยงต่ำมากในการเกิดมะเร็งปากมดลูกในปัจจุบัน", 
    "advice": [
        "ดูแลสุขภาพทั่วไป รักษาสุขอนามัยของระบบสืบพันธุ์", 
        "เข้ารับการตรวจคัดกรองมะเร็งปากมดลูกซ้ำอีกครั้งในอีก 5 ปี",
        "ใช้ถุงยางอนามัยเมื่อมีความเสี่ยง",
        "หากระหว่างนี้มีอาการผิดปกติ เช่น มีเลือดออกหลังมีเพศสัมพันธ์ เลือดออกผิดปกติทางช่องคลอด หรือตกขาวมีกลิ่นเหม็นผิดปกติ ให้มาพบแพทย์ทันทีโดยไม่ต้องรอครบ 5 ปี"
    ]
}

# --- 2. หมวดข้อมูล: ความเสี่ยงสูงมาก (HPV 16 / 18) ---
data_high_risk = {
    "result_type": "Positive HPV 16 หรือ 18",
    "risk_level": "❗ สูงมาก",
    "color_theme": "#dc3545",
    "message": "ผลตรวจพบเชื้อ HPV สายพันธุ์ 16 หรือ 18 ซึ่งเป็นกลุ่มที่มีความเสี่ยงสูงที่สุด มีโอกาสพัฒนากลายเป็นมะเร็งปากมดลูก \"การพบเชื้อไม่ได้แปลว่าเป็นมะเร็ง\" แต่หมายถึงต้องได้รับการตรวจเช็คช่องคลอดและปากมดลูกอย่างละเอียดเพิ่มเติมด้วยการตรวจส่องกล้องขยายช่องคลอดและตัดชิ้นเนื้อส่งตรวจ (Colposcopy / Biopsy) ที่โรงพยาบาลตามสิทธิการรักษา กรุณามาพบแพทย์ค่ะ",
    "advice": [
        "ทำจิตใจให้สบาย ไม่ต้องตกใจหรือวิตกกังวล การพบเชื้อตั้งแต่ระยะนี้ช่วยให้ป้องกันและรักษาได้ทันก่อนจะพัฒนากลายเป็นโรค",
        "งดสอดใส่ยา งดสวนล้างช่องคลอด และงดมีเพศสัมพันธ์ 24–48 ชั่วโมงก่อนวันนัดตรวจส่องกล้อง"
    ]
}

# --- 3. หมวดข้อมูล: สายพันธุ์เสี่ยงสูงอื่นๆ (Non 16/18) ---
data_other_risk = {
    "result_type": "Positive Non 16/18",
    "risk_level": "⚠️ สายพันธุ์เสี่ยงอื่นๆ",
    "color_theme": "#ffc107",
    "message": "ตรวจพบเชื้อ HPV สายพันธุ์เสี่ยงสูงกลุ่มอื่นๆ ซึ่งร่างกายของคนส่วนใหญ่สามารถกำจัดเชื้อชนิดนี้ออกไปได้เองตามธรรมชาติ แต่จำเป็นต้องตรวจเซลล์ปากมดลูกเพิ่มเติม (LBC) เพื่อประเมินแนวทางการรักษาต่อไป",
    "advice": [
        "รอฟังผลตรวจเช็กระดับเซลล์ (LBC) เพิ่มเติมตามที่เจ้าหน้าที่นัดหมาย",
        "พักผ่อนให้เพียงพอ ออกกำลังกายสม่ำเสมอ และรับประทานอาหารที่มีประโยชน์ เพื่อเสริมสร้างภูมิคุ้มกันร่างกายให้ช่วยกำจัดเชื้อ",
        "งดการสูบบุหรี่ (เนื่องจากการสูบบุหรี่ลดภูมิคุ้มกันบริเวณช่องคลอด ทำให้ร่างกายกำจัดเชื้อ HPV ได้ยากขึ้น)"
    ]
}

# --- ระบบจับคู่คำค้นหา (Keyword Mapping) ---
mock_db = {
    "NEGATIVE": data_negative,
    
    "HPV 16": data_high_risk,
    "HPV16": data_high_risk,
    "HPV 18": data_high_risk,
    "HPV18": data_high_risk,
    
    "POSITIVE NON 16/18": data_other_risk,
    "NON 16/18": data_other_risk,
    "HPV 31": data_other_risk,
    "HPV31": data_other_risk,
    "HPV 33": data_other_risk,
    "HPV33": data_other_risk,
    "HPV 45": data_other_risk,
    "HPV45": data_other_risk,
    "HPV 52": data_other_risk,
    "HPV52": data_other_risk,
    "HPV 58": data_other_risk,
    "HPV58": data_other_risk,
}

@app.get("/check-hpv/{code}")
async def check_hpv_result(code: str):
    search_term = code.strip().upper()
    result = mock_db.get(search_term)
    
    if not result:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลผลตรวจนี้ กรุณาพิมพ์ให้ตรงกับเอกสาร เช่น 'Negative', 'HPV 16', หรือ 'HPV 31'")
    return result
