import os
os.environ['GAIA_TOOLS_DATA']='/home/vnagpal/research/gilaa/data/apogee'
import gaia_tools.load as gload
apogee_cat= gload.apogee()
#export GAIA_TOOLS_DATA='/home/vnagpal/research/gilaa/data/'