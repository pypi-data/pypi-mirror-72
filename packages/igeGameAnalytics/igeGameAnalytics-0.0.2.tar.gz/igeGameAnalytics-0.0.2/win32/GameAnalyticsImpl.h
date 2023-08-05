#pragma onces
#include "GAnalytics.h"

class GameAnalyticsImpl {
public:
	GameAnalyticsImpl() {}
	~GameAnalyticsImpl() {}

	void Init(const char* version, const char* game_key, const char* secret_key, bool debug = false);
	void Release();
	void addProgressionEvent(int progressionStatus, const char* progression01, const char* progression02, const char* progression03);
	void addProgressionEvent(int progressionStatus, const char* progression01, const char* progression02, const char* progression03, int score);
	void addDesignEvent(const char* eventId);
	void addDesignEvent(const char* eventId, double value);
};
