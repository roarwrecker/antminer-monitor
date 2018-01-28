### Contains the code behind for the readonly_temperature.html template ###

import re
from datetime import timedelta
import time
from flask import render_template, flash
from app.views.antminer_json import get_stats
from app import app, logger, __version__
from app.models import Miner, MinerModel

@app.route('/temperature')
def temperature():
    # Init variables
    start = time.clock()
    miners = Miner.query.all()
    models = MinerModel.query.all()
    active_miners = []
    inactive_miners = []
    temperatures = {}
    uptimes = {}

    for miner in miners:
        miner_stats = get_stats(miner.ip)
        # if miner not accessible
        if miner_stats['STATUS'][0]['STATUS'] == 'error':
            inactive_miners.append(miner)
        else:
            # Get the temperatures of the miner according to miner's model
            temps = [int(miner_stats['STATS'][1][temp]) for temp in
                     sorted(miner_stats['STATS'][1].keys(), key=lambda x: str(x)) if
                     re.search(miner.model.temp_keys + '[0-9]', temp) if miner_stats['STATS'][1][temp] != 0]
            # Get uptime
            uptime = timedelta(seconds=miner_stats['STATS'][1]['Elapsed'])
            temperatures.update({miner.ip: temps})
            uptimes.update({miner.ip: uptime})
            active_miners.append(miner)

            # Flash error messages
            if max(temps) >= 80:
                error_message = "[WARNING] High temperatures on miner '{}'.".format(miner.ip)
                logger.warning(error_message)
                flash(error_message, "warning")

    end = time.clock()
    loading_time = end - start
    return render_template('readonly_temperature.html',
                           version=__version__,
                           models=models,
                           active_miners=active_miners,
                           inactive_miners=inactive_miners,
                           temperatures=temperatures,
                           uptimes=uptimes,
                           loading_time=loading_time)
