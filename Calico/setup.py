from cx_Freeze import setup, Executable


executable = [
    Executable('Calico.py', icon="calico.ico"),
    Executable('parsetab.py', icon="calico.ico")]
setup(
    name="Calico",
    version="0.2.1",
    description="An interpreter for Calico V 0.2.1",
    executables=executable
)
