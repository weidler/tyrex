import importlib.util
spec = importlib.util.spec_from_file_location("FeatureExtractionAlgorithms", "fea/FeatureExtractionAlgorithms.py")
fea = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fea)

spec = importlib.util.spec_from_file_location("Parser", "parser/Parser.py")
parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser)
