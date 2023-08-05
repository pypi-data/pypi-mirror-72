#include "GameAnalyticsImpl.h"
#include "GAnalytics.h"

#include "GameAnalytics.h"
using namespace gameanalytics;

void GameAnalyticsImpl::Init(const char* version, const char* game_key, const char* secret_key, bool debug)
{
	if (debug)
	{
		GameAnalytics::setEnabledInfoLog(true);
		GameAnalytics::setEnabledVerboseLog(true);
	}
	GameAnalytics::configureBuild(version);
	GameAnalytics::initialize(game_key, secret_key);
}

void GameAnalyticsImpl::Release()
{
	GameAnalytics::onQuit();
}

void GameAnalyticsImpl::addProgressionEvent(int progressionStatus, const char* progression01, const char* progression02, const char* progression03)
{
	GameAnalytics::addProgressionEvent((EGAProgressionStatus)progressionStatus, progression01, progression02, progression03);
}

void GameAnalyticsImpl::addProgressionEvent(int progressionStatus, const char* progression01, const char* progression02, const char* progression03, int score)
{
	GameAnalytics::addProgressionEvent((EGAProgressionStatus)progressionStatus, progression01, progression02, progression03, score);
}

void GameAnalyticsImpl::addDesignEvent(const char* eventId)
{
	GameAnalytics::addDesignEvent(eventId);
}

void GameAnalyticsImpl::addDesignEvent(const char* eventId, double value)
{
	GameAnalytics::addDesignEvent(eventId, value);
}