import logging
import os
from typing import Annotated, Optional
import sys

import vtk
import qt

import slicer
from slicer.i18n import tr as _
from slicer.i18n import translate
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
from slicer.parameterNodeWrapper import (
    parameterNodeWrapper,
    WithinRange,
)

from slicer import vtkMRMLScalarVolumeNode
from slicer.util import VTKObservationMixin, pip_install

#
# QC_Model
#

def func_import(install=False): 
    import os
    import json

    try:
        import shapeaxi
    except ImportError:
        pip_install('shapeaxi')
    
    try:   
        import torch
    except:
        print("torch not found")
        try:
            pip_install('torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu')
            import torch
            print("torch installed")
        except:
            print("Unable to install torch")
    
    try:
        import pytorch3d
    except ImportError:
        try : 
            import torch
            pyt_version_str = torch.__version__.split("+")[0].replace(".", "")
            version_str = "".join([f"py3{sys.version_info.minor}_cu", torch.version.cuda.replace(".", ""), f"_pyt{pyt_version_str}"])
            pip_install('--upgrade pip')
            pip_install('fvcore==0.1.5.post20220305')
            pip_install(f'--no-index --no-cache-dir pytorch3d -f https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/{version_str}/download.html')
        except:
            pip_install('--no-cache-dir torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0+cu113 --extra-index-url https://download.pytorch.org/whl/cu113')
            pip_install('--no-index --no-cache-dir pytorch3d -f https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/py39_cu113_pyt1110/download.html')


    
    # # try:
    # #     import pytorch3d
    # #     print("pytorch3d found")
    # try: 
    #     print("pytorch3d not found")
    #     try:
    #         # Get the absolute path of the current Python file
    #         current_directory = os.path.dirname(os.path.abspath(__file__))
    #         os.chdir(os.path.join(current_directory, "pytorch3d"))
    #         print(os.path.join(current_directory, "pytorch3d"))
    #         subprocess.run([sys.executable, "setup.py", "install"])
    #         import pytorch3d
    #         print("pytorch3d installed")
    #     except:
    #         print("Unable to install pytorch3d")

    # try:
    #     import pytorch3d
    # except: 
    #     print("pytorch3d not found")
    #     try:
    #         pip_install('git+https://github.com/facebookresearch/pytorch3d.git')
    #         import pytorch3d
    #         print("pytorch3d installed")
    #     except:
    #         print("Unable to install pytorch3d")


class QC_Model(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = _("QC_Model")  # TODO: make this more human readable by adding spaces
        # TODO: set categories (folders where the module shows up in the module selector)
        self.parent.categories = [translate("qSlicerAbstractCoreModule", "Examples")]
        self.parent.dependencies = []  # TODO: add here list of module names that this module requires
        self.parent.contributors = ["John Doe (AnyWare Corp.)"]  # TODO: replace with "Firstname Lastname (Organization)"
        # TODO: update with short description of the module and a link to online module documentation
        # _() function marks text as translatable to other languages
        self.parent.helpText = _("""
This is an example of scripted loadable module bundled in an extension.
See more information in <a href="https://github.com/organization/projectname#QC_Model">module documentation</a>.
""")
        # TODO: replace with organization, grant and thanks
        self.parent.acknowledgementText = _("""
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""")

        # Additional initialization step after application startup is complete
        slicer.app.connect("startupCompleted()", registerSampleData)


# #
# # Register sample data sets in Sample Data module
# #


def registerSampleData():
    """Add data sets to Sample Data module."""
    # It is always recommended to provide sample data for users to make it easy to try the module,
    # but if no sample data is available then this method (and associated startupCompeted signal connection) can be removed.

    import SampleData

    iconsPath = os.path.join(os.path.dirname(__file__), "Resources/Icons")

    # To ensure that the source code repository remains small (can be downloaded and installed quickly)
    # it is recommended to store data sets that are larger than a few MB in a Github release.

    # QC_Model1
    SampleData.SampleDataLogic.registerCustomSampleDataSource(
        # Category and sample name displayed in Sample Data module
        category="QC_Model",
        sampleName="QC_Model1",
        # Thumbnail should have size of approximately 260x280 pixels and stored in Resources/Icons folder.
        # It can be created by Screen Capture module, "Capture all views" option enabled, "Number of images" set to "Single".
        thumbnailFileName=os.path.join(iconsPath, "QC_Model1.png"),
        # Download URL and target file name
        uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
        fileNames="QC_Model1.nrrd",
        # Checksum to ensure file integrity. Can be computed by this command:
        #  import hashlib; print(hashlib.sha256(open(filename, "rb").read()).hexdigest())
        checksums="SHA256:998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
        # This node name will be used when the data set is loaded
        nodeNames="QC_Model1",
    )

    # QC_Model2
    SampleData.SampleDataLogic.registerCustomSampleDataSource(
        # Category and sample name displayed in Sample Data module
        category="QC_Model",
        sampleName="QC_Model2",
        thumbnailFileName=os.path.join(iconsPath, "QC_Model2.png"),
        # Download URL and target file name
        uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
        fileNames="QC_Model2.nrrd",
        checksums="SHA256:1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
        # This node name will be used when the data set is loaded
        nodeNames="QC_Model2",
    )


#
# QC_ModelParameterNode
#


@parameterNodeWrapper
class QC_ModelParameterNode:
    """
    The parameters needed by module.
    """
    input_dir: str
    out: str
    inputVolume: vtkMRMLScalarVolumeNode
    imageThreshold: Annotated[float, WithinRange(-100, 500)] = 100
    invertThreshold: bool = False
    thresholdedVolume: vtkMRMLScalarVolumeNode
    invertedVolume: vtkMRMLScalarVolumeNode


#
# QC_ModelWidget
#


class QC_ModelWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    """Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent=None) -> None:
        """Called when the user opens the module the first time and the widget is initialized."""
        ScriptedLoadableModuleWidget.__init__(self, parent)
        VTKObservationMixin.__init__(self)  # needed for parameter node observation
        self.logic = None
        self._parameterNode = None
        self._parameterNodeGuiTag = None

        self.input_dir = ""
        self.out = ""

    def setup(self) -> None:
        """Called when the user opens the module the first time and the widget is initialized."""
        ScriptedLoadableModuleWidget.setup(self)

        # Load widget from .ui file (created by Qt Designer).
        # Additional widgets can be instantiated manually and added to self.layout.
        uiWidget = slicer.util.loadUI(self.resourcePath("UI/QC_Model.ui"))
        self.layout.addWidget(uiWidget)
        self.ui = slicer.util.childWidgetVariables(uiWidget)

        # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
        # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
        # "setMRMLScene(vtkMRMLScene*)" slot.
        uiWidget.setMRMLScene(slicer.mrmlScene)

        # Create logic class. Logic implements all computations that should be possible to run
        # in batch mode, without a graphical user interface.
        self.logic = QC_ModelLogic()

        # Connections

        # These connections ensure that we update parameter node when scene is closed
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

        # Buttons
        self.ui.applyButton.connect("clicked(bool)", self.onApplyButton)
        self.ui.browseDirButton.connect("clicked(bool)", self.onbrowseDirButton)
        self.ui.browseOutButton.connect("clicked(bool)", self.onbrowseOutButton)
        self.ui.dirLineEdit.textChanged.connect(self.onEditDirLine)
        self.ui.outLineEdit.textChanged.connect(self.onEditOutLine)

        # Initialize attributes
        self.input_dir = self.ui.dirLineEdit.text
        self.out = self.ui.outLineEdit.text

        # Make sure parameter node is initialized (needed for module reload)
        self.initializeParameterNode()

    def cleanup(self) -> None:
        """Called when the application closes and the module widget is destroyed."""
        self.removeObservers()

    def enter(self) -> None:
        """Called each time the user opens this module."""
        # Make sure parameter node exists and observed
        self.initializeParameterNode()

    def exit(self) -> None:
        """Called each time the user opens a different module."""
        # Do not react to parameter node changes (GUI will be updated when the user enters into the module)
        if self._parameterNode:
            self._parameterNode.disconnectGui(self._parameterNodeGuiTag)
            self._parameterNodeGuiTag = None
            self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self._checkCanApply)

    def onSceneStartClose(self, caller, event) -> None:
        """Called just before the scene is closed."""
        # Parameter node will be reset, do not use it anymore
        self.setParameterNode(None)

    def onSceneEndClose(self, caller, event) -> None:
        """Called just after the scene is closed."""
        # If this module is shown while the scene is closed then recreate a new parameter node immediately
        if self.parent.isEntered:
            self.initializeParameterNode()

    def initializeParameterNode(self) -> None:
        """Ensure parameter node exists and observed."""
        # Parameter node stores all user choices in parameter values, node selections, etc.
        # so that when the scene is saved and reloaded, these settings are restored.

        self.setParameterNode(self.logic.getParameterNode())

        # Select default input nodes if nothing is selected yet to save a few clicks for the user
        if not self._parameterNode.inputVolume:
            firstVolumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
            if firstVolumeNode:
                self._parameterNode.inputVolume = firstVolumeNode

    def setParameterNode(self, inputParameterNode: Optional[QC_ModelParameterNode]) -> None:
        """
        Set and observe parameter node.
        Observation is needed because when the parameter node is changed then the GUI must be updated immediately.
        """

        if self._parameterNode:
            self._parameterNode.disconnectGui(self._parameterNodeGuiTag)
            self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self._checkCanApply)
        self._parameterNode = inputParameterNode
        if self._parameterNode:
            # Note: in the .ui file, a Qt dynamic property called "SlicerParameterName" is set on each
            # ui element that needs connection.
            self._parameterNodeGuiTag = self._parameterNode.connectGui(self.ui)
            self.addObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self._checkCanApply)
            self._checkCanApply()

    def _checkCanApply(self, caller=None, event=None) -> None:
        if self._parameterNode and self._parameterNode.inputVolume and self._parameterNode.thresholdedVolume:
            self.ui.applyButton.toolTip = _("Compute output volume")
            self.ui.applyButton.enabled = True
        else:
            self.ui.applyButton.toolTip = _("Select input and output volume nodes")
            self.ui.applyButton.enabled = True

    def onApplyButton(self) -> None:
        """Run processing when user clicks "Apply" button."""
        func_import()
        self.logic = QC_ModelLogic(
            class_column=self.class_column,
            csv=self.csv,
            input_dir=self.input_dir,
        )
        self.logic.process()
        self.addObserver(self.logic.cliNode,vtk.vtkCommand.ModifiedEvent,self.onProcessUpdate)
        # self.onProcessStarted()
    
    def onProcessUpdate(self,caller,event):
        self.ui.applyButton.enabled = False
        self.ui.applyButton.text = "Processing..."
        self.ui.applyButton.repaint()

        if self.logic.cliNode.GetStatus() & self.logic.cliNode.Completed:
            self.ui.applyButton.text = "Apply"
            self.ui.applyButton.enabled = True
            self.removeObserver(self.logic.cliNode,vtk.vtkCommand.ModifiedEvent,self.onProcessUpdate)
            # self.onProcessCompleted()
        
    def onbrowseDirButton(self) -> None:
        newDir = qt.QFileDialog.getExistingDirectory(self.parent, "Select a directory", '')
        if newDir != '':
            self.input_dir = newDir
            self.ui.dirLineEdit.setText(self.input_dir)
            print("browse F", self.input_dir)
    
    def onbrowseOutButton(self) -> None:
        newDir = qt.QFileDialog.getExistingDirectory(self.parent, "Select a directory", '')
        if newDir != '':
            self.out = newDir
            self.ui.outLineEdit.setText(self.out)
    
    def onEditDirLine(self) -> None:
        self.input_dir = self.ui.dirLineEdit.text
    
    def onEditOutLine(self) -> None:
        self.out = self.ui.outLineEdit.text



#
# QC_ModelLogic
#

class QC_ModelLogic(ScriptedLoadableModuleLogic):
    """This class should implement all the actual
    computation done by your module.  The interface
    should be such that other python code can import
    this class and make use of the functionality without
    requiring an instance of the Widget.
    Uses ScriptedLoadableModuleLogic base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """
    def __init__(self, class_column = "None", csv = "None", input_dir = "None", out = "None"):
        """
        Called when the logic class is instantiated. Can be used for initializing member variables.
        """
        ScriptedLoadableModuleLogic.__init__(self)
        self.input_dir = input_dir
        self.out = out
    
    def getParameterNode(self):
        return QC_ModelParameterNode(super().getParameterNode())

    def process(self):
        parameters = {}
        parameters ["input_dir"] = self.input_dir
        parameters ["out"] = self.out
        predictionProcess = slicer.modules.qc_modelcli
        self.cliNode = slicer.cli.run(predictionProcess, None, parameters)    
        return predictionProcess


#
# QC_ModelTest
#


class QC_ModelTest(ScriptedLoadableModuleTest):
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def setUp(self):
        """Do whatever is needed to reset the state - typically a scene clear will be enough."""
        slicer.mrmlScene.Clear()

    def runTest(self):
        """Run as few or as many tests as needed here."""
        self.setUp()
        self.test_QC_Model1()

    def test_QC_Model1(self):
        """Ideally you should have several levels of tests.  At the lowest level
        tests should exercise the functionality of the logic with different inputs
        (both valid and invalid).  At higher levels your tests should emulate the
        way the user would interact with your code and confirm that it still works
        the way you intended.
        One of the most important features of the tests is that it should alert other
        developers when their changes will have an impact on the behavior of your
        module.  For example, if a developer removes a feature that you depend on,
        your test should break so they know that the feature is needed.
        """

        self.delayDisplay("Starting the test")

        # Get/create input data

        import SampleData

        registerSampleData()
        inputVolume = SampleData.downloadSample("QC_Model1")
        self.delayDisplay("Loaded test data set")

        inputScalarRange = inputVolume.GetImageData().GetScalarRange()
        self.assertEqual(inputScalarRange[0], 0)
        self.assertEqual(inputScalarRange[1], 695)

        outputVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
        threshold = 100

        # Test the module logic

        logic = QC_ModelLogic()

        # Test algorithm with non-inverted threshold
        logic.process(inputVolume, outputVolume, threshold, True)
        outputScalarRange = outputVolume.GetImageData().GetScalarRange()
        self.assertEqual(outputScalarRange[0], inputScalarRange[0])
        self.assertEqual(outputScalarRange[1], threshold)

        # Test algorithm with inverted threshold
        logic.process(inputVolume, outputVolume, threshold, False)
        outputScalarRange = outputVolume.GetImageData().GetScalarRange()
        self.assertEqual(outputScalarRange[0], inputScalarRange[0])
        self.assertEqual(outputScalarRange[1], inputScalarRange[1])

        self.delayDisplay("Test passed")
