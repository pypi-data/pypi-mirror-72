#include "GAnalytics.h"
#include "GameAnalyticsImpl.h"

GAnalytics* GAnalytics::instance = nullptr;

GAnalytics::GAnalytics()
	: m_gameAnalyticsImpl(new GameAnalyticsImpl())
{
	LOG("GAnalytics()");
}
GAnalytics::~GAnalytics()
{
	LOG("~GAnalytics()");
}

void GAnalytics::init(const char* version, const char* game_key, const char* secret_key, bool debug)
{
	m_gameAnalyticsImpl->Init(version, game_key, secret_key, debug);
}

void GAnalytics::release()
{
	m_gameAnalyticsImpl->Release();
}

void GAnalytics::addProgressionEvent(int progressionStatus, const char* progression01, const char* progression02, const char* progression03)
{
	m_gameAnalyticsImpl->addProgressionEvent(progressionStatus, progression01, progression02, progression03);
}

void GAnalytics::addProgressionEvent(int progressionStatus, const char* progression01, const char* progression02, const char* progression03, int score)
{
	m_gameAnalyticsImpl->addProgressionEvent(progressionStatus, progression01, progression02, progression03, score);
}

void GAnalytics::addDesignEvent(const char* eventId)
{
	m_gameAnalyticsImpl->addDesignEvent(eventId);
}

void GAnalytics::addDesignEvent(const char* eventId, double value)
{
	m_gameAnalyticsImpl->addDesignEvent(eventId, value);
}
