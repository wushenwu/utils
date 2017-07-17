#-*- coding: UTF-8 -*-
import sys
import os
import re

IPReg = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"

#http://data.iana.org/TLD/tlds-alpha-by-domain.txt
g_domains = ["AAA", "AARP", "ABB", "ABBOTT", "ABOGADO", "AC", "ACADEMY", "ACCENTURE", "ACCOUNTANT", "ACCOUNTANTS", "ACO", "ACTIVE", "ACTOR", "AD", "ADS", "ADULT", "AE", "AEG", "AERO", "AF", "AFL", "AG", "AGENCY", "AI", "AIG", "AIRFORCE", "AIRTEL", "AL", "ALLFINANZ", "ALSACE", "AM", "AMICA", "AMSTERDAM", "ANALYTICS", "ANDROID", "AO", "APARTMENTS", "APP", "APPLE", "AQ", "AQUARELLE", "AR", "ARAMCO", "ARCHI", "ARMY", "ARPA", "ARTE", "AS", "ASIA", "ASSOCIATES", "AT", "ATTORNEY", "AU", "AUCTION", "AUDI", "AUDIO", "AUTHOR", "AUTO", "AUTOS", "AW", "AX", "AXA", "AZ", "AZURE", "BA", "BAIDU", "BAND", "BANK", "BAR", "BARCELONA", "BARCLAYCARD", "BARCLAYS", "BARGAINS", "BAUHAUS", "BAYERN", "BB", "BBC", "BBVA", "BCN", "BD", "BE", "BEATS", "BEER", "BENTLEY", "BERLIN", "BEST", "BET", "BF", "BG", "BH", "BHARTI", "BI", "BIBLE", "BID", "BIKE", "BING", "BINGO", "BIO", "BIZ", "BJ", "BLACK", "BLACKFRIDAY", "BLOOMBERG", "BLUE", "BM", "BMS", "BMW", "BN", "BNL", "BNPPARIBAS", "BO", "BOATS", "BOEHRINGER", "BOM", "BOND", "BOO", "BOOK", "BOOTS", "BOSCH", "BOSTIK", "BOT", "BOUTIQUE", "BR", "BRADESCO", "BRIDGESTONE", "BROADWAY", "BROKER", "BROTHER", "BRUSSELS", "BS", "BT", "BUDAPEST", "BUGATTI", "BUILD", "BUILDERS", "BUSINESS", "BUY", "BUZZ", "BV", "BW", "BY", "BZ", "BZH", "CA", "CAB", "CAFE", "CAL", "CALL", "CAMERA", "CAMP", "CANCERRESEARCH", "CANON", "CAPETOWN", "CAPITAL", "CAR", "CARAVAN", "CARDS", "CARE", "CAREER", "CAREERS", "CARS", "CARTIER", "CASA", "CASH", "CASINO", "CAT", "CATERING", "CBA", "CBN", "CC", "CD", "CEB", "CENTER", "CEO", "CERN", "CF", "CFA", "CFD", "CG", "CH", "CHANEL", "CHANNEL", "CHAT", "CHEAP", "CHLOE", "CHRISTMAS", "CHROME", "CHURCH", "CI", "CIPRIANI", "CIRCLE", "CISCO", "CITIC", "CITY", "CITYEATS", "CK", "CL", "CLAIMS", "CLEANING", "CLICK", "CLINIC", "CLINIQUE", "CLOTHING", "CLOUD", "CLUB", "CLUBMED", "CM", "CN", "CO", "COACH", "CODES", "COFFEE", "COLLEGE", "COLOGNE", "COM", "COMMBANK", "COMMUNITY", "COMPANY", "COMPARE", "COMPUTER", "COMSEC", "CONDOS", "CONSTRUCTION", "CONSULTING", "CONTACT", "CONTRACTORS", "COOKING", "COOL", "COOP", "CORSICA", "COUNTRY", "COUPONS", "COURSES", "CR", "CREDIT", "CREDITCARD", "CREDITUNION", "CRICKET", "CROWN", "CRS", "CRUISES", "CSC", "CU", "CUISINELLA", "CV", "CW", "CX", "CY", "CYMRU", "CYOU", "CZ", "DABUR", "DAD", "DANCE", "DATE", "DATING", "DATSUN", "DAY", "DCLK", "DE", "DEALER", "DEALS", "DEGREE", "DELIVERY", "DELL", "DELTA", "DEMOCRAT", "DENTAL", "DENTIST", "DESI", "DESIGN", "DEV", "DIAMONDS", "DIET", "DIGITAL", "DIRECT", "DIRECTORY", "DISCOUNT", "DJ", "DK", "DM", "DNP", "DO", "DOCS", "DOG", "DOHA", "DOMAINS", "DOOSAN", "DOWNLOAD", "DRIVE", "DUBAI", "DURBAN", "DVAG", "DZ", "EARTH", "EAT", "EC", "EDU", "EDUCATION", "EE", "EG", "EMAIL", "EMERCK", "ENERGY", "ENGINEER", "ENGINEERING", "ENTERPRISES", "EPSON", "EQUIPMENT", "ER", "ERNI", "ES", "ESQ", "ESTATE", "ET", "EU", "EUROVISION", "EUS", "EVENTS", "EVERBANK", "EXCHANGE", "EXPERT", "EXPOSED", "EXPRESS", "FAGE", "FAIL", "FAIRWINDS", "FAITH", "FAMILY", "FAN", "FANS", "FARM", "FASHION", "FAST", "FEEDBACK", "FERRERO", "FI", "FILM", "FINAL", "FINANCE", "FINANCIAL", "FIRESTONE", "FIRMDALE", "FISH", "FISHING", "FIT", "FITNESS", "FJ", "FK", "FLIGHTS", "FLORIST", "FLOWERS", "FLSMIDTH", "FLY", "FM", "FO", "FOO", "FOOTBALL", "FORD", "FOREX", "FORSALE", "FORUM", "FOUNDATION", "FOX", "FR", "FRESENIUS", "FRL", "FROGANS", "FUND", "FURNITURE", "FUTBOL", "FYI", "GA", "GAL", "GALLERY", "GAME", "GARDEN", "GB", "GBIZ", "GD", "GDN", "GE", "GEA", "GENT", "GENTING", "GF", "GG", "GGEE", "GH", "GI", "GIFT", "GIFTS", "GIVES", "GIVING", "GL", "GLASS", "GLE", "GLOBAL", "GLOBO", "GM", "GMAIL", "GMO", "GMX", "GN", "GOLD", "GOLDPOINT", "GOLF", "GOO", "GOOG", "GOOGLE", "GOP", "GOT", "GOV", "GP", "GQ", "GR", "GRAINGER", "GRAPHICS", "GRATIS", "GREEN", "GRIPE", "GROUP", "GS", "GT", "GU", "GUCCI", "GUGE", "GUIDE", "GUITARS", "GURU", "GW", "GY", "HAMBURG", "HANGOUT", "HAUS", "HEALTHCARE", "HELP", "HERE", "HERMES", "HIPHOP", "HITACHI", "HIV", "HK", "HM", "HN", "HOCKEY", "HOLDINGS", "HOLIDAY", "HOMEDEPOT", "HOMES", "HONDA", "HORSE", "HOST", "HOSTING", "HOTELES", "HOTMAIL", "HOUSE", "HOW", "HR", "HSBC", "HT", "HU", "HYUNDAI", "IBM", "ICBC", "ICE", "ICU", "ID", "IE", "IFM", "IINET", "IL", "IM", "IMMO", "IMMOBILIEN", "IN", "INDUSTRIES", "INFINITI", "INFO", "ING", "INK", "INSTITUTE", "INSURANCE", "INSURE", "INT", "INTERNATIONAL", "INVESTMENTS", "IO", "IPIRANGA", "IQ", "IR", "IRISH", "IS", "ISELECT", "IST", "ISTANBUL", "IT", "ITAU", "IWC", "JAGUAR", "JAVA", "JCB", "JE", "JETZT", "JEWELRY", "JLC", "JLL", "JM", "JMP", "JO", "JOBS", "JOBURG", "JOT", "JOY", "JP", "JPRS", "JUEGOS", "KAUFEN", "KDDI", "KE", "KFH", "KG", "KH", "KI", "KIA", "KIM", "KINDER", "KITCHEN", "KIWI", "KM", "KN", "KOELN", "KOMATSU", "KP", "KPN", "KR", "KRD", "KRED", "KW", "KY", "KYOTO", "KZ", "LA", "LACAIXA", "LAMBORGHINI", "LAMER", "LANCASTER", "LAND", "LANDROVER", "LASALLE", "LAT", "LATROBE", "LAW", "LAWYER", "LB", "LC", "LDS", "LEASE", "LECLERC", "LEGAL", "LEXUS", "LGBT", "LI", "LIAISON", "LIDL", "LIFE", "LIFESTYLE", "LIGHTING", "LIKE", "LIMITED", "LIMO", "LINCOLN", "LINDE", "LINK", "LIVE", "LIVING", "LIXIL", "LK", "LOAN", "LOANS", "LOL", "LONDON", "LOTTE", "LOTTO", "LOVE", "LR", "LS", "LT", "LTD", "LTDA", "LU", "LUPIN", "LUXE", "LUXURY", "LV", "LY", "MA", "MADRID", "MAIF", "MAISON", "MAKEUP", "MAN", "MANAGEMENT", "MANGO", "MARKET", "MARKETING", "MARKETS", "MARRIOTT", "MBA", "MC", "MD", "ME", "MED", "MEDIA", "MEET", "MELBOURNE", "MEME", "MEMORIAL", "MEN", "MENU", "MEO", "MG", "MH", "MIAMI", "MICROSOFT", "MIL", "MINI", "MK", "ML", "MM", "MMA", "MN", "MO", "MOBI", "MOBILY", "MODA", "MOE", "MOI", "MOM", "MONASH", "MONEY", "MONTBLANC", "MORMON", "MORTGAGE", "MOSCOW", "MOTORCYCLES", "MOV", "MOVIE", "MOVISTAR", "MP", "MQ", "MR", "MS", "MT", "MTN", "MTPC", "MTR", "MU", "MUSEUM", "MUTUELLE", "MV", "MW", "MX", "MY", "MZ", "NA", "NADEX", "NAGOYA", "NAME", "NAVY", "NC", "NE", "NEC", "NET", "NETBANK", "NETWORK", "NEUSTAR", "NEW", "NEWS", "NEXUS", "NF", "NG", "NGO", "NHK", "NI", "NICO", "NINJA", "NISSAN", "NL", "NO", "NOKIA", "NORTON", "NOWRUZ", "NP", "NR", "NRA", "NRW", "NTT", "NU", "NYC", "NZ", "OBI", "OFFICE", "OKINAWA", "OM", "OMEGA", "ONE", "ONG", "ONL", "ONLINE", "OOO", "ORACLE", "ORANGE", "ORG", "ORGANIC", "ORIGINS", "OSAKA", "OTSUKA", "OVH", "PA", "PAGE", "PANERAI", "PARIS", "PARS", "PARTNERS", "PARTS", "PARTY", "PE", "PET", "PF", "PG", "PH", "PHARMACY", "PHILIPS", "PHOTO", "PHOTOGRAPHY", "PHOTOS", "PHYSIO", "PIAGET", "PICS", "PICTET", "PICTURES", "PID", "PIN", "PING", "PINK", "PIZZA", "PK", "PL", "PLACE", "PLAY", "PLAYSTATION", "PLUMBING", "PLUS", "PM", "PN", "POHL", "POKER", "PORN", "POST", "PR", "PRAXI", "PRESS", "PRO", "PROD", "PRODUCTIONS", "PROF", "PROMO", "PROPERTIES", "PROPERTY", "PROTECTION", "PS", "PT", "PUB", "PW", "PY", "QA", "QPON", "QUEBEC", "RACING", "RE", "READ", "REALTOR", "REALTY", "RECIPES", "RED", "REDSTONE", "REDUMBRELLA", "REHAB", "REISE", "REISEN", "REIT", "REN", "RENT", "RENTALS", "REPAIR", "REPORT", "REPUBLICAN", "REST", "RESTAURANT", "REVIEW", "REVIEWS", "REXROTH", "RICH", "RICOH", "RIO", "RIP", "RO", "ROCHER", "ROCKS", "RODEO", "ROOM", "RS", "RSVP", "RU", "RUHR", "RUN", "RW", "RWE", "RYUKYU", "SA", "SAARLAND", "SAFE", "SAFETY", "SAKURA", "SALE", "SALON", "SAMSUNG", "SANDVIK", "SANDVIKCOROMANT", "SANOFI", "SAP", "SAPO", "SARL", "SAS", "SAXO", "SB", "SBS", "SC", "SCA", "SCB", "SCHAEFFLER", "SCHMIDT", "SCHOLARSHIPS", "SCHOOL", "SCHULE", "SCHWARZ", "SCIENCE", "SCOR", "SCOT", "SD", "SE", "SEAT", "SECURITY", "SEEK", "SELECT", "SENER", "SERVICES", "SEVEN", "SEW", "SEX", "SEXY", "SFR", "SG", "SH", "SHARP", "SHELL", "SHIA", "SHIKSHA", "SHOES", "SHOW", "SHRIRAM", "SI", "SINGLES", "SITE", "SJ", "SK", "SKI", "SKIN", "SKY", "SKYPE", "SL", "SM", "SMILE", "SN", "SNCF", "SO", "SOCCER", "SOCIAL", "SOFTWARE", "SOHU", "SOLAR", "SOLUTIONS", "SONY", "SOY", "SPACE", "SPIEGEL", "SPREADBETTING", "SR", "SRL", "ST", "STADA", "STAR", "STARHUB", "STATEFARM", "STATOIL", "STC", "STCGROUP", "STOCKHOLM", "STORAGE", "STUDIO", "STUDY", "STYLE", "SU", "SUCKS", "SUPPLIES", "SUPPLY", "SUPPORT", "SURF", "SURGERY", "SUZUKI", "SV", "SWATCH", "SWISS", "SX", "SY", "SYDNEY", "SYMANTEC", "SYSTEMS", "SZ", "TAB", "TAIPEI", "TATAMOTORS", "TATAR", "TATTOO", "TAX", "TAXI", "TC", "TCI", "TD", "TEAM", "TECH", "TECHNOLOGY", "TEL", "TELEFONICA", "TEMASEK", "TENNIS", "TF", "TG", "TH", "THD", "THEATER", "THEATRE", "TICKETS", "TIENDA", "TIPS", "TIRES", "TIROL", "TJ", "TK", "TL", "TM", "TN", "TO", "TODAY", "TOKYO", "TOOLS", "TOP", "TORAY", "TOSHIBA", "TOURS", "TOWN", "TOYOTA", "TOYS", "TR", "TRADE", "TRADING", "TRAINING", "TRAVEL", "TRAVELERS", "TRAVELERSINSURANCE", "TRUST", "TRV", "TT", "TUBE", "TUI", "TUSHU", "TV", "TW", "TZ", "UA", "UBS", "UG", "UK", "UNIVERSITY", "UNO", "UOL", "US", "UY", "UZ", "VA", "VACATIONS", "VANA", "VC", "VE", "VEGAS", "VENTURES", "VERISIGN", "VERSICHERUNG", "VET", "VG", "VI", "VIAJES", "VIDEO", "VILLAS", "VIN", "VIP", "VIRGIN", "VISION", "VISTA", "VISTAPRINT", "VIVA", "VLAANDEREN", "VN", "VODKA", "VOLKSWAGEN", "VOTE", "VOTING", "VOTO", "VOYAGE", "VU", "WALES", "WALTER", "WANG", "WANGGOU", "WATCH", "WATCHES", "WEATHER", "WEBCAM", "WEBER", "WEBSITE", "WED", "WEDDING", "WEIR", "WF", "WHOSWHO", "WIEN", "WIKI", "WILLIAMHILL", "WIN", "WINDOWS", "WINE", "WME", "WORK", "WORKS", "WORLD", "WS", "WTC", "WTF", "XBOX", "XEROX", "XIN", "XN--11B4C3D", "XN--1QQW23A", "XN--30RR7Y", "XN--3BST00M", "XN--3DS443G", "XN--3E0B707E", "XN--3PXU8K", "XN--42C2D9A", "XN--45BRJ9C", "XN--45Q11C", "XN--4GBRIM", "XN--55QW42G", "XN--55QX5D", "XN--6FRZ82G", "XN--6QQ986B3XL", "XN--80ADXHKS", "XN--80AO21A", "XN--80ASEHDB", "XN--80ASWG", "XN--90A3AC", "XN--90AIS", "XN--9DBQ2A", "XN--9ET52U", "XN--B4W605FERD", "XN--C1AVG", "XN--C2BR7G", "XN--CG4BKI", "XN--CLCHC0EA0B2G2A9GCD", "XN--CZR694B", "XN--CZRS0T", "XN--CZRU2D", "XN--D1ACJ3B", "XN--D1ALF", "XN--ECKVDTC9D", "XN--EFVY88H", "XN--ESTV75G", "XN--FHBEI", "XN--FIQ228C5HS", "XN--FIQ64B", "XN--FIQS8S", "XN--FIQZ9S", "XN--FJQ720A", "XN--FLW351E", "XN--FPCRJ9C3D", "XN--FZC2C9E2C", "XN--GECRJ9C", "XN--H2BRJ9C", "XN--HXT814E", "XN--I1B6B1A6A2E", "XN--IMR513N", "XN--IO0A7I", "XN--J1AEF", "XN--J1AMH", "XN--J6W193G", "XN--JLQ61U9W7B", "XN--KCRX77D1X4A", "XN--KPRW13D", "XN--KPRY57D", "XN--KPU716F", "XN--KPUT3I", "XN--L1ACC", "XN--LGBBAT1AD8J", "XN--MGB9AWBF", "XN--MGBA3A3EJT", "XN--MGBA3A4F16A", "XN--MGBAAM7A8H", "XN--MGBAB2BD", "XN--MGBAYH7GPA", "XN--MGBB9FBPOB", "XN--MGBBH1A71E", "XN--MGBC0A9AZCG", "XN--MGBERP4A5D4AR", "XN--MGBPL2FH", "XN--MGBT3DHD", "XN--MGBTX2B", "XN--MGBX4CD0AB", "XN--MK1BU44C", "XN--MXTQ1M", "XN--NGBC5AZD", "XN--NGBE9E0A", "XN--NODE", "XN--NQV7F", "XN--NQV7FS00EMA", "XN--NYQY26A", "XN--O3CW4H", "XN--OGBPF8FL", "XN--P1ACF", "XN--P1AI", "XN--PBT977C", "XN--PGBS0DH", "XN--PSSY2U", "XN--Q9JYB4C", "XN--QCKA1PMC", "XN--QXAM", "XN--RHQV96G", "XN--S9BRJ9C", "XN--SES554G", "XN--T60B56A", "XN--TCKWE", "XN--UNUP4Y", "XN--VERMGENSBERATER-CTB", "XN--VERMGENSBERATUNG-PWB", "XN--VHQUV", "XN--VUQ861B", "XN--WGBH1C", "XN--WGBL6A", "XN--XHQ521B", "XN--XKC2AL3HYE2A", "XN--XKC2DL3A5EE0H", "XN--Y9A3AQ", "XN--YFRO4I67O", "XN--YGBI2AMMX", "XN--ZFR164B", "XPERIA", "XXX", "XYZ", "YACHTS", "YAMAXUN", "YANDEX", "YE", "YODOBASHI", "YOGA", "YOKOHAMA", "YOUTUBE", "YT", "ZA", "ZARA", "ZERO", "ZIP", "ZM", "ZONE", "ZUERICH", "ZW"]

def RemovePort(domain):
    #60t.mintongh.com:9090
    index = domain.find(':')
    if index != -1:
        domain = domain[ :index]
    return domain
    
def IsInDomain(part):
    '''
    '''
    part = part.upper()
    if part not in g_domains:
        return False
    return True
    
def IsValidDomain(domain):
    domain = RemovePort(domain)
    
    #211.84.64.201/file.php?name=2_com.baidu.superservice_1.6.2.apk&path=/c/0/c043e4509d73df7c223aa1bef8c4f202.apk&cache_url=baidu.com/2_com.baidu.superservice_1.6.2.apk
    if domain.find('?') != -1 or domain.find('=') != -1 or domain.find('&') != -1:
        return False
       
    items = domain.split('.')
    root = items[-1].upper()
    if 'ZIP' == root:
        return False
    
    if root not in g_domains:
        return False
        
    if 'com' == items[0]: 
        #['update.lieyou.com', 'com.aipai.android', 'multi_domain']
        #['update.coolyun.com', 'com.icoolme.android.weather', 'multi_domain']
        #['sj.img4399.com', 'com.hytc.sg', 'multi_domain']
        #['sign.92.net', 'com.zxly.market', 'multi_domain']
        return False
        
    for item in items:
        #/movie/.upload/
        if 0 == len(item):
            return False
    
    return True
       
def IsValidIp(ip):
    ip = RemovePort(ip)
        
    if not re.match(IPReg, ip):
        return False
        
    items = ip.split('.')
    if '0' == items[-1]:
        #112.5.183.237/1Q2W3E4R5T6Y7U8I9O0P1Z2X3C4V5B/cdn7.ops.baidu.com/new-repackonline/baidubrowser/AndroidPhone/6.3.13.0/1/1014392k/20151125132429/baidubrowser_AndroidPhone_6-3-13-0_1014392k.apk?response-content-disposition=attachment;filename=baidubrowser_AndroidPhone_1014392k.apk&response-content-type=application/vnd.android.package-archive&request_id=1452764098_7796330253&type=static
        #==>6.3.13.0/1/1014392k/20151125132429/baidubrowser_AndroidPhone_6-3-13-0_1014392k.apk?response-content-disposition=attachment;filename=baidubrowser_AndroidPhone_1014392k.apk&response-content-type=application/vnd.android.package-archive&request_id=1452764098_7796330253&type=static
        return False
        
    if '10' == items[0]:
        #10.0.28.2/qq.com/offline/100/142/354/20160113/comp_bsdiff_35803.zip
        #10.0.42.124/data3/zip/f58426010d2dfcffc86fd1d94c8bea28/comp_bsdiff_34384.zip
        return False
    
    # need to do more check
    # 112.17.13.201/files/3092000004AD6D23/shuocdn.108sq.cn/frontEnd/widget/integral_shop/3.0.0.4/integral_shop.zip
    # 10.200.0.3:8084/C/3774FCD95DB93101CCB4B910ADC33FA3F586BACB/080AB19DFCDD2DD5CBD056A092C19A6C96316DFE/txkj_url/cdn2.ops.baidu.com/new-repackonline/appsearch/AndroidPhone/1.0.37.193/1/1014281f/20151127161528/appsearch_AndroidPhone_1-0-37-193_1014281f.apk
        
    #these used for URLCheck to be more accurate
    '''
    if 1 == len(items[0]):
        print 'Invalid Ip ', ip
        return False
    '''
    
    return True
    
def URLCheck(url):
    '''
    从后向前，找到第一个符合格式的域名或者ip
    '''
    items = url.split('/')[ :-1] #exclude the last file part
    
    #case for startswith domain
    items[0] = RemovePort(items[0])
    if not re.match(IPReg, items[0]):
        return url
    
    for item in items[::-1]:  # in reverse order
        if -1 == item.find('.'):
            continue
            
        #10.102.3.20/update/files/31710000007F3D77/down.myapp.com/myapp/smart_ajax/com.tencent.android.qqdownloader/991310_22331408_1451062634607.apk
        #10.236.6.15/downloadw.inner.bbk.com/sms/upapk/0/com.bbk.appstore/20151009151923/com.bbk.appstore.apk
        if IsValidDomain(item):
            return url[url.find(item):]
        
        #
        #10.200.0.3:8084/C/3774FCD95DB93101CCB4B910ADC33FA3F586BACB/080AB19DFCDD2DD5CBD056A092C19A6C96316DFE/txkj_url/cdn2.ops.baidu.com/new-repackonline/appsearch/AndroidPhone/1.0.37.193/1/1014281f/20151127161528/appsearch_AndroidPhone_1-0-37-193_1014281f.apk
        if IsValidIp(item):
            return url[url.find(item):]
        
    return url

def URLCheck_Normal(url):
    '''
    针对以ip开头的url，自前向后，找到第一个domain；
    '''
    items = url.split('/')[ :-1]
    
    #case for startswith domain        
    items[0] = RemovePort(items[0])
    
    if not re.match(IPReg, items[0]):
        return url
        
    #found the first domain
    lastip = ''
    for item in items:
        if -1 == item.find('.'):
            continue
        
        if IsValidDomain(item):
            return url[url.find(item):]
            
        #used to know the last ip, for case without domain
        if IsValidIp(item):
            lastip = item
    
    #if domain not found, 
    return url[url.find(lastip):]
    
def URLCheck_Mix(url):
    '''
    优先寻找最后的domain
    当domain均不存在时，寻找最后的ip
    '''
    items = url.split('/')[:-1]
    
    lastip = ''
    l_domains = []
    for item in items:
        if -1 == item.find('.'):
            continue
        
        if IsValidDomain(item):
            l_domains.append(item)
        elif IsValidIp(item):
            lastip = item
    
    if len(l_domains) != 0:
        return url[url.find(l_domains[-1]):]
    else:
        return url[url.find(lastip):]
        
g_l_domain = []
def Filter(url):
    '''
    used for test
    '''
    items = url.split('/')[:-1]
    
    global g_l_domain
    domain_cnt = 0
    
    l_domain_ip = []
    for item in items:
        if -1 == item.find('.'):
            continue
        
        if IsValidDomain(item):
            l_domain_ip.append(item)
            domain_cnt += 1
        if IsValidIp(item):
            l_domain_ip.append(item)
    
    if domain_cnt > 1:
            l_domain_ip.append('multi_domain')
            
    if l_domain_ip not in g_l_domain:
        g_l_domain.append(l_domain_ip)    
        return  str(len(l_domain_ip)) + '\t' + str(l_domain_ip) + '\n\n'   
    return '\n'
    
def main():
    fname = sys.argv[1]
    fr = open(fname)
    fw = open(fname + '_check.txt', 'w')
    
    #skip one line
    fr.readline()
    for url in fr.readlines():
        ret = URLCheck_Mix(url)
        fw.write(url)
        if ret != url:
            fw.write('\t==>%s'%ret)
        '''
        filter = Filter(url)
        fw.write(url)
        if filter.find('multi_domain') != -1:
            fw.write(filter)
        
        fw.write(url)
        ret1 = URLCheck(url)
        ret2 = URLCheck_Normal(url)
        fw.write('\t==>' + ret1)
        fw.write('\t==>' + ret2)
        if ret1 != ret2 and -1 == ret1.find('wdjcdn.com'):
            fw.write('\t=====> Not Same\n')
        '''
        
    fw.close()
    fr.close()     
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print 'Usage: URL_Check.py url.txt'
        exit(-1)
    main()