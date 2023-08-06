######################## FUNCTIONS ##############################
from lib.sjc import sjc
from lib.sea import sea
from lib.sjc_sea import sjc_sea
from lib.default import shared 
import re

SHOWS_TO_COPY = {
	'9-1-1' : sjc_sea,
	'20-20' : sjc,
	'60.Minutes' : sjc,
	'The.Affair' : sjc,
	'The.Amazing.Race' : sjc,
	'The.Amazing.Race.Canada' : sjc,
	'Anthony.Bourdain.Parts.Unknown' : sjc,
	'Bethenny.and.Fredrik' : sjc,
	'Better.Call.Saul' : sjc,
	'The.Big.Bang.Theory' : sjc,
	'Big.Little.Lies' : sjc,
	'Blue.Bloods' : sjc,
	'Cops' : sjc,
	'Diners.Drive-ins.and.Dives' : sjc,
	'Dragons.Den' : sjc,
	'Fear.the.Walking.Dead' : sjc,
	'Fresh.Off.the.Boat' : sjc,
	'Hardcore.Pawn' : sjc,
	'Hells.Kitchen' : sjc,
	'Into.the,Badlands' : sjc,
	'Jane.the.Virgin' : sjc,
	'Law.&.Order.Special.Victims.Unit' : sjc,
	'Llama.Llama' : sjc,
	'Million.Dollar.Listing.Los.Angeles' : sjc,
	'Mr.Robot' : sjc,
	'Ozark' : sjc,
	'Roseanne' : sjc,
	'Shameless' : sjc,
	'Shark.Tank' : sjc,
	'Shooter' : sjc,
	'Silicon.Valley' : sjc,
	'Sneaky.Pete' : sjc,
	'Suits' : sjc,
	'Survivor' : sjc,
	'This.is.Life.with.Lisa.Ling' : sjc,
	'The.Walking.Dead' : sjc,
	'Worlds.Toughest.Fixes' : sjc
}

DEFAULT_NOCOPY = {
	'default' : shared 
}

def get_show(directory):

	index = 0
	module = DEFAULT_NOCOPY['default']
	LIST_OF_SHOWS = SHOWS_TO_COPY.keys()

	for title in LIST_OF_SHOWS:
		result = re.search(title,'%s' % directory, re.IGNORECASE)
		if(result):
			key = LIST_OF_SHOWS[index]
			module = SHOWS_TO_COPY[key]
			return module
		else:
			pass

		index = index + 1

	return module
