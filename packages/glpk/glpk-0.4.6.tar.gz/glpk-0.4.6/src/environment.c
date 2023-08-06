/**************************************************************************
Copyright (C) 2007, 2008 Thomas Finley, tfinley@gmail.com

This file is part of PyGLPK.

PyGLPK is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

PyGLPK is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyGLPK. If not, see <http://www.gnu.org/licenses/>.
**************************************************************************/

#include "2to3.h"

#include <glpk.h>
#include <limits.h>
#include "environment.h"
#include "structmember.h"
#include "util.h"

static int Environment_traverse(EnvironmentObject *self, visitproc visit,
		void *arg)
{
	Py_VISIT(self->version);
	Py_VISIT(self->term_hook);
	return 0;
}

static int Environment_clear(EnvironmentObject *self)
{
	if (self->weakreflist != NULL) {
		PyObject_ClearWeakRefs((PyObject*)self);
	}
	Py_CLEAR(self->version);
	Py_CLEAR(self->term_hook);
	return 0;
}

static void Environment_dealloc(EnvironmentObject *self)
{
	Environment_clear(self);
	Py_TYPE(self)->tp_free((PyObject*)self);
}

EnvironmentObject* Environment_New(void)
{
	EnvironmentObject *env = (EnvironmentObject*)
		PyObject_GC_New(EnvironmentObject, &EnvironmentType);
	if (env == NULL)
		return env;
	// Initialize data members.
	env->mem_limit = -1;
	env->term_on = 1;
	env->term_hook = NULL;
	env->version = Py_BuildValue("ii", GLP_MAJOR_VERSION, GLP_MINOR_VERSION);
	env->weakreflist = NULL;
	// Now return the structure.
	return env;
}

/****************** GET-SET-ERS ***************/

static PyObject* Environment_getblocks(EnvironmentObject *self,void *closure)
{
	int count;
	glp_mem_usage(&count, NULL, NULL, NULL);
	return PyInt_FromLong(count);
}

static PyObject* Environment_getblocks_peak(EnvironmentObject *self,
					   void *closure)
{
	int cpeak;
	glp_mem_usage(NULL, &cpeak, NULL, NULL);
	return PyInt_FromLong(cpeak);
}

static PyObject* Environment_getbytes(EnvironmentObject *self,void *closure)
{
#if GLPK_VERSION(4, 48)
	size_t total;
#else
	glp_long total;
#endif
	glp_mem_usage(NULL, NULL, &total, NULL);
#if GLPK_VERSION(4, 48)
	return PyInt_FromSize_t(total);
#else
	return PyInt_FromLong(((long)total.hi) << 32 | total.lo);
#endif
}

static PyObject* Environment_getbytes_peak(EnvironmentObject *self,
					   void *closure)
{
#if GLPK_VERSION(4, 48)
	size_t tpeak;
#else
	glp_long tpeak;
#endif
	glp_mem_usage(NULL, NULL, NULL, &tpeak);
#if GLPK_VERSION(4, 48)
	return PyInt_FromSize_t(tpeak);
#else
	return PyInt_FromLong(((long)tpeak.hi) << 32 | tpeak.lo);
#endif
}

static PyObject* Environment_getmemlimit(EnvironmentObject *self,
					 void *closure)
{
	if (self->mem_limit < 0)
		Py_RETURN_NONE;
	return PyInt_FromLong(self->mem_limit);
}

static int Environment_setmemlimit(EnvironmentObject *self, PyObject *value,
				   void *closure)
{
	int limit;
	if (value == NULL || value == Py_None) {
		limit = INT_MAX;
		self->mem_limit = -1;
	} else if (PyInt_Check(value)) {
		limit = PyInt_AS_LONG(value);
		if (limit < 0) {
			PyErr_SetString(PyExc_ValueError, "mem_limit must be non-negative");
			return -1;
		}
		self->mem_limit = limit;
                limit = limit > 0 ? limit : INT_MAX;
	} else {
		PyErr_SetString(PyExc_TypeError, "mem_limit must be int");
		return -1;
	}
	glp_mem_limit(limit);
	return 0;
}

/**************** TERMINAL BEHAVIOR ***********/

static int environment_term_hook(EnvironmentObject *env, const char *s)
{
	// When this is called, env->term_hook should *never* be NULL.
	PyObject_CallFunction(env->term_hook, "s", s);
	if (PyErr_Occurred())
		PyErr_Clear();
	return 1;
}

static PyObject* Environment_gettermon(EnvironmentObject *self,void *closure)
{
	if (self->term_on)
		Py_RETURN_TRUE;
	else
		Py_RETURN_FALSE;
}

static int Environment_settermon(EnvironmentObject *self,
				 PyObject *value, void *closure)
{
	if (!PyBool_Check(value)) {
		PyErr_SetString(PyExc_TypeError, "term_on must be set with bool");
		return -1;
	}
	glp_term_out(value==Py_True ? GLP_ON : GLP_OFF);
	self->term_on = value == Py_True ? 1 : 0;
	return 0;
}

static PyObject* Environment_gettermhook(EnvironmentObject *self,
					 void *closure)
{
	if (self->term_hook) {
		Py_INCREF(self->term_hook);
		return self->term_hook;
	} else {
		Py_RETURN_NONE;
	}
}

static int Environment_settermhook(EnvironmentObject *self,
				   PyObject *value, void *closure)
{
	// Set the value of the internal terminal hook variable.
	if (value==NULL || value==Py_None) {
		if (self->term_hook) {
			Py_DECREF(self);
		}
		Py_XDECREF(self->term_hook);
		self->term_hook=NULL;
	} else {
		if (self->term_hook==NULL) {
			Py_INCREF(self);
		}
		Py_INCREF(value);
		Py_XDECREF(self->term_hook);
		self->term_hook = value;
	}
	// Next, set the hook with the glp_set_hook function.
	if (self->term_hook) {
		glp_term_hook((int(*)(void*,const char*))environment_term_hook,
				(void*)self);
	} else {
		glp_term_hook(NULL, NULL);
	}
	return 0;
}

/****************** OBJECT DEFINITION *********/

int Environment_InitType(PyObject *module)
{
	return util_add_type(module, &EnvironmentType);
}

PyDoc_STRVAR(version_doc,
"Tuple holding the major version and minor version of the GLPKthat this\n"
"PyGLPK module was built upon. For example, if built against GLPK 4.31,\n"
"version==(4,31)."
);

static PyMemberDef Environment_members[] = {
	{"version", T_OBJECT_EX, offsetof(EnvironmentObject, version), READONLY,
		version_doc},
	{NULL}
};

PyDoc_STRVAR(mem_limit_doc,
"The memory limit in megabytes. None if no limit is set."
);

PyDoc_STRVAR(blocks_doc,
"The number of currently allocated memory blocks."
);

PyDoc_STRVAR(blocks_peak_doc,
"The peak value of the blocks attribute."
);

PyDoc_STRVAR(bytes_doc,
"The number of currently allocated memory bytes."
);

PyDoc_STRVAR(bytes_peak_doc, "The peak value of the bytes attribute.");

PyDoc_STRVAR(term_on_doc,
"Whether or not terminal output for the underlying GLPK procedures is on or\n"
"off."
);

PyDoc_STRVAR(term_hook_doc,
"Function to intercept all terminal output. This should be a callable object\n"
"that accepts a single string argument, or None to indicate that no hook is\n"
"set (e.g., all output goes to the terminal, default behavior). Note that\n"
"when the function is called, there is no guarantee that the input string\n"
"will be a full line, or even non-empty. All exceptions thrown by the\n"
"function will go ignored and unreported."
);

static PyGetSetDef Environment_getset[] = {
	{"mem_limit", (getter)Environment_getmemlimit, (setter)Environment_setmemlimit,
		mem_limit_doc, NULL},
	{"blocks", (getter)Environment_getblocks, (setter)NULL,
		blocks_doc, NULL},
	{"blocks_peak", (getter)Environment_getblocks_peak, (setter)NULL,
		blocks_peak_doc, NULL},
	{"bytes", (getter)Environment_getbytes, (setter)NULL,
		bytes_doc, NULL},
	{"bytes_peak", (getter)Environment_getbytes_peak, (setter)NULL,
		bytes_peak_doc, NULL},
	{"term_on", (getter)Environment_gettermon, (setter)Environment_settermon,
		term_on_doc, NULL},
	{"term_hook",(getter)Environment_gettermhook,(setter)Environment_settermhook,
		term_hook_doc, NULL},
	{NULL}
};

static PyMethodDef Environment_methods[] = {
	/*
	 * {"foo", (PyCFunction)Environment_Foo, METH_NOARGS,
	 * "foo()\n\n"
	 * "Dummy function."},
	 */
	{NULL}
};

PyDoc_STRVAR(env_doc,
"This represents the PyGLPK environment. Through this, one may control the\n"
"global behavior of the GLPK. One instance of this exists, named "
ENVIRONMENT_INSTANCE_NAME " in the\n"
"glpk module."
);

PyTypeObject EnvironmentType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name           = "glpk.Environment",
    .tp_basicsize      = sizeof(EnvironmentObject),
    .tp_dealloc        = (destructor) Environment_dealloc,
    .tp_flags          = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
    .tp_doc            = env_doc,
    .tp_traverse       = (traverseproc) Environment_traverse,
    .tp_clear          = (inquiry) Environment_clear,
    .tp_weaklistoffset = offsetof(EnvironmentObject, weakreflist),
    .tp_methods        = Environment_methods,
    .tp_members        = Environment_members,
    .tp_getset         = Environment_getset,
};
