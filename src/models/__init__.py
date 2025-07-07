import warnings

# Suppress specific deprecation warnings from FAISS
warnings.filterwarnings("ignore", category=DeprecationWarning, module="faiss.loader")
warnings.filterwarnings("ignore", message="builtin type SwigPyPacked has no __module__ attribute")
warnings.filterwarnings("ignore", message="builtin type SwigPyObject has no __module__ attribute")
warnings.filterwarnings("ignore", message="builtin type swigvarlink has no __module__ attribute")
