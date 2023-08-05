//gameAnalytics init
PyDoc_STRVAR(gameAnalyticsInit_doc,
	"init the gameAnalytics system \n"\
	"\n"\
	"igeGameAnalytics.init(version, info1=1, info2=1, info3=1, info4=1, debug=False)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
    "    version : string\n"\
    "        your app version\n"\
    "    game_key : string\n"\
    "        your game key\n"\
    "    secret_key : string\n"\
    "        your secret key\n"\
	"    debug : bool(optional)\n"\
	"        False by default. Enable to get more device log");

//gameAnalytics release
PyDoc_STRVAR(gameAnalyticsRelease_doc,
	"release the gameAnalytics system\n"\
	"\n"\
	"igeGameAnalytics.release()");

//gameAnalytics addProgressionEvent
PyDoc_STRVAR(gameAnalyticsAddProgressionEvent_doc,
	"add progression event\n"\
	"\n"\
	"igeGameAnalytics.addProgressionEvent(progressionStatus, progression01, progression02, progression03, score)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    progressionStatus : int(Start = 1, Complete = 2, Fail = 3)\n"\
	"        Status of added progression\n"\
	"    progression01 : string\n"\
	"        Required progression location\n"\
	"    progression02 : string(optional)\n"\
	"        Not required. Use if needed\n"\
	"    progression03 : string(optional)\n"\
	"        Not required. Use if needed\n"\
	"    score : int(optional)\n"\
	"        An optional score when a user completes or fails a progression attempt");

//gameAnalytics addDesignEvent_doc
PyDoc_STRVAR(gameAnalyticsAddDesignEvent_doc,
	"add design event\n"\
	"\n"\
	"igeGameAnalytics.addDesignEvent(eventId, value)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    eventId : string\n"\
	"        The eventId is a hierarchy string that can consist of 1-5 segments separated by ‘:’. Each segment can have a max length of 32\n"\
	"    value : float(optional)\n"\
	"       A float event tied to the eventId. Will result in sum & mean values being available");