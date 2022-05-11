import time
import pandas as pd
import allure
import pytest
import datetime
from pandas import isnull
from pytest_dependency import depends
import AppiumFrameWork.utilities.CustomLogger as cl
import AppiumFrameWork.utilities.Results_logging as rl
from AppiumFrameWork.base.BaseClass import BaseClass
from AppiumFrameWork.pages.LoginPage import LoginPage
from AppiumFrameWork.base.DriverClass import Driver
from AppiumFrameWork.base.DataClass import DataClass
from AppiumFrameWork.utilities.Paths import dataSheetPath
from AppiumFrameWork.utilities.Results_logging import resultsObj
from AppiumFrameWork.utilities.locators import Locators



##**************************************************************************************************************************************************************************************************
iterationHeaders = "strTestCase,testCaseFlag,Scenario_Description,strExpResult,userName,password,mainMenuDesc,subMenuDesc,screenTitle,is_negative_case,app_package_name"
# dataSheetPath = "C:\\Appium\\MobileAutomation\\AppiumFrameWork\\tests\\Automation_SmokeTest.xls"
primaryColumn = "Test_Case_ID"
# # Opening a file
# file1 = open('reports\\environment.properties', 'x')
# env = ["Device=Galaxy\n", "OS Version=11.0\n", "Environment=Production\n"]
#
# file1.writelines(env)
#
# # Closing file
# file1.close()


# noinspection PyTestParametrized
#@allure.title("TAG-Mobile- Goolge Nexus OS 10" + (date.strftime("%x")))
@allure.parent_suite("Sanity Verification")
@pytest.mark.usefixtures("appium_connection_and_app_launch")
class TestAppLaunch():
    dataObj = DataClass()
    launch_case_range = dataObj.getRange(dataSheetPath, "Launch")
    public_case_range = dataObj.getRange(dataSheetPath, "Public")
    overallPublic_case_range = dataObj.getRange(dataSheetPath, "allPublic")
    login_case_range = dataObj.getRange(dataSheetPath, "Login")
    secure_case_range = dataObj.getRange(dataSheetPath, "Secure")
    overallSecure_case_range = dataObj.getRange(dataSheetPath, "allSecure")
    logout_case_range = dataObj.getRange(dataSheetPath, "Logout")



    def setup_method(self):
        self.lp = LoginPage(self.driver)
        self.bc = BaseClass(self.driver)
        self.rl = resultsObj


    ##**************************************************************************************************************************************************************************************************
    ## This test verifies whether app launch is successful or not

    @allure.suite("App Launch Verification")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Verify App Launch")
    @allure.title("Verify App Launch")
    @pytest.mark.dependency(name="verifyLaunch")
    def test_verify_app_launch(self):
        resultsObj.strComments = ""
        resultsObj.strActualResult = ""
        resultsObj.OverAllStatus = ""
        # get data for this test case
        self.result_data = self.dataObj.runIteration(dataSheetPath, primaryColumn, "ST01", "ST01")
        time.sleep(2)
        assert self.bc.errorOccured() == True
        assert self.bc.waitUntillNotDisplays('Sign In', 8) == True
        assert self.bc.errorOccured() == True
        time.sleep(1)
        assert self.bc.verifyLaunch() == True
        self.bc.takescreenshot('App Launch')
        assert self.lp.verifyLoginScreen() == True
        self.rl.setOperationalComments('App launch Successful')
    ### *****************************************************************************************************************************************************************************
    ## This test verifies public menus are configured as per required config
    @allure.suite("Extra/Missing Public Menus Verification")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Extra/Missing Public Menus Verification")
    @allure.title("Verify Public Menus")
    @pytest.mark.dependency(name="allPublicMenus", depends=["verifyLaunch"])
    @pytest.mark.parametrize(iterationHeaders,dataObj.runIteration(dataSheetPath, primaryColumn, overallPublic_case_range[0], overallPublic_case_range[1]))
    def test_verify_allPublicmenus(self, request, strTestCase, testCaseFlag, Scenario_Description, strExpResult, userName, password, mainMenuDesc, subMenuDesc, screenTitle, is_negative_case, app_package_name):
        resultsObj.strComments = ""
        resultsObj.strActualResult = ""
        resultsObj.OverAllStatus = ""
        overallStatus = ""
        statusFlag1 = ""

        assert self.bc.verifyLaunch() == True
        time.sleep(1)
        assert self.lp.verifyLoginScreen() == True
        time.sleep(1)
        assert self.bc.menuExists() == True
        self.bc.openMenu()
        time.sleep(1)
        appMainMenus = self.bc.getAppMenus()
        sheetMainMenus = self.bc.getMenuFromSheet(dataSheetPath, 'Public', 'Menu_Name', 'Test_Case_Flag')
        assert self.bc.closemenuButtonExists() == True
        self.bc.closeMenu()
        assert self.bc.chkLength(appMainMenus, sheetMainMenus) == True
        statusFlag1 = self.bc.compArrays('Main', appMainMenus, sheetMainMenus)
        if statusFlag1 == False:
            overallStatus = 'Fail'
        else:
            overallStatus = 'Pass'
        for m in sheetMainMenus:
            sheetSubMenus = self.bc.getMenuFromSheet(dataSheetPath, m, 'Sub_Menu', 'Menu_Name')
            if len(sheetSubMenus) == 0:
                if overallStatus == "" or overallStatus == "Pass":
                    overallStatus = "Pass"
                continue
            else:
                time.sleep(1)
                if self.bc.menuExists():
                    self.bc.openMenu()
                assert self.bc.searchTapMenu(m) == True
                appSubMenus = self.bc.getAppMenus()
                assert self.bc.chkLength(appSubMenus, sheetSubMenus) == True
                tempStatus = self.bc.compArrays(m, appSubMenus, sheetSubMenus)
                if self.bc.closeSubMenuButtonExists():
                    self.bc.closeSubMenu()
                if tempStatus == False:
                    overallStatus = 'Fail'
        assert (overallStatus == 'Pass') == True

    ##**************************************************************************************************************************************************************************************************
    ## This test verifies navigation between public menus
    @allure.suite("Public Menus Verification")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Public Menus Verification")
    @allure.title("Verify Public Menus")
    # @allure.step({2},{6})
    @pytest.mark.dependency(name="publicMenu", depends=["verifyLaunch"])
    @pytest.mark.parametrize(iterationHeaders,dataObj.runIteration(dataSheetPath, primaryColumn, public_case_range[0], public_case_range[1]))
    def test_verify_publicmenus(self, request, strTestCase, testCaseFlag, Scenario_Description, strExpResult, userName, password, mainMenuDesc, subMenuDesc, screenTitle, is_negative_case, app_package_name):
        resultsObj.strComments = ""
        resultsObj.strActualResult = ""
        resultsObj.OverAllStatus = ""
        assert self.bc.verifyLaunch() == True
        time.sleep(1)
        assert self.lp.verifyLoginScreen() == True
        time.sleep(1)
        assert self.bc.menuExists() == True
        self.bc.openMenu()
        if isnull(subMenuDesc):
            assert self.bc.searchTapMenu(mainMenuDesc) == True
        else:
            assert self.bc.searchTapMenu(mainMenuDesc) == True
            assert self.bc.searchTapMenu(subMenuDesc) == True
        start_time = time.time()
        self.bc.waitUntilTextDisplays('Please Wait', 15)
        end_time = time.time()
        total_time = round((end_time - start_time), 2)
        str_total_time = str(total_time)
        resultsObj.setScreenLaunchTime('Screen Launch Time in seconds = ' + str_total_time)
        self.bc.hideKeyboard()
        screenLaunchResult = self.bc.screenLaunched(screenTitle)
        blankScreenResult = self.bc.chkBlankScreen()
        # buttonsVerificationResult = self.bc.chkAllButtons(screenTitle)
        buttonsVerificationResult = True
        errorOccured = self.bc.errorOccured()
        if self.bc.backArrowExists():
            self.bc.tapBackArrow()
        assert self.bc.screenLaunchTimeOK(5, total_time) == True
        assert (screenLaunchResult == True and blankScreenResult == True and buttonsVerificationResult == True and errorOccured == True) == True

    ##**************************************************************************************************************************************************************************************************
    ## This test verifies that login action of the app functions properly
    @allure.suite("Login Verification")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Verify App Login")
    @allure.title("Verify App Login")
    @pytest.mark.dependency(name="Login", depends=["verifyLaunch"])
    @pytest.mark.parametrize(iterationHeaders, dataObj.runIteration(dataSheetPath, primaryColumn, login_case_range[0] , login_case_range[1] ))
    def test_verify_login(self,request, strTestCase, testCaseFlag, Scenario_Description, strExpResult, userName, password, mainMenuDesc, subMenuDesc, screenTitle, is_negative_case,app_package_name):
        # depends(request, ["TestAppLaunch::test_verify_app_launch"])
        resultsObj.strComments = ""
        resultsObj.strActualResult = ""
        resultsObj.OverAllStatus = ""
        assert self.bc.verifyLaunch() == True
        time.sleep(1)
        assert self.lp.verifyLoginScreen() == True
        time.sleep(1)
        assert self.lp.enterUsername(userName) == True
        assert self.lp.enterPassword(password) == True
        assert self.lp.signInExists() == True
        self.lp.clickSignIn()
        time.sleep(10)
        assert self.bc.waitUntilTextDisplays('Please Wait', 30) == True
        self.bc.popUpsHandled()
        self.bc.takescreenshot('Login')
        assert self.bc.errorOccured() == True
        assert self.bc.noCardFoundError() == True
        assert self.bc.verifyUserLoggedIn() == True


    ##**************************************************************************************************************************************************************************************************
    ## This test verifies secure menus are configured as per required config
    @allure.suite("Extra/Missing Secure Menus Verification")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Extra/Missing Secure Menus Verification")
    @allure.title("Verify Secure Menus")
    @pytest.mark.dependency(name="allSecureMenus", depends=["Login"])
    @pytest.mark.parametrize(iterationHeaders, dataObj.runIteration(dataSheetPath, primaryColumn, overallSecure_case_range[0], overallSecure_case_range[1]))
    def test_verify_allSecuremenus(self, request, strTestCase, testCaseFlag, Scenario_Description, strExpResult, userName, password,mainMenuDesc, subMenuDesc, screenTitle, is_negative_case,app_package_name):
        resultsObj.strComments = ""
        resultsObj.strActualResult = ""
        resultsObj.OverAllStatus = ""
        overallStatus = ""
        assert self.bc.verifyLaunch() == True
        time.sleep(1)
        if self.bc.verifyUserLoggedIn():
          pass
        else:
            assert self.lp.verifyLoginScreen() == True
            time.sleep(1)
            assert self.lp.enterUsername(userName) == True
            assert self.lp.enterPassword(password) == True
            assert self.lp.signInExists() == True
            self.lp.clickSignIn()
            assert self.bc.waitUntilTextDisplays('Please Wait', 15) == True
            self.bc.popUpsHandled()
            assert self.bc.errorOccured() == True
            assert self.bc.noCardFoundError() == True

        assert self.bc.menuExists() == True
        self.bc.openMenu()
        time.sleep(1)
        appMainMenus = self.bc.getAppMenus()
        sheetMainMenus = self.bc.getMenuFromSheet(dataSheetPath, 'Secure', 'Menu_Name', 'Test_Case_Flag')
        assert self.bc.chkLength(appMainMenus, sheetMainMenus) == True
        statusFlag1 = self.bc.compArrays('Main', appMainMenus, sheetMainMenus)
        if statusFlag1 == False:
            overallStatus = 'Fail'
        else:
            overallStatus = 'Pass'
        for m in sheetMainMenus:
            sheetSubMenus = self.bc.getMenuFromSheet(dataSheetPath, m, 'Sub_Menu', 'Menu_Name')
            if len(sheetSubMenus) == 0:
                if overallStatus == "" or overallStatus == "Pass":
                    overallStatus = "Pass"
                continue
            else:
                time.sleep(1)
                if self.bc.menuExists():
                    self.bc.openMenu()
                assert self.bc.searchTapMenu(m) == True
                appSubMenus = self.bc.getAppMenus()
                assert self.bc.chkLength(appSubMenus, sheetSubMenus) == True
                tempStatus = self.bc.compArrays(m, appSubMenus, sheetSubMenus)
                assert self.bc.closeSubMenuButtonExists() == True
                self.bc.closeSubMenu()
                if tempStatus == False:
                    overallStatus = 'Fail'
        assert (overallStatus == 'Pass') == True

    ##**************************************************************************************************************************************************************************************************
    ## This test verifies navigation between secure menus
    @allure.suite("Private Menus Verification")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Private Menu Traversing Verification")
    @allure.title("Verify Private Menu")
    @pytest.mark.dependency(name="Menu", depends=["Login"])
    @pytest.mark.parametrize(iterationHeaders, dataObj.runIteration(dataSheetPath, primaryColumn, secure_case_range[0], secure_case_range[1]))
    # @allure.severity(allure.severity_level.NORMAL)
    def test_verify_menu_screens(self, request, strTestCase, testCaseFlag, Scenario_Description, strExpResult, userName, password, mainMenuDesc, subMenuDesc, screenTitle, is_negative_case,app_package_name):
        resultsObj.strComments = ""
        resultsObj.strActualResult = ""
        resultsObj.OverAllStatus = ""
        assert self.bc.verifyLaunch() == True
        time.sleep(1)

        if self.bc.verifyUserLoggedIn():
            pass
        else:
            assert self.lp.verifyLoginScreen() == True
            time.sleep(1)
            assert self.lp.enterUsername(userName) == True
            assert self.lp.enterPassword(password) == True
            assert self.lp.signInExists() == True
            self.lp.clickSignIn()
            assert self.bc.waitUntilTextDisplays('Please Wait', 15) == True
            self.bc.popUpsHandled()
            assert self.bc.errorOccured() == True
            assert self.bc.noCardFoundError() == True

        assert self.bc.menuExists() == True
        # cl.allureLogs(self.driver,"Menu Exist Verification")
        self.bc.openMenu()
        # objComm.allureLogs(self.driver,"Open Menu Verification")
        time.sleep(2)
        if self.bc.subMenuBackButtonExists():
            self.bc.tapSubMenuBack()
        if isnull(subMenuDesc):

            assert self.bc.searchTapMenu(mainMenuDesc) == True
        else:
            assert self.bc.searchTapMenu(mainMenuDesc) == True
            assert self.bc.searchTapMenu(subMenuDesc) == True
        start_time = time.time()
        self.bc.waitUntilTextDisplays('Please Wait', 15)
        end_time = time.time()
        total_time = round((end_time - start_time), 2)
        str_total_time = str(total_time)
        resultsObj.setScreenLaunchTime('Screen Launch Time in seconds = ' + str_total_time)
        self.bc.hideKeyboard()
        screenLaunchResult = self.bc.screenLaunched(screenTitle)
        blankScreenResult = self.bc.chkBlankScreen()
        # buttonsVerificationResult = self.bc.chkAllButtons(screenTitle)
        buttonsVerificationResult = True
        errorOccured = self.bc.errorOccured()
        if self.bc.backArrowExists():
            self.bc.tapBackArrow()
        assert self.bc.screenLaunchTimeOK(5, total_time) == True
        assert (screenLaunchResult == True and blankScreenResult == True and buttonsVerificationResult == True and errorOccured == True) == True

    # ######**************************************************************************************************************************************************************************************************
    # # *******This test verifies that logout action of the app functions properly
    # @allure.suite("Logout Verification")
    # @allure.severity(allure.severity_level.NORMAL)
    # @allure.description("Logout Verification")
    # @allure.title("Verify Logout")
    # # @pytest.mark.dependency(name="LogOut", depends=["Login"])
    # @pytest.mark.parametrize(iterationHeaders, dataObj.runIteration(dataSheetPath, primaryColumn, logout_case_range[0], logout_case_range[1]))
    # # @allure.severity(allure.severity_level.NORMAL)
    # def test_verify_logout(self, request,strTestCase, testCaseFlag, Scenario_Description, strExpResult, userName, password, mainMenuDesc, subMenuDesc, screenTitle, is_negative_case,app_package_name):
    #     resultsObj.strComments = ""
    #     resultsObj.strActualResult = ""
    #     resultsObj.OverAllStatus = ""
    #     assert self.bc.verifyLaunch() == True
    #     if self.bc.verifyUserLoggedIn():
    #         pass
    #     else:
    #         assert self.lp.verifyLoginScreen() == True
    #         time.sleep(1)
    #         assert self.lp.enterUsername(userName) == True
    #         assert self.lp.enterPassword(password) == True
    #         assert self.lp.signInExists() == True
    #         self.lp.clickSignIn()
    #         assert self.bc.waitUntilTextDisplays('Please Wait', 15) == True
    #         self.bc.popUpsHandled()
    #         assert self.bc.errorOccured() == True
    #         assert self.bc.noCardFoundError() == True
    #
    #     assert self.bc.menuExists() == True
    #     self.bc.openMenu()
    #     time.sleep(1)
    #     if self.bc.subMenuBackButtonExists():
    #         self.bc.tapSubMenuBack()
    #     assert self.bc.logoutExists() == True
    #     assert self.bc.logout() == True
    #     self.bc.takescreenshot('Logout Confirmation')
    #     assert self.lp.verifyLoginScreen()
    #     self.bc.takescreenshot('Logout')
    #     self.rl.setOperationalComments("Logout Successful")
# # ##**************************************************************************************************************************************************************************************************
# #
# # # We can use an if __name__ == "__main__" block to allow or
# # # # prevent parts of code from being run when the modules are imported.
# # # if __name__ == '__main__':
# # #     unittest.main()
