def gethtml(filename):
    with open(f"wwwroot/{filename}", "r", encoding="utf-8") as f:
        cnt = f.read()
    return cnt   