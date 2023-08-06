
def _jupyter_nbextension_paths():
    return [dict(section="notebook",
                 src="static",
                 dest="empinken",
                 require="empinken/index")]

def load_jupyter_server_extension(nbapp):
    nbapp.log.info("empinken enabled!")