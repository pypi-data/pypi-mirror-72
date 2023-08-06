#include <Python.h>
#include <stdio.h>
#include "parser.h"

static PyObject* parse_python_object(PyObject *self, PyObject *args) {
    const char* string;
    size_t initial_stack_size = 10;
    int is_jsonlines = 0;
#if PY_MAJOR_VERSION >= 3
    if (!PyArg_ParseTuple(args, "s|np", &string, &initial_stack_size, &is_jsonlines)) {
#else
    if (!PyArg_ParseTuple(args, "s|ni", &string, &initial_stack_size, &is_jsonlines)) {
#endif
        return NULL;
    }

    struct Lexer lexer;
    init(&lexer, string, initial_stack_size, is_jsonlines);
    while(lexer.lexer_status == CAN_ADVANCE) {
        advance(&lexer);
    }

    PyObject* ret = Py_BuildValue("s#", lexer.output, lexer.output_position-1);
    free((char*)lexer.output);
    free((Type*)lexer.stack);
    if(lexer.lexer_status == ERROR) {
        char error_message[30];
        strncpy(error_message, lexer.input+lexer.input_position, 30);

        PyErr_SetString(PyExc_ValueError, error_message);
        return NULL;
    }
    return ret;
}

static PyMethodDef parser_methods[] = { 
    {   
        "parse", parse_python_object, METH_VARARGS,
        "Parse JavaScript object string"
    },  
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef parser_definition = { 
    PyModuleDef_HEAD_INIT,
    "_chompjs",
    "C extension for fast JavaScript object parsing",
    -1, 
    parser_methods
};

PyMODINIT_FUNC PyInit__chompjs(void) {
    Py_Initialize();
    return PyModule_Create(&parser_definition);
}

#else

PyObject* init_chompjs(void) {
    return Py_InitModule("_chompjs", parser_methods);
}

#endif
