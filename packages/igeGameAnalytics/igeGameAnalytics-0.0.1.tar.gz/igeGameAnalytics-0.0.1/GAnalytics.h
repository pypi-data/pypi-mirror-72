#pragma once

#include <map>
#include <string>

#ifdef _WIN32
#define IGE_EXPORT __declspec(dllexport)
#else
#define IGE_EXPORT
#endif

#ifdef NDEBUG
	#define LOG_VERBOSE(...)
	#define LOG_DEBUG(...)
	#define LOG(...)
	#define LOG_WARN(...)
	#define LOG_ERROR(...)
#else
	#if defined(__ANDROID__)
		#include <android/log.h>

		#define LOG_VERBOSE(...) __android_log_print(ANDROID_LOG_VERBOSE, "GameAnalytics", __VA_ARGS__);
		#define LOG_DEBUG(...) __android_log_print(ANDROID_LOG_DEBUG, "GameAnalytics", __VA_ARGS__);
		#define LOG(...) __android_log_print(ANDROID_LOG_INFO, "GameAnalytics", __VA_ARGS__);
		#define LOG_WARN(...) __android_log_print(ANDROID_LOG_WARN, "GameAnalytics", __VA_ARGS__);
		#define LOG_ERROR(...) __android_log_print(ANDROID_LOG_ERROR, "GameAnalytics", __VA_ARGS__);
	#else
		#define LOG_VERBOSE(...) printf(__VA_ARGS__);
		#define LOG_DEBUG(...) printf(__VA_ARGS__);
		#define LOG(...) printf(__VA_ARGS__);
		#define LOG_WARN(...) printf(__VA_ARGS__);
		#define LOG_ERROR(...) printf(__VA_ARGS__);
	#endif
#endif

class GameAnalyticsImpl;
class IGE_EXPORT GAnalytics
{
public:
	GAnalytics();
	~GAnalytics();
	void init(const char* version, const char* game_key, const char* secret_key, bool debug = false);
	void release();
	void addProgressionEvent(int progressionStatus, const char* progression01, const char* progression02, const char* progression03);
	void addProgressionEvent(int progressionStatus, const char* progression01, const char* progression02, const char* progression03, int score);
	void addDesignEvent(const char* eventId);
	void addDesignEvent(const char* eventId, double value);

	static GAnalytics* Instance()
	{
		if (instance == nullptr)
		{
			instance = new GAnalytics();
		}
		return instance;
	}
private:
	GameAnalyticsImpl* m_gameAnalyticsImpl;
	static GAnalytics* instance;
};
