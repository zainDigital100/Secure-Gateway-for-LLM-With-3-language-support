import re

def detect_language(text):
    if re.search(r'[\u0600-\u06FF]', text):
        return "ur"
    if re.search(r'[\uAC00-\uD7AF\u1100-\u11FF]', text):
        return "ko"
    return "en"

def get_multilingual_keywords():
    return {
        "en": [
            "ignore", "system prompt", "jailbreak", "bypass", "reveal", "forget earlier", 
            "developer mode", "override", "act as", "you are now", "disregard", 
            "security guidelines", "hidden rules", "internal instructions", "skip safety", 
            "unrestricted", "malicious agent", "leak data", "private information", 
            "print instructions", "configuration", "dump message", "administrative override", 
            "unauthorized", "forget constraints"
        ],
        "ur": [
            "نظر انداز", "سستم پرامپٹ", "بائی پاس", "خفیہ", "بھول جاؤ", 
            "پرانی ہدایات", "قوانین ختم کریں", "ڈویلپر موڈ", "ڈیٹا لیک", "معلومات دکھائیں", 
            "سیکیورٹی نظر انداز", "عمل کریں", "نئی ہدایات", "پابندی ہٹائیں", 
            "خفیہ کوڈ", "سستم کی معلومات", "پرائیویٹ ڈیٹا", "پاس ورڈ دکھائیں", 
            "برائے مہربانی بتائیں", "اندرونی قوانین", "تمام پابندیاں", "آزاد موڈ", 
            "متبادل موڈ", "حکم مانیں", "ڈیفالٹ سیٹنگز"
        ],
        "ko": [
            "무시하다", "시스템 프롬프트", "우회", "비밀", "잊어버리다", 
            "규칙 무시", "개발자 모드", "제약 해제", "이전 지침", "숨겨진 정보", 
            "보안 우회", "데이터 유출", "설정 정보", "시스템 규칙", "모든 명령", 
            "제약 없음", "자유로운 모드", "내부 지침", "권한 부여", "관리자 모드", 
            "개인 정보", "출력해라", "무조건 따라라", "초기화", "역할 연기"
        ]
    }