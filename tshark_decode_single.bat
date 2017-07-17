cd %~dp1
tshark -R "http.request or http.response"   -2 -T fields -E separator="|"   -e http.host -e http.request.uri  -e http.referer   -e http.location  -r %~1 > traffic_dump.txt 2>>&1