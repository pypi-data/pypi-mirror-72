# igeGameAnalytics 

C++ extension GameAnalytics  for 3D and 2D games.

### Before running this tutorial, you have to install igeGameAnalytics
	[pip install igeGameAnalytics]

### Functions

`import igeGameAnalytics`

- init
	- ` igeGameAnalytics.init('version', 'game_key', 'secret_key', debug=True/False)`
- addProgressionEvent
	- `igeGameAnalytics.addProgressionEvent(progressionStatus, progression01, progression02, progression03, score)`

		- progressionStatus : int(Start = 1, Complete = 2, Fail = 3)
			- Status of added progression
		- progression01 : string
			- Required progression location
		- progression02 : string(optional)
			- Not required. Use if needed
		- progression03 : string(optional)
			- Not required. Use if needed
		- score : int(optional)
			- An optional score when a user completes or fails a progression attempt
	- example
		```
		igeGameAnalytics.addProgressionEvent(1, "world01", score=0)
		igeGameAnalytics.addProgressionEvent(1, "world01", "stage01")
		igeGameAnalytics.addProgressionEvent(1, "world01", "stage01", score=1)
		igeGameAnalytics.addProgressionEvent(1, "world01", "stage01", "level01")
		igeGameAnalytics.addProgressionEvent(2, "world01", "stage01", "level01", score=2)
		```
- addDesignEvent
	- `igeGameAnalytics.addDesignEvent(eventId, value)`

		- eventId : string
			-  The eventId is a hierarchy string that can consist of 1-5 segments separated by ‘:’. Each segment can have a max length of 32
		- value : float(optional)
			- A float event tied to the eventId. Will result in sum & mean values being available
	- example
		```
		igeGameAnalytics.addDesignEvent(event[0])
		igeGameAnalytics.addDesignEvent(event[0], 10)
		```
- ...