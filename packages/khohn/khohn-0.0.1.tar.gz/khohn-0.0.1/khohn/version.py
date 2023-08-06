
KHOHN_PROJ = "khohn"

KHOHN_VERSION_MAJOR = 0
KHOHN_VERSION_MINOR = 0
KHOHN_VERSION_PATCH = 1
KHOHN_VERSION_STRING = "{}.{}.{}".format(KHOHN_VERSION_MAJOR, 
                                         KHOHN_VERSION_MINOR,
                                         KHOHN_VERSION_PATCH)
                                         
                                         
khohn_version_format = lambda delim: delim.join([str(KHOHN_VERSION_MAJOR), 
                                                 str(KHOHN_VERSION_MINOR), 
                                                 str(KHOHN_VERSION_PATCH)])