#!/usr/local/bin/python3
# -*- coding:UTF-8 -*-

import sys
import json
import pytz
import datetime
import time
import logging
from conversant_auth import HttpUtil
# from fastly_models import DataContainer, DataLine
# from database import DB
# from utils import timestamp
# from five_to_one import divide

logging.basicConfig(
    format="%(asctime)s;%(levelname)s;%(message)s",
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

key_id = "Pv7k3o2v5K7tghm8"
key_secret = "M6yI30F54935B8LqMpR9o7p296T4s24j"
source = "conversant-cloud"
single_timeout = 60
data_delay = 1*3600

uri = "https://cdn-api.swiftfederation.com"
uri_total_flux = "/v1.1/report/volume"
uri_hit_flux = "/v1.0/report/hit_volume"
uri_request_hit = "/v1.0/report/hit_request_number"

def get_pull_interval():
    if len(sys.argv) == 3:
        start_time = timestamp(sys.argv[1], "%Y%m%d%H%M")
        end_time = timestamp(sys.argv[2], "%Y%m%d%H%M")
    else:
        now = int(time.time())
        start_time = now // 60 * 60 - data_delay
        end_time = now
    return start_time, end_time

def timestamp_to_utc(timestamp, utc_format='%Y-%m-%dT%H:%M:%SZ'):
    tz = pytz.utc
    local_tz = pytz.timezone('Asia/Chongqing')
    local_datetime = datetime.datetime.fromtimestamp(timestamp)
    local_dt = local_tz.localize(local_datetime, is_dst=None)
    utc_dt = local_dt.astimezone(tz)
    return utc_dt.strftime(utc_format)

def utc_to_timestamp(time_str,utc_format='%Y-%m-%dT%H:%M:%SZ'):
    t_obj = time.strptime(time_str, utc_format)
    return int(time.mktime(t_obj)+8*3600)

def get_customer_id():
    try:
        resp = HttpUtil.request_api('https://base-api.swiftfederation.com', '/v1.1/customer/', None, key_id, key_secret, HttpUtil.HTTP_GET)
        data = resp.json()
        return data['id']
    except Exception as e:
        logger.info("request for customer id err: %s", e)
        return 16939

def get_domain_list(customer_id):
    try:
        domain_list = []
        path = '/v1.0/customers/'+str(customer_id)+'/domains'
        resp = HttpUtil.request_api(uri, path, None, key_id, key_secret, HttpUtil.HTTP_GET)
        data = resp.json()
        for ele in data:
            domain_list.append(ele['name'])
        return domain_list
    except Exception as e:
        logger.fatal("request for domain list err: %s", e)
        sys.exit(0)

def get_total_flux(domains, start, end):
    try:
        result = {}
        params = {
            "domains": domains,
            "startTime": start,
            "endTime": end,
            "fillFixedTime": "true",
            "interval": "minute",
        }
        resp = HttpUtil.request_api(uri, uri_total_flux, json.dumps(params), key_id, key_secret, HttpUtil.HTTP_POST)
        data = resp.json()
        if len(data)==0:
            logger.fatal("request total flux is empty")
            sys.exit(0)
        for domain_ele in data:
            domain = domain_ele['domain']
            if not domain in result:
                result[domain] = []
            for ele in domain_ele['volumes']:
                timestamp = utc_to_timestamp(ele['timestamp'])
                value = ele['value']
                result[domain].append((timestamp,value))
        return result
    except Exception as e:
        logger.fatal("request total flux err: %s",e)
        sys.exit(0)

def get_hit_flux(domains, start, end):
    try:
        result = {}
        params = {
            "domains": domains,
            "startTime": start,
            "endTime": end,
            "fillFixedTime": "true",
            "interval": "minute",
        }
        resp = HttpUtil.request_api(uri, uri_hit_flux, json.dumps(params), key_id, key_secret, HttpUtil.HTTP_POST)
        data = resp.json()
        if len(data)==0:
            logger.fatal("request hit flux is empty")
            sys.exit(0)
        for domain_ele in data:
            domain = domain_ele['domain']
            if not domain in result:
                result[domain] = []
            for ele in domain_ele['hitVolumes']:
                timestamp = utc_to_timestamp(ele['timestamp'])
                value = ele['value']
                result[domain].append((timestamp,value))
        return result
    except Exception as e:
        logger.fatal("request hit flux err: %s", e)
        sys.exit(0)

def get_total_hit_request_num(domains, start, end):
    try:
        result_request = {}
        result_hit = {}
        params = {
            "domains": domains,
            "startTime": start,
            "endTime": end,
            "fillFixedTime": "true",
            "interval": "minute",
        }
        resp = HttpUtil.request_api(uri, uri_request_hit, json.dumps(params), key_id, key_secret, HttpUtil.HTTP_POST)
        data = resp.json()
        if len(data)==0:
            logger.fatal("request hit request is empty")
            sys.exit(0)
        for domain_ele in data:
            domain = domain_ele['domain']
            if not domain in result_request:
                result_request[domain] = []
                result_hit[domain] = []
            for ele in domain_ele['hitReqNumbers']:
                timestamp = utc_to_timestamp(ele['timestamp'])
                request = ele['request']
                hit = ele['hit']
                result_request[domain].append((timestamp,request))
                result_hit[domain].append((timestamp,hit))
        return result_request,result_hit
    except Exception as e:
        logger.fatal("request hit request err: %s", e)
        sys.exit(0)

def add_data(data, metric_name, data_container):
    try:
        for domain in data:
            for ts,value in data[domain]:
                data_line = DataLine(ts, domain, 0, source, "CN")
                data_container.add_data(data_line, metric_name, int(value))
    except Exception as e:
        logger.warn("add data err: %s, %s", e, metric_name)

if __name__ == '__main__':
    start = time.time()

    # DATABASE = DB('../../conf/config.json')
    # container = DataContainer(DATABASE)

    start_timestamp, end_timestamp = get_pull_interval()
    start_time_str = timestamp_to_utc(start_timestamp)
    end_time_str = timestamp_to_utc(end_timestamp)

    customer_id = get_customer_id()
    domain_list = get_domain_list(customer_id)

    traffic = get_total_flux(domain_list,start_time_str,end_time_str)
    traffic_hit = get_hit_flux(domain_list,start_time_str,end_time_str)
    request_num, request_num_hit = get_total_hit_request_num(domain_list,start_time_str,end_time_str)
    print (json.dumps(traffic,indent=2))

    # add_data(traffic,'traffic',container)
    # add_data(traffic_hit,'traffic_hit',container)
    # add_data(request_num,'request',container)
    # add_data(request_num_hit,'request_hit',container)

    # compute_other_filed(container)
    # container.save(1)
    # DATABASE.close()
    # divide(startTime - 2 * 3600, endTime, source)

    logger.info("it finished and takes %s secondes", time.time() - start)

