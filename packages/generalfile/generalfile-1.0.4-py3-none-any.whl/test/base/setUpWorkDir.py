"""Just contains class for File handling tests"""

from generalfile.base.classpath import Path
from generalfile.base.classfile import File


class SetUpWorkDir:
    """Class to set up working dir for tests, File extensions import this class."""
    workingDir = Path(__file__).getParent(2).addPath("tests")
    if not workingDir.endsWithPath("test/tests"):
        raise EnvironmentError(f"Failed setting correct working dir, should be ..test/tests but it's {workingDir}")

    @classmethod
    def activate(cls):
        """Set working dir and clear it after it's made sure it's correct path."""
        File.setWorkingDir(cls.workingDir)
        if File.getWorkingDir().endsWithPath("tests"):
            File.clearFolder("", delete=True)


