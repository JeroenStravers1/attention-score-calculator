Ubuntu

activate venv in attentionscorecalculator/bin
	source activate

install requirements (as non-root user, chown the relevant dirs to this user)
	pip3 install -r /path/to/requirements.txt

run Hug api:
	navigate to attentionscorecalculator/src
	hug -f api.py

run attention score calculator:
	navigate to attentionscorecalculator/src
	./attention_score_calculator.py



Usage of screen on Ubuntu server

type:
	screen
for new screen, type:
	screen -r
to reconnect to a disconnected screen (eg: on reconnect)

ctrl-a ctrl-c: create new window
ctrl-a ctrl-a: switch between windows
ctrl-a n     : toggle next window
ctrl-a p     : toggle previous window
ctrl-a "     : get list of all windows
ctrl-a A     : tool for naming windows
ctrl-a k     : kill current window
ctrl-a d     : detach from the session
