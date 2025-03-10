from flask import Flask, render_template, request
from requests import get, post
from bs4 import BeautifulSoup
import json
from time import time
from urllib.parse import quote  # Updated import

app = Flask(__name__)

# Country flag mapping (Add all countries as needed)
country_flags = {
    "AF": "🇦🇫", "AL": "🇦🇱", "DZ": "🇩🇿", "AS": "🇦🇸", "AD": "🇦🇩", "AO": "🇦🇴", "AR": "🇦🇷", "AM": "🇦🇲", 
    "AW": "🇦🇼", "AU": "🇦🇺", "AT": "🇦🇹", "AZ": "🇦🇿", "BS": "🇧🇸", "BH": "🇧🇭", "BD": "🇧🇩", "BB": "🇧🇧", 
    "BY": "🇧🇾", "BE": "🇧🇪", "BZ": "🇧🇿", "BJ": "🇧🇯", "BM": "🇧🇲", "BT": "🇧🇹", "BO": "🇧🇴", "BA": "🇧🇦", 
    "BW": "🇧🇼", "BR": "🇧🇷", "BN": "🇧🇳", "BG": "🇧🇬", "BF": "🇧🇫", "BI": "🇧🇮", "KH": "🇰🇭", "CM": "🇨🇲", 
    "CA": "🇨🇦", "CV": "🇨🇻", "KY": "🇰🇾", "CF": "🇨🇫", "TD": "🇹🇩", "CL": "🇨🇱", "CN": "🇨🇳", "CO": "🇨🇴", 
    "CR": "🇨🇷", "CU": "🇨🇺", "CY": "🇨🇾", "CZ": "🇨🇿", "DR": "🇩🇴", "DK": "🇩🇰", "DJ": "🇩🇯", "DM": "🇩🇲", 
    "DO": "🇩🇴", "EC": "🇪🇨", "EG": "🇪🇬", "SV": "🇸🇻", "GQ": "🇬🇶", "ER": "🇪🇷", "EE": "🇪🇪", "SZ": "🇸🇿", 
    "ET": "🇪🇹", "FI": "🇫🇮", "FJ": "🇫🇯", "FM": "🇫🇲", "FR": "🇫🇷", "GA": "🇬🇦", "GB": "🇬🇧", "GD": "🇬🇩", 
    "GE": "🇬🇪", "GH": "🇬🇭", "GI": "🇬🇮", "GR": "🇬🇷", "GL": "🇬🇱", "GT": "🇬🇹", "GN": "🇬🇳", "GW": "🇬🇼", 
    "GY": "🇬🇾", "HT": "🇭🇹", "HN": "🇭🇳", "HK": "🇭🇰", "HU": "🇭🇺", "IS": "🇮🇸", "IN": "🇮🇳", "ID": "🇮🇩", 
    "IR": "🇮🇷", "IQ": "🇮🇶", "IE": "🇮🇪", "IL": "🇮🇱", "IT": "🇮🇹", "JM": "🇯🇲", "JP": "🇯🇵", "JO": "🇯🇴", 
    "KZ": "🇰🇿", "KE": "🇰🇪", "KI": "🇰🇮", "KP": "🇰🇵", "KR": "🇰🇷", "KW": "🇰🇼", "KG": "🇰🇬", "LA": "🇱🇦", 
    "LV": "🇱🇻", "LB": "🇱🇧", "LS": "🇱🇸", "LR": "🇱🇷", "LY": "🇱🇾", "LI": "🇱🇮", "LT": "🇱🇹", "LU": "🇱🇺", 
    "MO": "🇲🇴", "MK": "🇲🇰", "MG": "🇲🇬", "MW": "🇲🇼", "MY": "🇲🇾", "MV": "🇲🇻", "ML": "🇲🇱", "MT": "🇲🇹", 
    "MH": "🇲🇭", "MQ": "🇲🇶", "MR": "🇲🇷", "MU": "🇲🇺", "YT": "🇾🇹", "MX": "🇲🇽", "FM": "🇫🇲", "MD": "🇲🇩", 
    "MC": "🇲🇨", "MN": "🇲🇳", "ME": "🇲🇪", "MS": "🇲🇸", "MA": "🇲🇦", "MZ": "🇲🇿", "MM": "🇲🇲", "NA": "🇳🇦", 
    "NR": "🇳🇷", "NP": "🇳🇵", "NL": "🇳🇱", "NC": "🇳🇨", "NE": "🇳🇪", "NG": "🇳🇬", "NI": "🇳🇮", "NE": "🇳🇪", 
    "NO": "🇳🇴", "NP": "🇳🇵", "NP": "🇳🇵", "OM": "🇴🇲", "PA": "🇵🇦", "PE": "🇵🇪", "PF": "🇵🇫", "PH": "🇵🇭", 
    "PK": "🇵🇰", "PL": "🇵🇱", "PT": "🇵🇹", "PR": "🇵🇷", "QA": "🇶🇦", "RO": "🇷🇴", "RU": "🇷🇺", "RW": "🇷🇼", 
    "SA": "🇸🇦", "SN": "🇸🇳", "RS": "🇷🇸", "SC": "🇸🇨", "SL": "🇸🇱", "SG": "🇸🇬", "SK": "🇸🇰", "SI": "🇸🇮", 
    "SO": "🇸🇴", "ZA": "🇿🇦", "SS": "🇸🇸", "ES": "🇪🇸", "LK": "🇱🇰", "SD": "🇸🇩", "SR": "🇸🇷", "SZ": "🇸🇿", 
    "SE": "🇸🇪", "CH": "🇨🇭", "SY": "🇸🇾", "TW": "🇹🇼", "TJ": "🇹🇯", "TZ": "🇹🇿", "TH": "🇹🇭", "TG": "🇹🇬", 
    "TO": "🇹🇴", "TT": "🇹🇹", "TN": "🇹🇳", "TR": "🇹🇷", "TM": "🇹🇲", "TC": "🇹🇨", "TV": "🇹🇻", "UG": "🇺🇬", 
    "UA": "🇺🇦", "AE": "🇦🇪", "GB": "🇬🇧", "US": "🇺🇸", "UY": "🇺🇾", "UZ": "🇺🇿", "VU": "🇻🇺", "VE": "🇻🇪", 
    "VN": "🇻🇳", "WF": "🇼🇫", "YE": "🇾🇪", "ZM": "🇿🇲", "ZW": "🇿🇼"
}

# Function to fetch TikTok user data
def info(secuid):
    try:
        url = f'https://tiktok.com/@{secuid}'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }
        r = get(url, headers=headers).text
        soup = BeautifulSoup(r, "html.parser")
        data = soup.find("script", {"id": "__UNIVERSAL_DATA_FOR_REHYDRATION__"})
        data = json.loads(data.string)
        user_info = data["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]["user"]
        stats = data["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]["stats"]

        return {
            'follower': stats.get('followerCount'),
            'following': stats.get('followingCount'),
            'likes': stats.get('heart'),
            'bio': user_info.get('signature'),
            'created': user_info.get('createTime'),
            'region': user_info.get('region'),
            'private': user_info.get('privateAccount'),
            'last_username_change': None if user_info.get('uniqueIdModifyTime') == 0 else user_info.get('uniqueIdModifyTime'),
            'last_nickname_change': user_info.get('nickNameModifyTime'),
            'profile_picture': user_info.get('avatarLarger'),
            'passkey': None
        }
    except:
        return {
            'follower': None,
            'following': None,
            'likes': None,
            'bio': None,
            'created': None,
            'region': None,
            'private': None,
            'last_username_change': None,
            'last_nickname_change': None,
            'profile_picture': None,
            'passkey': None
        }

# Function to check if TikTok account has passkey
def check_passkey(username):
    try:
        iid = int(bin(int(time()))[2:].zfill(32) + "0" * 32, 2)
        did = int(bin(int(time() + time() * 0.0004))[2:].zfill(32) + "0" * 32, 2)
        url = f'https://api16-normal-c-useast1a.tiktokv.com/passport/find_account/tiktok_username/?request_tag_from=h5&iid={iid}&device_id={did}&ac=wifi&channel=googleplay&aid=567753'
        payload = f'mix_mode=1&username={username}'
        r = post(url, data=payload).json()
        if r['message'] != 'success':
            return False

        ticket = r['data']['token']
        url = f'https://api16-normal-c-useast1a.tiktokv.com/passport/auth/available_ways/?request_tag_from=h5&not_login_ticket={ticket}&iid={iid}&device_id={did}&ac=wifi&channel=googleplay&aid=567753'
        return get(url).json()['data']['has_passkey']
    except:
        return False

# Format numbers like K, M, T for large numbers
def format_number(num):
    if num is None:
        return "Unknown"
    if num >= 1_000_000_000_000:
        return f"{num / 1_000_000_000_000:.1f}T"
    elif num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return str(num)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        user_data = info(username)
        user_data['followers'] = format_number(user_data['follower'])
        user_data['following'] = format_number(user_data['following'])
        user_data['likes'] = format_number(user_data['likes'])

        region = country_flags.get(user_data['region'], user_data['region'])
        
        # Check for passkey
        if check_passkey(username):
            user_data['passkey'] = 'Yes'

        return render_template('index.html', user_data=user_data, region=region)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
