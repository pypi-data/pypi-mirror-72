#include <Python.h>
#include "GAnalytics.h"

typedef struct {
	PyObject_HEAD
		GAnalytics* gameAnalytics;
} gameAnalytics_obj;

extern PyTypeObject GameAnalyticsType;
