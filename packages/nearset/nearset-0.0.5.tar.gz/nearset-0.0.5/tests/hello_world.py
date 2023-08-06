from nearset import Nearset


ns = Nearset(lambda x: len(x))
ns["hi"] = "hi"
ns["how"] = "how"
ns["are"] = "are"
ns["you"] = "you ?"

print(ns)
