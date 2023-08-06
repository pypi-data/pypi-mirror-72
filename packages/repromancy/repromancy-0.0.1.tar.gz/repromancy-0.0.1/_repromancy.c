/*
         ▄▀▀▄ ▀▄  ▄▀▀▀▀▄   ▄▀▀▀█▀▀▄      ▄▀▀▀█▄    ▄▀▀▀▀▄   ▄▀▀▄▀▀▀▄ 
        █  █ █ █ █      █ █    █  ▐     █  ▄▀  ▀▄ █      █ █   █   █ 
        ▐  █  ▀█ █      █ ▐   █         ▐ █▄▄▄▄   █      █ ▐  █▀▀█▀  
          █   █  ▀▄    ▄▀    █           █    ▐   ▀▄    ▄▀  ▄▀    █  
        ▄▀   █     ▀▀▀▀    ▄▀            █          ▀▀▀▀   █     █   
        █    ▐            █             █                  ▐     ▐   
        ▐                 ▐             ▐                            
         ▄▀▀▄ ▄▀▄  ▄▀▀▀▀▄   ▄▀▀▄▀▀▀▄  ▄▀▀▀█▀▀▄  ▄▀▀█▄   ▄▀▀▀▀▄       
        █  █ ▀  █ █      █ █   █   █ █    █  ▐ ▐ ▄▀ ▀▄ █    █        
        ▐  █    █ █      █ ▐  █▀▀█▀  ▐   █       █▄▄▄█ ▐    █        
          █    █  ▀▄    ▄▀  ▄▀    █     █       ▄▀   █     █         
        ▄▀   ▄▀     ▀▀▀▀   █     █    ▄▀       █   ▄▀    ▄▀▄▄▄▄▄▄▀   
        █    █             ▐     ▐   █         ▐   ▐     █           
        ▐    ▐                       ▐                   ▐           
                 ▄▀▀█▄▄▄▄  ▄▀▀▄ ▀▀▄  ▄▀▀█▄▄▄▄  ▄▀▀▀▀▄                
                ▐  ▄▀   ▐ █   ▀▄ ▄▀ ▐  ▄▀   ▐ █ █   ▐                
                  █▄▄▄▄▄  ▐     █     █▄▄▄▄▄     ▀▄                  
                  █    ▌        █     █    ▌  ▀▄   █                 
                 ▄▀▄▄▄▄       ▄▀     ▄▀▄▄▄▄    █▀▀▀                  
                 █    ▐       █      █    ▐    ▐                     
                 ▐            ▐      ▐                               
*/

// see _cls_full_name in the repromancy package for an introduction

#include "Python.h"

static struct PyModuleDef module_def = {
    PyModuleDef_HEAD_INIT,
    "_repromancy",
    NULL,
    -1,
    NULL
};

// classes which directly inherit from object (or type) may not have their
// bases modified, this necessitates darker magic, and so importing the
// _repromancy module will modify the type object itself, altering the repr
static reprfunc original_type_repr = 0;

static PyObject *
repromancy_type_repr(PyObject* cls)
{
    PyObject* repr = 0;
    PyObject* qualname = PyObject_GetAttrString(cls, "__qualname__");
    if (!qualname){ PyErr_Clear(); }
    if (qualname &&
        PyUnicode_Check(qualname) &&
        PyUnicode_READ_CHAR(qualname, 0) == '<')
    {
        repr = PyUnicode_FromFormat("<class '%U'>", qualname);
    }
    else
    {
        repr = original_type_repr(cls);
    }
    Py_XDECREF(qualname);
    return repr;
}

// functions do not report the module that they were defined in, here we `fix`
// that inconsistency
static PyObject*
repromancy_func_repr(PyObject *func)
{
    PyObject* repr = 0;
    PyObject* module = PyObject_GetAttrString(func, "__module__");
    if (!module){ return 0; }
    PyObject* qualname = PyObject_GetAttrString(func, "__qualname__");
    if (qualname &&
        PyUnicode_Check(qualname) &&
        PyUnicode_READ_CHAR(qualname, 0) == '<')
    {
        repr = PyUnicode_FromFormat("<function '%U' at %p>",
            qualname,
            func
        );
    }
    else
    {
        repr = PyUnicode_FromFormat("<function '%U.%U' at %p>",
            module,
            qualname,
            func
        );
    }
    Py_DECREF(module);
    Py_XDECREF(qualname);
    return repr;
}

// methods usually just report the name of the function, rather than the repr
static PyObject*
repromancy_meth_repr(PyMethodObject *meth)
{
    return PyUnicode_FromFormat(
        "<bound method '%R' of '%R'>",
        meth->im_func,
        meth->im_self
    );
}

PyMODINIT_FUNC
PyInit__repromancy(void)
{
    // monkey patch certain builtin reprs, but only once
    if (original_type_repr == 0)
    {
        original_type_repr = PyType_Type.tp_repr;
        PyType_Type.tp_repr = (reprfunc)repromancy_type_repr;
        
        PyFunction_Type.tp_repr = (reprfunc)repromancy_func_repr;
        
        PyMethod_Type.tp_repr = (reprfunc)repromancy_meth_repr;
    }
    
    return PyModule_Create(&module_def);
}
