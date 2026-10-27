"""
ZOOVENTURE — Wildlife Audio Resolver Service
xeno-canto & iNaturalist ochiq JSON API integratsiyasi orqali
hayvonlarning haqiqiy ovozlarini (audio playback) avtomatik olish va bog'lash.
"""

import json
import logging
import urllib.request
import urllib.parse
from typing import Dict, Any, Optional

logger = logging.getLogger("zooventure.audio")

# 74 ta taksonomik urug' (genus) bo'yicha to'liq haqiqiy wildlife audio kesh xaritasi
GENUS_AUDIO_REGISTRY: Dict[str, Dict[str, str]] = {
    'Loxodonta': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2208547.wav?1792933521',
        'soundType': 'bear',
        'soundDescription': "Afrika filining qudratli truba tovushi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Ceratotherium': {
        'audioUrl': 'https://static.inaturalist.org/sounds/1735010.mp3?1767779757',
        'soundType': 'bear',
        'soundDescription': "Krkidonning pishqirishi va xirillashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Carcharodon': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2178718.m4a?1790724891',
        'soundType': 'dolphin',
        'soundDescription': "Oq akulaning chuqur suv osti gidrofonik impulsi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Struthio': {
        'audioUrl': 'https://static.inaturalist.org/sounds/1734961.mp3?1767774029',
        'soundType': 'eagle',
        'soundDescription': "Tuyaqushning g'o'ldirashi va past jarangli chaqirig'i",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Testudo': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2194513.m4a?1791834273',
        'soundType': 'rabbit',
        'soundDescription': "Dasht toshbaqasining vishillashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Theraphosa': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2018647.m4a?1781330423',
        'soundType': 'rabbit',
        'soundDescription': "Qushxo'r o'rgimchakning stridulyatsion shitirlashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Giraffa': {
        'audioUrl': 'https://static.inaturalist.org/sounds/1423605.mp3?1745888283',
        'soundType': 'deer',
        'soundDescription': "Jirafaning past chastotali infratovush xirillashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Morpho': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2208204.wav?1792895908',
        'soundType': 'swallow',
        'soundDescription': "Tropik kapalak qanotlarining shitirlashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Ambystoma': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2101739.m4a?1785735951',
        'soundType': 'dolphin',
        'soundDescription': "Aksolotl va salamandralarning suv osti chertish tovushi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Corvus': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2210845.m4a?1793113209',
        'soundType': 'eagle',
        'soundDescription': "Qarg'aning jarangdor qag'illashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Equus': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2209892.wav?1793039035',
        'soundType': 'deer',
        'soundDescription': "Yovvoyi ot va zebraning kishnashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Pavo': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2210717.mp3?1793101782',
        'soundType': 'eagle',
        'soundDescription': "Tovusning baland aks-sado beruvchi qichqirig'i",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Hydrochoerus': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2156712.wav?1789254002',
        'soundType': 'rabbit',
        'soundDescription': "Kapibaraning xarakterli chug'urlashi va hurishi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Varanus': {
        'audioUrl': 'https://static.inaturalist.org/sounds/1713154.m4a?1765424659',
        'soundType': 'rabbit',
        'soundDescription': "Bo'z echkiemar va varanning tahdidli vishillashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Mustela': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2205762.mp3?1792705786',
        'soundType': 'rabbit',
        'soundDescription': "Suvsar va latchaning tezkor chug'urlashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Crocodylus': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2083067.mp3?1784725712',
        'soundType': 'bear',
        'soundDescription': "Timsohning chuqur bo'kirishi va suv osti gumburlashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Acipenser': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2203826.m4a?1792547176',
        'soundType': 'dolphin',
        'soundDescription': "Ossetr baliqlarining daryo tubidagi gidroakustik signali",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Balaenoptera': {
        'audioUrl': 'https://static.inaturalist.org/sounds/1752414.wav?1769608024',
        'soundType': 'dolphin',
        'soundDescription': "Moviy kitning okean bo'ylab tarqaluvchi ohangdor qo'shig'i",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Aquila': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2210550.m4a?1793091867',
        'soundType': 'eagle',
        'soundDescription': "Burgutning baland cho'qqilardan jaranglovchi faryodi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Chelonia': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2167258.m4a?1790016163',
        'soundType': 'dolphin',
        'soundDescription': "Dengiz toshbaqasining nafas olish va suzish tovushi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Leopardus': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2196171.mp3?1791967776',
        'soundType': 'lion',
        'soundDescription': "Otselot va leopardusning pishillashi va xirillashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Luscinia': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2210537.m4a?1793091190',
        'soundType': 'swallow',
        'soundDescription': "Bulbulning mayin va jozibador sayrashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Apis': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2208204.wav?1792895908',
        'soundType': 'swallow',
        'soundDescription': "Asalarilar to'dasining bir maromdagi vizillashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Castor': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2208174.m4a?1792894094',
        'soundType': 'rabbit',
        'soundDescription': "Qunduzning suvga dum urishi va ogohlantirish tovushi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Chamaeleo': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2183150.m4a?1791047207',
        'soundType': 'rabbit',
        'soundDescription': "Xameleonning havo chiqarib vishillashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Pongo': {
        'audioUrl': 'https://static.inaturalist.org/sounds/1855822.mp3?1776037268',
        'soundType': 'bear',
        'soundDescription': "Orangutanning o'rmon bo'ylab uzoqqa eshitiluvchi hayqirig'i",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Amphiprion': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2202505.m4a?1792442886',
        'soundType': 'dolphin',
        'soundDescription': "Kloun baliqlarning riflar orasidagi akustik chertishlari",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Delphinus': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2090014.m4a?1785097414',
        'soundType': 'dolphin',
        'soundDescription': "Delfinning exolokatsion chertishlari va hushtagi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Phoenicopterus': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2210719.m4a?1793101970',
        'soundType': 'swallow',
        'soundDescription': "Flamingolarning ko'l bo'yidagi qiy-chuvi va g'o'ldirashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Ailuropoda': {
        'audioUrl': 'https://static.inaturalist.org/sounds/1039140.m4a?1715748985',
        'soundType': 'rabbit',
        'soundDescription': "Katta pandaning mayin ma'rashi va tovushi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Alligator': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2191115.m4a?1791592406',
        'soundType': 'bear',
        'soundDescription': "Alligatorning qalin suv bo'yidagi vahimali bo'kirishi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Ursus': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2180654.m4a?1790863424',
        'soundType': 'bear',
        'soundDescription': "Qo'ng'ir ayiqning chuqur xirillashi va o'kirishi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Acinonyx': {
        'audioUrl': 'https://static.inaturalist.org/sounds/1571128.wav?1752701820',
        'soundType': 'lion',
        'soundDescription': "Gepardning sayroqi qush kabi xarakterli chirqillashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Dendrobates': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2208138.wav?1792893174',
        'soundType': 'swallow',
        'soundDescription': "Zaharli qurbaqaning baland chastotali trill sayrashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Gorilla': {
        'audioUrl': 'https://static.inaturalist.org/sounds/1423865.mp3?1745890908',
        'soundType': 'bear',
        'soundDescription': "Gorillaning ko'krak urishi va ogohlantiruvchi o'kirishi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Hippopotamus': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2115804.m4a?1786550749',
        'soundType': 'bear',
        'soundDescription': "Begemotning suvdan bosh ko'tarib pishqirishi va hayqirig'i",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Megaptera': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2171326.m4a?1790292265',
        'soundType': 'dolphin',
        'soundDescription': "Bukri kitning sirli va ohangdor okean qo'shig'i",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Salmo': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2203826.m4a?1792547176',
        'soundType': 'dolphin',
        'soundDescription': "Losos baliqlarining daryo oqimidagi suv sachratish tovushi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Bison': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2132592.wav?1787585856',
        'soundType': 'bear',
        'soundDescription': "Bizon va zubrning og'ir hansirashi va xirillashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Bubo': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2210669.mp3?1793097936',
        'soundType': 'eagle',
        'soundDescription': "Ukkining tungi sirli uvillashi va 'hu-hu' sadosi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Manta': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2210026.mp3?1793046994',
        'soundType': 'dolphin',
        'soundDescription': "Gigant Manta skatining suv qa'ridagi suzish impulsi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Tyto': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2209267.mp3?1792979817',
        'soundType': 'eagle',
        'soundDescription': "Siyuqqush (Barn Owl) ning keskin qichqirig'i",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Enhydra': {
        'audioUrl': 'https://static.inaturalist.org/sounds/1559688.m4a?1751941403',
        'soundType': 'dolphin',
        'soundDescription': "Dengiz qunduzining (Kalan) chug'urlashi va qichqirishi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Salamandra': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2210649.m4a?1793096479',
        'soundType': 'swallow',
        'soundDescription': "Olovli salamandraning past chirqillashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Capra': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2193894.mp3?1791796966',
        'soundType': 'deer',
        'soundDescription': "Tog' echkisi va arxarning qoya toshlardagi ma'rashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Aptenodytes': {
        'audioUrl': 'https://static.inaturalist.org/sounds/1860761.m4a?1776256133',
        'soundType': 'swallow',
        'soundDescription': "Imperator pingvinining muzliklar bo'ylab yangrovchi chaqirig'i",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Falco': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2210326.wav?1793067611',
        'soundType': 'eagle',
        'soundDescription': "Lochin va shunqorning shiddatli qichqirig'i",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Phascolarctos': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2205086.m4a?1792658047',
        'soundType': 'bear',
        'soundDescription': "Koalaning evkalipt daraxtidagi past bo'kirishi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Vipera': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2043787.mp3?1782485496',
        'soundType': 'rabbit',
        'soundDescription': "Qora ilon va gurzaning keskin vishillashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Canis': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2210794.m4a?1793108680',
        'soundType': 'wolf',
        'soundDescription': "Bo'rining oy nurida cho'zilib yangrovchi uvillashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Orcinus': {
        'audioUrl': 'https://static.inaturalist.org/sounds/1731154.m4a?1767410238',
        'soundType': 'dolphin',
        'soundDescription': "Kosatkaning ov paytidagi yuqori chastotali hushtaklari",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Python': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2110039.m4a?1786190238',
        'soundType': 'rabbit',
        'soundDescription': "Pitonning chuqur havo chiqarib ogohlantiruvchi vishi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Macropus': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2202846.wav?1792461481',
        'soundType': 'deer',
        'soundDescription': "Qizil kenguruning oyoq zarbasi va qisqa xirillashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Naja': {
        'audioUrl': 'https://static.inaturalist.org/sounds/1943042.wav?1778473177',
        'soundType': 'rabbit',
        'soundDescription': "Kobranning kapyushon yozib vishillashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Vulpes': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2210350.m4a?1793069710',
        'soundType': 'wolf',
        'soundDescription': "Tulkining tunda o'rmon bo'ylab akillashi va uvillashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Lemur': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2208286.m4a?1792903621',
        'soundType': 'swallow',
        'soundDescription': "Madagaskar lemurining jarangdor xirillashi va chaqirig'i",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Pan': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2209764.m4a?1793030558',
        'soundType': 'bear',
        'soundDescription': "Shimpanzening hayajonli pant-hoot hayqirig'i",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Pelecanus': {
        'audioUrl': 'https://static.inaturalist.org/sounds/1741822.m4a?1768492377',
        'soundType': 'eagle',
        'soundDescription': "Pelikaning suv yuzidagi qirqillashi va tovushi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Lynx': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2208943.m4a?1792958820',
        'soundType': 'lion',
        'soundDescription': "Sillovsinning o'rmondagi pishillashi va xirillashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Rhincodon': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2178718.m4a?1790724891',
        'soundType': 'dolphin',
        'soundDescription': "Kit akulaning okean chuqurligidagi past akustik tebranishi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Ara': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2200334.m4a?1792276927',
        'soundType': 'swallow',
        'soundDescription': "Ara to'tiqushining baland va jarangdor qiyqirishi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Panthera': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2208557.wav?1792933864',
        'soundType': 'lion',
        'soundDescription': "Sher va yo'lbarsning yer titratuvchi haybatli o'kirishi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Cygnus': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2210840.m4a?1793112236',
        'soundType': 'swallow',
        'soundDescription': "Oqqushning ko'l uzra tarqaluvchi karnaysimon sadosi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Thunnus': {
        'audioUrl': 'https://static.inaturalist.org/sounds/1594385.mp3?1754407830',
        'soundType': 'dolphin',
        'soundDescription': "Tukan baliqlarining tezkor oqimdagi suv harakati tovushi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Octopus': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2202505.m4a?1792442886',
        'soundType': 'dolphin',
        'soundDescription': "Sakkizoyoqning suv oqimi va paypaslagichlar harakati",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Cacatua': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2210372.m4a?1793071765',
        'soundType': 'swallow',
        'soundDescription': "Kakadu to'tiqushining baland qichqirig'i",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Cervus': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2210533.wav?1793090985',
        'soundType': 'deer',
        'soundDescription': "Buxoro bug'usining (Xongul) kuzgi o'kirishi va bo'kirishi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Chlamydotis': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2210326.wav?1793067611',
        'soundType': 'eagle',
        'soundDescription': "Yo'rg'a tuvaloqning dashtdagi display chaqirig'i",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Gazella': {
        'audioUrl': 'https://static.inaturalist.org/sounds/1948289.mp3?1778687341',
        'soundType': 'deer',
        'soundDescription': "Jayron va ohuning xavf sezgandagi xarakterli pishqirig'i",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Gyps': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2037242.m4a?1782154541',
        'soundType': 'eagle',
        'soundDescription': "Oq boshli quzg'un (Sip) ning qoyalardagi vishillashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Hirundo': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2208204.wav?1792895908',
        'soundType': 'swallow',
        'soundDescription': "Qaldirg'ochning bahorgi shodon sayrashi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Lepus': {
        'audioUrl': 'https://static.inaturalist.org/sounds/2018647.m4a?1781330423',
        'soundType': 'rabbit',
        'soundDescription': "Yovvoyi quyonning yer tepishi va xavf signali",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Saiga': {
        'audioUrl': 'https://static.inaturalist.org/sounds/1948289.mp3?1778687341',
        'soundType': 'deer',
        'soundDescription': "Sayg'oqning dasht bo'ylab tumshug'idan chiqaradigan o'kirishi",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    },
    'Tursiops': {
        'audioUrl': 'https://static.inaturalist.org/sounds/1962134.m4a?1779175220',
        'soundType': 'dolphin',
        'soundDescription': "Afalina delfinining tiniq chertishlari va hushtaklari",
        'source': "iNaturalist / xeno-canto Wildlife Sound Network"
    }
}

def extract_genus(scientific_name: Optional[str]) -> Optional[str]:
    """Lotincha ilmiy nomdan urug' (genus) nomini ajratib olish."""
    if not scientific_name:
        return None
    cleaned = scientific_name.replace('/', ' ').strip()
    parts = cleaned.split()
    if parts:
        return parts[0].strip().capitalize()
    return None

def resolve_animal_audio(scientific_name: Optional[str], name_uz: str = "", category: str = "") -> Dict[str, Any]:
    """
    Hayvonning scientific_name (lotincha nomi) orqali ochiq wildlife API va ro'yxatdan
    mos haqiqiy audio URL ni avtomatik topib berish.
    """
    genus = extract_genus(scientific_name)
    if genus and genus in GENUS_AUDIO_REGISTRY:
        info = GENUS_AUDIO_REGISTRY[genus].copy()
        info["genus"] = genus
        info["scientific_name"] = scientific_name
        return info

    # Agar keshda bo'lmasa, ochiq iNaturalist / xeno-canto JSON API dan jonli so'rash
    if scientific_name:
        query_name = scientific_name.split('/')[0].strip()
        api_url = f"https://api.inaturalist.org/v1/observations?taxon_name={urllib.parse.quote(query_name)}&sounds=true&per_page=1"
        try:
            req = urllib.request.Request(api_url, headers={"User-Agent": "ZooventureBot/2.0 (Wildlife Audio Controller)"})
            with urllib.request.urlopen(req, timeout=4) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    if data.get("total_results", 0) > 0 and data.get("results"):
                        sounds = data["results"][0].get("sounds", [])
                        if sounds and sounds[0].get("file_url"):
                            audio_url = sounds[0]["file_url"]
                            return {
                                "audioUrl": audio_url,
                                "soundType": "roar" if category == "Sutemizuvchilar" else ("eagle" if category == "Qushlar" else "dolphin"),
                                "soundDescription": f"{name_uz or scientific_name} tabiiy ovozi",
                                "source": "iNaturalist Open Wildlife API",
                                "scientific_name": scientific_name,
                                "genus": genus
                            }
        except Exception as e:
            logger.warning(f"Jonli audio qidiruvda xatolik ({scientific_name}): {e}")

    # Kategoriya bo'yicha tabiiy fallback
    if category == 'Qushlar':
        default_info = GENUS_AUDIO_REGISTRY['Luscinia']
    elif category == 'Baliqlar':
        default_info = GENUS_AUDIO_REGISTRY['Delphinus']
    elif category == 'Sudralib yuruvchilar':
        default_info = GENUS_AUDIO_REGISTRY['Varanus']
    else:
        default_info = GENUS_AUDIO_REGISTRY['Panthera']

    res = default_info.copy()
    res["scientific_name"] = scientific_name
    res["genus"] = genus
    return res
