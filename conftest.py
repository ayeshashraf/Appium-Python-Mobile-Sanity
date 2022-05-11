from types import SimpleNamespace
import datetime
import pytest
from AppiumFrameWork.base.DriverClass import Driver
import AppiumFrameWork.utilities.Results_logging  as rl
from AppiumFrameWork.utilities.locators import Locators
from AppiumFrameWork.utilities.Results_logging import resultsObj

@pytest.fixture(scope='class')
def appium_connection_and_app_launch(request):
    #appium_service = AppiumService()
    driver1 = Driver()
    global driver
    driver = driver1.getDriverMethod()
    if request.cls is not None:
        request.cls.driver = driver

    # yield driver
    # time.sleep(5)
    # #driver.quit()
    # #appium_service.stop()

# hook for assertion message change
def pytest_assertrepr_compare(config, op, left, right):
    # state_app = driver.query_app_state("com.i2c.mcpcc.cmaFaceLift")
    state_app = driver.query_app_state(Locators.appPackage)

    if state_app == 1:
        resultsObj.setOperationalComments("App has terminated or crashed!")
        return [
                "App has terminated or crashed!:"
            ]

@pytest.fixture(autouse=True)
def check_crash_and_relaunch(request):
    # any code before yield / teardown code
    yield
    if request.node.rep_setup.failed:
        pass
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            state_app = driver.query_app_state(Locators.appPackage)
            if state_app == 1:
                resultsObj.setOperationalComments("App has terminated or crashed!")
                driver2 = Driver()
                launch_app = driver2.getDriverMethod()

# # # official
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture(autouse=True)
def log_result_fixture(request):
    # any code before yield / teardown code
    yield

    results_log = resultsObj  # Instantiate class Results()
    strDateTime = datetime.datetime.now()
    if not getattr(request.instance, 'result_data','Test') =='Test' :
        case_data = getattr(request.instance, 'result_data')
        # print(case_data)
        strTestCase = case_data[0]['Test_Case_ID']
        Scenario_Description = case_data[0]['Scenario_Description']
        strExpResult = case_data[0]['Expected_Result']
        input_1 = resultsObj.nanToStr(case_data[0]['Menu_Name'], "N/A")
        input_2 = resultsObj.nanToStr(case_data[0]['Sub_Menu'], "N/A")
        input_3 = resultsObj.nanToStr(case_data[0]['Screen_Tile'], "N/A")
        Input_Factors = input_1 + "|" + input_2 + "|" + input_3
        # menu_name = case_data[0]['Screen_Tile']

    else:
        test_function_arguments = request.node.funcargs  # this gets values of all test method arguments
        #print(test_function_arguments)
        n = SimpleNamespace(**test_function_arguments)
        strTestCase = n.strTestCase
        #print(strTestCase)
        Scenario_Description = n.Scenario_Description
        strExpResult = n.strExpResult
        input_1 = resultsObj.nanToStr(n.mainMenuDesc, "N/A")
        input_2 = resultsObj.nanToStr(n.subMenuDesc, "N/A")
        input_3 = resultsObj.nanToStr(n.screenTitle, "N/A")
        Input_Factors = input_1 + "|" + input_2 + "|" + input_3
        strActualResult = ""
        # menu_name = n.Screen_Tile

    if request.node.rep_setup.failed:
        pass
        #print("setting up a test failed!", request.node.nodeid)
        # results_log.printAndSetActualResult("Fail", "Test case setup failed")
    elif request.node.rep_setup.passed:
        # results_log.printAndSetActualResult("Pass", "Test case setup passed")
        if request.node.rep_call.failed:
            # results_log.printAndSetActualResult("Fail", "Test case failed because screen title -" + menu_name + "- did not match")
            # results_log.setActualResult("Fail")
            strActualResult = "Fail"
            results_log.setOperationalComments('Test Case Failed')
            # print("executing test failed", request.node.nodeid)
        elif request.node.rep_call.passed:
            # results_log.setActualResult("Pass")
            strActualResult = "Pass"
            results_log.setOperationalComments('Test Case Passed')

    results_log.SetOverAllStatus(strActualResult, "Pass")
    results_log.logResults(strTestCase, strDateTime, Scenario_Description,Input_Factors, strExpResult, strActualResult,
                            results_log.OverAllStatus, results_log.strComments, results_log.strScreenLaunchTime)
    # results_log = None

