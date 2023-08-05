#include "igeGameAnalytics.h"
#include "igeGameAnalytics_doc_en.h"
#include <map>
#include <string>


PyObject* gameAnalytics_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	gameAnalytics_obj* self = NULL;

	self = (gameAnalytics_obj*)type->tp_alloc(type, 0);
	self->gameAnalytics = GAnalytics::Instance();

	return (PyObject*)self;
}

void gameAnalytics_dealloc(gameAnalytics_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* gameAnalytics_str(gameAnalytics_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "gameAnalytics object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* gameAnalytics_Init(gameAnalytics_obj* self, PyObject* args, PyObject* kwargs)
{
	static char* kwlist[] = { "version", "game_key", "secret_key", "debug", NULL };
		
    char* version = nullptr;
	char* game_key = nullptr;
	char* secret_key = nullptr;
	int debug = 0;
    
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "sssi", kwlist, &version, &game_key, &secret_key, &debug)) return NULL;

	GAnalytics::Instance()->init(version, game_key, secret_key, debug);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* gameAnalytics_Release(gameAnalytics_obj* self)
{
	GAnalytics::Instance()->release();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* gameAnalytics_AddProgressionEvent(gameAnalytics_obj* self, PyObject* args, PyObject* kwargs)
{
	int progressionStatus = 1;	// Start = 1, Complete = 2, Fail = 3
	char* progression01 = nullptr;
	char* progression02 = nullptr;
	char* progression03 = nullptr;
	PyObject* score = nullptr;

	static char* kwlist[] = { "progressionStatus", "progression01", "progression02", "progression03", "score", NULL };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "is|ssO", kwlist, &progressionStatus, &progression01, &progression02, &progression03, &score)) return NULL;	
	if (score)
	{
		const int _score = PyLong_AsLong(score);
		GAnalytics::Instance()->addProgressionEvent(progressionStatus, progression01, progression02, progression03, _score);
	}
	else
	{
		GAnalytics::Instance()->addProgressionEvent(progressionStatus, progression01, progression02, progression03);
	}	

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* gameAnalytics_AddDesignEvent(gameAnalytics_obj* self, PyObject* args)
{
	char* eventId = nullptr;
	PyObject* value = nullptr;

	if (!PyArg_ParseTuple(args, "s|O", &eventId, &value)) return NULL;
	if (value)
	{
		double _value;
		if (PyFloat_Check(value))
		{
			_value = PyFloat_AsDouble(value);
		}
		else if (PyLong_Check(value))
		{
			_value = PyLong_AsDouble(value);			
		}
		GAnalytics::Instance()->addDesignEvent(eventId, _value);
	}
	
	else
	{
		GAnalytics::Instance()->addDesignEvent(eventId);
	}

	Py_INCREF(Py_None);
	return Py_None;
}

PyMethodDef gameAnalytics_methods[] = {
	{ "init", (PyCFunction)gameAnalytics_Init, METH_VARARGS | METH_KEYWORDS, gameAnalyticsInit_doc },
	{ "release", (PyCFunction)gameAnalytics_Release, METH_NOARGS, gameAnalyticsRelease_doc },
	{ "addProgressionEvent", (PyCFunction)gameAnalytics_AddProgressionEvent, METH_VARARGS | METH_KEYWORDS, gameAnalyticsAddProgressionEvent_doc },
	{ "addDesignEvent", (PyCFunction)gameAnalytics_AddDesignEvent, METH_VARARGS, gameAnalyticsAddDesignEvent_doc },
	{ NULL,	NULL }
};

PyGetSetDef gameAnalytics_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject GameAnalyticsType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igGameAnalytics",							/* tp_name */
	sizeof(gameAnalytics_obj),					/* tp_basicsize */
	0,											/* tp_itemsize */
	(destructor)gameAnalytics_dealloc,			/* tp_dealloc */
	0,											/* tp_print */
	0,											/* tp_getattr */
	0,											/* tp_setattr */
	0,											/* tp_reserved */
	0,											/* tp_repr */
	0,											/* tp_as_number */
	0,											/* tp_as_sequence */
	0,											/* tp_as_mapping */
	0,											/* tp_hash */
	0,											/* tp_call */
	(reprfunc)gameAnalytics_str,				/* tp_str */
	0,											/* tp_getattro */
	0,											/* tp_setattro */
	0,											/* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,							/* tp_flags */
	0,											/* tp_doc */
	0,											/* tp_traverse */
	0,											/* tp_clear */
	0,											/* tp_richcompare */
	0,											/* tp_weaklistoffset */
	0,											/* tp_iter */
	0,											/* tp_iternext */
	gameAnalytics_methods,						/* tp_methods */
	0,											/* tp_members */
	gameAnalytics_getsets,						/* tp_getset */
	0,											/* tp_base */
	0,											/* tp_dict */
	0,											/* tp_descr_get */
	0,											/* tp_descr_set */
	0,											/* tp_dictoffset */
	0,											/* tp_init */
	0,											/* tp_alloc */
	gameAnalytics_new,							/* tp_new */
	0,											/* tp_free */
};

static PyModuleDef gameAnalytics_module = {
	PyModuleDef_HEAD_INIT,
	"igegameAnalytics",							// Module name to use with Python import statements
	"GameAnalytics Module.",					// Module description
	0,
	gameAnalytics_methods						// Structure that defines the methods of the module
};

PyMODINIT_FUNC PyInit_igeGameAnalytics() {
	PyObject* module = PyModule_Create(&gameAnalytics_module);

	if (PyType_Ready(&GameAnalyticsType) < 0) return NULL;

	return module;
}
