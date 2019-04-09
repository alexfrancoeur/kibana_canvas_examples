#!/usr/bin/python
import json
import urllib2
import elasticsearch
import pprint
import time
import random
import datetime
import pytz
import uuid

try:
    es = elasticsearch.Elasticsearch(["localhost"],port=9200)
except:
    print "unable to es"

# random city data
city_file = open('cities.json')
location_data = json.load(city_file)
destination_location_data = [{"country": "US","name": "Ashburn","lat": "38.414989","lng": "-77.607361"},{"country": "US","name": "Los Angeles","lat": "34.052235","lng": "-118.243683"},{"country": "BR","name": "Sao Paulo","lat": "-23.550520","lng": "-46.633308"},{"country": "DE","name": "Frankfurt","lat": "50.110924","lng": "8.682127"},{"country": "JP","name": "Tokyo","lat": "35.689487","lng": "139.691711"}]

# fake suricata data
agent_hostname = ["suricata-tokyo", "suricata-saopaulo", "suricata-ashburn", "suricata-losangeles","suricata-frankfurt"]
agent_type = "filebeat"
agent_version = "7.0.0"
log_file_path = ["/var/log/bro/current/conn.log","/var/log/suricata/eve.json","/var/log/auth.log","/home/tsg/suricata-logs/logs/eve-result.json","/var/log/bro/current/dns.log","/var/log/bro/current/http.log","/var/log/bro/current/notice.log","/var/log/bro/current/ssl.log"]
destination_port = [80,22,445,23,59919,49905]
source_port = [443,80,8883,5223,3,123]
fileset_name = ["connection","eve","auth","dns","http","notice","ssl"]
message = ["Potential Corporate Privacy Violation","Generic Protocol Command Decode", "Potentially Bad Traffic", "A Network Trojan was detected", "Attempted Information Leak","Potential Corporate Privacy Violation"]
network_protocol = ["http","ssh","failed","tls","ntp","dns","tftp","ikev2","krb5"]
network_transport = ["tcp","udp","icmp","sctp"]
cloud_availability_zone = "projects/238712873821/zones/us-east1-b"
cloud_instance_name = "suricata-ems"
cloud_instance_id = "2982319812023902193"
cloud_provider = "gce"
cloud_machine_type = "projects/238712873821/machineTypes/n1-standard-1"
cloud_project = "elastic-beats"
input_type = "log"
service_type = "suricata"
host_hostname = ["suricata-tokyo", "suricata-saopaulo", "suricata-ashburn", "suricata-losangeles","suricata-frankfurt"]
host_os_codename = ["bionic","stretch"]
host_os_kernal = ["4.15.0-45-generic","4.14.50-v7+","4.9.0-8-amd64"]
host_os_family = "debian"
host_os_name = ["Ubuntu","Raspbian GNU/Linux","Debian GNU/Linux"]
host_os_version = ["18.04.2 LTS (Bionic Beaver)","9 (stretch)"]
host_os_platform = ["ubuntu","raspbian","debian"]
host_architecture = ["x86_64","armv7l"]
suricata_eve_event_type = ["flow","ssh","alert","dns","http","fileinfo","tftp","tls","ikev2"]
suricata_eve_alert_signature_id = [2402000,2260002,2018959,2001219,2210044,2500024,2011716,2008578,2010935,2210050]
suricata_eve_alert_signature = ["ET DROP Dshield Block Listed Source group 1","SURICATA Applayer Detect protocol only one direction","ET POLICY PE EXE or DLL Windows file download HTTP","ET SCAN Potential SSH Scan","SURICATA STREAM Packet with invalid timestamp","ET COMPROMISED Known Compromised or Hostile Host Traffic group 13","ET SCAN Sipvicious User-Agent Detected (friendly-scanner)","ET SCAN Sipvicious Scan","ET SCAN Suspicious inbound to MSSQL port 1433","SURICATA STREAM reassembly overlap with different data"]
suricata_eve_alert_category = ["Misc Attack","Generic Protocol Command Decode","Attempted Information Leak","Potential Corporate Privacy Violation","Potentially Bad Traffic","Not Suspicious Traffic","Decode of an RPC Query","Misc activity","A Network Trojan was detected","Detection of a Network Scan"]
suricata_eve_tls_not_before = [1543880167000,1494979200000,1520453015000,1548773880000,1548979200000]
suricata_eve_tls_not_after = [1638488167000,1526601599000,1527706380000,1556031480000,1558689900000]
suricata_eve_tls_fingerprint = ["15:9A:76:C5:AE:F4:90:15:79:E6:A4:99:96:C1:D6:A1:D9:3B:07:43","18:91:80:9B:75:1F:19:27:BA:09:F8:3F:9F:3D:0E:A7:56:F4:ED:B7","E8:20:7A:27:8C:BE:D4:D9:7F:44:32:89:E7:6B:13:DD:CE:58:50:F6","58:3E:A1:CD:3F:46:D5:F9:4B:51:5D:55:8F:90:97:1B:65:6D:51:C3","D0:E6:B8:EF:CF:34:D1:4E:D1:C7:5F:B9:DE:21:17:96:82:67:2B:EA","0A:39:D8:A9:C5:8A:46:C8:88:6D:DB:3C:2E:41:70:B2:8E:F6:D6:5B","62:84:F1:44:40:7C:FC:BF:E3:07:9C:59:E2:75:3A:1E:10:0C:29:86","DE:9E:8E:5B:C0:D9:AD:A9:E8:C4:68:F4:76:DD:57:75:12:90:EB:D6","79:1A:83:83:21:20:F6:6D:9D:1E:77:5F:ED:89:16:FC:8E:A0:E0:C3","6A:0F:88:D6:2D:7A:CC:AF:24:01:B7:7A:7A:68:9C:9F:FD:76:C4:BE"]
suricata_eve_tls_subject = ["CN=instance","OU=Domain Control Validated, OU=PositiveSSL, CN=api.ipify.org","C=US, ST=New York, L=Brooklyn, O=Google Inc, CN=*.google.com","C=US, ST=California, L=Los Gatos, O=Netflix, Inc., OU=Content Delivery, CN=*.1.oca.nflxvideo.net","C=US, ST=California, L=Mountain View, O=Google LLC, CN=edgestatic.com","C=US, ST=California, L=Los Gatos, O=Netflix, Inc., OU=Content Delivery, CN=*.1.nflxso.net","C=US, ST=New York, L=Brooklyn, O=Google LLC, CN=www.google.com","C=KR, ST=Kyong-gi, O=Samsung Electronics, OU=Samsung Hubsite, CN=*.samsungcloudsolution.net","C=US, ST=CA, L=Menlo Park, O=Facebook, Inc., CN=*.facebook.com","C=US, ST=Illinois, L=Lisle, O=Kantar Operations, OU=Information Technology, CN=*.insightexpressai.com"]
suricata_eve_tls_issuer =["CN=Elastic Fakelogs","C=GB, ST=Greater Manchester, L=Salford, O=COMODO CA Limited, CN=COMODO RSA Domain Validation Secure Server CA","C=US, O=Google Trust Services, CN=Google Internet Authority G3","C=US, O=DigiCert Inc, CN=DigiCert SHA2 Secure Server CA","CN=Samsung Hubsite CA/O=Samsung Electronics/C=KR/ST=Kyong-gi/L=Suwon","C=US, O=DigiCert Inc, OU=www.digicert.com, CN=DigiCert SHA2 High Assurance Server CA","C=US, ST=New York, L=Brooklyn, O=COMODO CA Limited, CN=COMODO RSA Organization Validation Secure Server CA","C=KR, ST=Gyeonggi do, L=Suwon, O=SAMSUNG ELECTRONICS CO., LTD, CN=*.push.samsungosp.com/emailAddress=admin@push.samsungosp.com","C=US, O=DigiCert Inc, OU=www.digicert.com, CN=DigiCert SHA2 Extended Validation Server CA","C=US, O=Let's Encrypt, CN=Let's Encrypt Authority X3"]
suricata_eve_tls_serial = ["15:9A:76:C5:AE:F4:90:15:79:E6:A4:99:96:C1:D6:A1:D9:3B:07:43","18:91:80:9B:75:1F:19:27:BA:09:F8:3F:9F:3D:0E:A7:56:F4:ED:B7","E8:20:7A:27:8C:BE:D4:D9:7F:44:32:89:E7:6B:13:DD:CE:58:50:F6","58:3E:A1:CD:3F:46:D5:F9:4B:51:5D:55:8F:90:97:1B:65:6D:51:C3","D0:E6:B8:EF:CF:34:D1:4E:D1:C7:5F:B9:DE:21:17:96:82:67:2B:EA","0A:39:D8:A9:C5:8A:46:C8:88:6D:DB:3C:2E:41:70:B2:8E:F6:D6:5B","62:84:F1:44:40:7C:FC:BF:E3:07:9C:59:E2:75:3A:1E:10:0C:29:86","DE:9E:8E:5B:C0:D9:AD:A9:E8:C4:68:F4:76:DD:57:75:12:90:EB:D6","79:1A:83:83:21:20:F6:6D:9D:1E:77:5F:ED:89:16:FC:8E:A0:E0:C3","6A:0F:88:D6:2D:7A:CC:AF:24:01:B7:7A:7A:68:9C:9F:FD:76:C4:BE"]
suricata_eve_tls_version = "TLS 1.2"
suricata_eve_tls_sni = "api.ipify.org"
event_kind = "event"
event_module = "suricata"
event_dataset = "suricata.eve"
event_outcome = "allowed"

# make some filebeat docs
while True:
    try:
        src = random.choice(location_data)
        dest = random.choice(destination_location_data)
        now = pytz.utc.localize(datetime.datetime.utcnow())
        start_time = now + datetime.timedelta(days=random.randrange(-10,-2)) + datetime.timedelta(hours=random.randrange(1,24))+ datetime.timedelta(minutes=random.randrange(1,60))
        new_body = {
            "agent": {
              "hostname": random.choice(agent_hostname),
              "id": str(uuid.uuid4()),
              "ephemeral_id": str(uuid.uuid4()),
              "type": agent_type,
              "version": agent_version
            },
            "log": {
              "file": {
                "path": random.choice(log_file_path)
              },
              "offset": random.randrange(300000000,400000000)
            },
            "destination": {
              "geo": {
                "city_name": dest["name"],
                "country_iso_code": dest["country"],
                "location": {
                  "lon": float(dest["lng"]),
                  "lat": float(dest["lat"])
                }
              },
              "port": random.choice(destination_port),
              "bytes": random.randrange(10000,100000),
              "ip": "{0}.{1}.{2}.{3}".format(random.randrange(1,255),random.randrange(1,255),random.randrange(1,255),random.randrange(1,255)),
              "packets": random.randrange(10,50)
            },
            "source": {
              "geo": {
                "city_name": src["name"],
                "country_iso_code": src["country"],
                "location": {
                  "lon": float(src["lng"]),
                  "lat": float(src["lat"])
                }
              },
              "port": random.choice(source_port),
              "bytes": random.randrange(10000,100000),
              "ip": "{0}.{1}.{2}.{3}".format(random.randrange(1,255),random.randrange(1,255),random.randrange(1,255),random.randrange(1,255)),
              "packets": random.randrange(10,50)
            },
            "fileset": {
              "name": random.choice(fileset_name)
            },
            "message": random.choice(message),
            "tags": [
              "suricata"
            ],
            "network": {
              "protocol": random.choice(network_protocol),
              "bytes": random.randrange(10000,100000),
              "transport": random.choice(network_protocol),
              "packets": random.randrange(10,50)
            },
            "cloud": {
              "availability_zone": cloud_availability_zone,
              "instance": {
                "name": cloud_instance_name,
                "id": cloud_instance_id
              },
              "provider": cloud_provider,
              "machine": {
                "type": cloud_machine_type
              },
              "project": {
                "id": cloud_project
              }
            },
            "input": {
              "type": input_type
            },
            "@timestamp": datetime.datetime.strftime(now,'%Y-%m-%dT%H:%M:%S.%fZ'),
            "ecs": {
              "version": "1.0.0"
            },
            "service": {
              "type": service_type
            },
            "host": {
              "hostname": random.choice(host_hostname),
              "os": {
                "kernel": random.choice(host_os_kernal),
                "codename": random.choice(host_os_codename),
                "name": random.choice(host_os_name),
                "family": host_os_family,
                "version": random.choice(host_os_version),
                "platform": random.choice(host_os_platform)
              },
              "containerized": "false",
              "name": "suricata-ems",
              "id": str(uuid.uuid4().hex),
              "architecture": random.choice(host_architecture)
            },
            "suricata": {
              "eve": {
                "pcap_cnt": random.randrange(2000000,3000000),
                "tx_id": random.randrange(1,3),
                "event_type": random.choice(suricata_eve_event_type),
                "alert": {
                  "rev": random.randrange(1,3),
                  "signature_id": random.choice(suricata_eve_alert_signature_id),
                  "gid": 1,
                  "signature": random.choice(suricata_eve_alert_signature),
                  "category": random.choice(suricata_eve_alert_category)
                },
                "flow_id": random.randrange(2000000000000000,3000000000000000),
                "tls": {
                  "notbefore": random.choice(suricata_eve_tls_not_before),
                  "serial": random.choice(suricata_eve_tls_serial),
                  "subject": random.choice(suricata_eve_tls_subject),
                  "issuerdn": random.choice(suricata_eve_tls_issuer),
                  "notafter": random.choice(suricata_eve_tls_not_after),
                  "fingerprint": random.choice(suricata_eve_tls_fingerprint),
                  "version": suricata_eve_tls_version,
                  "sni": suricata_eve_tls_sni
                },
                "flow": {}
              }
            },
            "event": {
              "severity": random.randrange(1,5),
              "kind": event_kind,
              "module": event_module,
              "start": datetime.datetime.strftime(start_time,'%Y-%m-%dT%H:%M:%S.%fZ'),
              "end": datetime.datetime.strftime(now,'%Y-%m-%dT%H:%M:%S.%fZ'),
              "duration": (now - start_time).total_seconds(),
              "dataset": event_dataset,
              "outcome": event_outcome
            },
            "request_path": {"type":"linestring","coordinates":[[float(src["lng"]),float(src["lat"])],[float(dest["lng"]),float(dest["lat"])]]}
          }

        try:
            res = es.index(index="filebeat-fakelogs", doc_type="_doc", body=new_body)
            pprint.pprint("{0}:{1}".format(new_body["@timestamp"],res['result']))
        except Exception as e:
            print e
    except Exception as e:
        print e
    print "sleeping for 5 sec"
    time.sleep(5)
