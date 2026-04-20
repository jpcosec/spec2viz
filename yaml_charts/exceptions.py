class YamlChartsError(Exception):
    pass

class ParseError(YamlChartsError):
    pass

class ValidationError(YamlChartsError):
    pass

class CompileError(YamlChartsError):
    pass

class RenderError(YamlChartsError):
    pass
