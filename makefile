# Makefile for FMAplaylist, used for running the program (not installation!)
# See https://www.gnu.org/software/make/manual/make.html for a comprehensive, yet
# friendly introduction to makefiles.

# Default recipe; will download files and process them.
run : download
	@# We must invoke make again, so files_to_process is generated once again
	@# and includes any new, downloaded files.
	@make process

# Download files from FMA into the downloaded_tracks directory.
download : configure
	python FMAdownloader.py

# Implicit recipe describing how to process a single, downloaded track
tracks/%.mp3 : downloaded_tracks/%.mp3
	@echo Processing "$<"
	@# Remove silence from the start and end of the track, and
	@# add 0.3 seconds of silence to the end.
	@# See http://digitalcardboard.com/blog/2009/08/25/the-sox-of-silence/ for
	@# an explaination of this command.
	@sox $< $@ silence 1 0.1 0.1% reverse silence 1 0.1 0.1% reverse pad 0.0 0.3
	@# Remove the file from the downloaded folder (no need to waste space)
	@rm $<

# Variable listing the tracks inside the tracks directory that need to be made.
# This is done by looking at what tracks are in the downloaded_tracks directory.
# See https://www.gnu.org/software/make/manual/make.html#Wildcard-Function
files_to_process := $(patsubst downloaded_tracks/%,tracks/%,$(wildcard downloaded_tracks/*))

# Process downloaded files and move them to the tracks directory.
process : $(files_to_process)

# Configure the program, making it ready to be used.
configure : settings.py

# Populate settings.py with the API_KEY.
settings.py : 
	@echo "To use the Free Music Archive API, you need to obtain an API key."
	@echo "Visit https://freemusicarchive.org/api/agreement if you don't have one already."
	@echo 
	@read -p "API key: " input; \
	echo API_KEY = \"$$input\" > settings.py
