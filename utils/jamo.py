def extract_chosung(s) -> str:
    CHOSUNG_LIST = [
        "ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ",
        "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ",
        "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ",
        "ㅋ", "ㅌ", "ㅍ", "ㅎ",
    ]

    def divide_korean_char(ch):
        try:
            char_code = ord(ch) - 44032
            jong = char_code % 28
            jung = ((char_code - jong) // 28) % 21
            cho = ((char_code - jong) // 28) // 21

            return cho, jung, jong
        except:
            return None

    jamo_arr = []
    for c in s:
        if ord(c) < 44032 or ord(c) > 55203:
            jamo_arr.append(c)
        else:
            cho, jung, jong = divide_korean_char(c)
            jamo_arr.append(CHOSUNG_LIST[cho])

    result = "".join([x for x in jamo_arr if x in CHOSUNG_LIST])
    return result
