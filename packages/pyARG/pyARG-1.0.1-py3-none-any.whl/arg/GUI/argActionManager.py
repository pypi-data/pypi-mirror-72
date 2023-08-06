#HEADER
#                       arg/GUI/argActionManager.py
#               Automatic Report Generator (ARG) v. 1.0
#
# Copyright 2020 National Technology & Engineering Solutions of Sandia, LLC
# (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S.
# Government retains certain rights in this software.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Questions? Visit gitlab.com/AutomaticReportGenerator/arg
#
#HEADER

########################################################################
# Import GUI packages
from PySide2.QtCore             import QObject

# Import ARG-GUI modules
from arg.GUI.argQuitAction              import *
from arg.GUI.argOpenAction              import *
from arg.GUI.argOpenRecentAction        import *
from arg.GUI.argRunAction               import *
from arg.GUI.argCleanAction             import *
from arg.GUI.argSaveBeforeRunAction     import *
from arg.GUI.argSaveAction              import *
from arg.GUI.argSaveAsAction            import *
from arg.GUI.argReloadAction            import *
from arg.GUI.argHelpAction              import *
from arg.GUI.argAboutAction             import *
from arg.GUI.argOpenUserSettingsAction  import *

########################################################################
class argActionManager(QObject):
    """An action manager class to cover all available actions
    """

    ####################################################################
    def __init__(self, parent=None):
        super(argActionManager, self).__init__(parent)

        # All available actions
        self.quitAct = argQuitAction(self)
        self.openAct = argOpenAction(self)
        self.saveAct = argSaveAction(self)
        self.saveAsAct = argSaveAsAction(self)
        self.saveBeforeRunAct = argSaveBeforeRunAction(self)
        self.runAct = argRunAction(self)
        self.cleanAct = argCleanAction(self)
        self.reloadAct = argReloadAction(self)
        self.helpAct = argHelpAction(self)
        self.openUserSettingsAct = argOpenUserSettingsAction(self)
        self.aboutAct = argAboutAction(self)
        self.maxNumberOfActions = 10
        self.openRecentActs = []

    ########################################################################
    def initActionFromSettings(self):

        # fill actions from settings
        settings = QApplication.instance().settingsController
        permanentSettings = QSettings(QSettings.IniFormat, QSettings.UserScope, settings.getCompanyName(), settings.getToolName())
        recentMenuFilesNames = permanentSettings.value(settings.getRecentMenuSettings())
        if recentMenuFilesNames:
            if isinstance(recentMenuFilesNames, str):
                self.createOpenRecentAction(recentMenuFilesNames)
            else:
                # To keep the order of the list with insertion comment, we need to inverse it
                recentMenuFilesNamesInverted = []
                for fileName in recentMenuFilesNames:
                    recentMenuFilesNamesInverted.insert(0, fileName)
                for fileName in recentMenuFilesNamesInverted:
                    self.createOpenRecentAction(fileName)

    ########################################################################
    def createOpenRecentAction(self, fileName):

        # Verify if the fileName already exists
        needsCreate = True
        for openRecentAct in self.openRecentActs:
            if openRecentAct.getFileName() == fileName:
                #in the action already exist, move it on the top of the list and return it
                self.openRecentActs.remove(openRecentAct)
                self.openRecentActs.insert(0, openRecentAct)
                needsCreate = False

        if needsCreate:
            openRecentAction = argOpenRecentAction(fileName, self)
            self.openRecentActs.insert(0, openRecentAction)

            # If the number of actions is more than the maximum allowed, we remove the old one
            if len(self.openRecentActs) > self.maxNumberOfActions:
                self.openRecentActs.pop(len(self.openRecentActs) - 1)

        # settings
        settings = QApplication.instance().settingsController
        permanentSettings = QSettings(QSettings.IniFormat, QSettings.UserScope, settings.getCompanyName(), settings.getToolName())

        openRecentActSttings = []
        for openRecentAct in self.openRecentActs:
            openRecentActSttings.append(openRecentAct.getFileName())

        permanentSettings.setValue(settings.getRecentMenuSettings(), openRecentActSttings)

        if needsCreate:
            return openRecentAction
        else:
            return None

    ########################################################################
    def getActions(self):

        return self.openRecentActs

########################################################################
