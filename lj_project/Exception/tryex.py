def strip(sr):
    if sr:
        sr = sr.strip()
    return sr

def split(sr, f, i):
    try:
        sr_r = sr.split(f)[i]
        return sr_r
    except:
        return None