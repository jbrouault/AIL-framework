#!/usr/bin/env python3
# -*-coding:UTF-8 -*

"""
Update AIL
============================

Update AIL in the background

"""

import os
import sys
import redis
import subprocess

sys.path.append(os.path.join(os.environ['AIL_BIN'], 'lib/'))
import ConfigLoader

if __name__ == "__main__":

    config_loader = ConfigLoader.ConfigLoader()

    r_serv = config_loader.get_redis_conn("ARDB_DB")
    r_serv_onion = config_loader.get_redis_conn("ARDB_Onion")
    config_loader = None

    if r_serv.scard('ail:update_v1.5') != 5:
        r_serv.delete('ail:update_error')
        r_serv.set('ail:update_in_progress', 'v1.5')
        r_serv.set('ail:current_background_update', 'v1.5')
        if not r_serv.sismember('ail:update_v1.5', 'onions'):
            update_file = os.path.join(os.environ['AIL_HOME'], 'update', 'v1.5', 'Update-ARDB_Onions.py')
            process = subprocess.run(['python' ,update_file])

        if not r_serv.sismember('ail:update_v1.5', 'metadata'):
            update_file = os.path.join(os.environ['AIL_HOME'], 'update', 'v1.5', 'Update-ARDB_Metadata.py')
            process = subprocess.run(['python' ,update_file])

        if not r_serv.sismember('ail:update_v1.5', 'tags'):
            update_file = os.path.join(os.environ['AIL_HOME'], 'update', 'v1.5', 'Update-ARDB_Tags.py')
            process = subprocess.run(['python' ,update_file])

        if not r_serv.sismember('ail:update_v1.5', 'tags_background'):
            update_file = os.path.join(os.environ['AIL_HOME'], 'update', 'v1.5', 'Update-ARDB_Tags_background.py')
            process = subprocess.run(['python' ,update_file])
        if not r_serv.sismember('ail:update_v1.5', 'crawled_screenshot'):
            update_file = os.path.join(os.environ['AIL_HOME'], 'update', 'v1.5', 'Update-ARDB_Onions_screenshots.py')
            process = subprocess.run(['python' ,update_file])
        if r_serv.scard('ail:update_v1.5') != 5:
            r_serv.set('ail:update_error', 'Update v1.5 Failed, please relaunch the bin/update-background.py script')
        else:
            r_serv.delete('ail:update_in_progress')
            r_serv.delete('ail:current_background_script')
            r_serv.delete('ail:current_background_script_stat')
            r_serv.delete('ail:current_background_update')

    if r_serv.get('ail:current_background_update') == 'v2.4':
        r_serv.delete('ail:update_error')
        r_serv.set('ail:update_in_progress', 'v2.4')
        r_serv.set('ail:current_background_update', 'v2.4')
        r_serv.set('ail:current_background_script', 'domain update')

        update_file = os.path.join(os.environ['AIL_HOME'], 'update', 'v2.4', 'Update_domain.py')
        process = subprocess.run(['python' ,update_file])


        if int(r_serv_onion.scard('domain_update_v2.4')) != 0:
            r_serv.set('ail:update_error', 'Update v2.4 Failed, please relaunch the bin/update-background.py script')
        else:
            r_serv.delete('ail:update_in_progress')
            r_serv.delete('ail:current_background_script')
            r_serv.delete('ail:current_background_script_stat')
            r_serv.delete('ail:current_background_update')
            r_serv.delete('update:nb_elem_to_convert')
            r_serv.delete('update:nb_elem_converted')
