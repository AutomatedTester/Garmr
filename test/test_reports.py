import os
from garmr import Reporter

class TestReports:

    def setup_method(self, method):
        if os.path.exists("garmr-results.xml"):
            os.remove("garmr-results.xml")

    def test_report_throws_exception_with_no_data(self):
        reporter = Reporter()
        try:
            reporter.write_file()
            raise AssertionError("Exception should have been thrown")
        except AssertionError as e:
            raise
        except Exception:
            pass

    def test_reporter_formats_test_cases_with_no_errors_or_failures(self):
        tests_list = []
        tests_list.append({"name":"good test",
                           "time_taken": 1,
            })
        reporter = Reporter(tests_list)
        result = reporter._format_results()
        assert result["testcase"] == """<testcase classname="" name="%s" time="%s" />""" % \
                        (tests_list[0]["name"], tests_list[0]["time_taken"])
        assert result["time_taken"] == 1
        assert result["errors"] == 0
        assert result["failed"] == 0
        assert result["skips"] == 0 

    def test_reporter_formats_2_test_cases_with_no_errors_or_failures(self):
        tests_list = []
        tests_list.append({"name":"good test",
                           "time_taken": 1,
            })
        tests_list.append({"name":"good test 2",
                           "time_taken": 1,
            })
        reporter = Reporter(tests_list)
        result = reporter._format_results()
        expected = """<testcase classname="" name="%s" time="%s" />""" % \
                        (tests_list[0]["name"], tests_list[0]["time_taken"])
        expected += """<testcase classname="" name="%s" time="%s" />""" % \
                        (tests_list[1]["name"], tests_list[1]["time_taken"]) 
        assert result["testcase"] == expected, result["testcase"]
        assert result["time_taken"] == 2
        assert result["errors"] == 0
        assert result["failed"] == 0
        assert result["tests"] == 2
        assert result["skips"] == 0 

    def test_reporter_formats_2_test_cases_with_mix_of_errors_or_failures(self):
        tests_list = []
        tests_list.append({"name":"error test",
                           "time_taken": 1,
                           "errors" : True,
                           "message" : "omg i errored",
            })
        tests_list.append({"name":"failure test",
                           "time_taken": 1,
                           "failed" : True,
                           "message": "Omg I failed",
            })
        reporter = Reporter(tests_list)
        result = reporter._format_results()
        expected = """<testcase classname="" name="%s" time="%s" ><error>%s</error></testcase>""" % \
                        (tests_list[0]["name"], tests_list[0]["time_taken"],tests_list[0]["message"])
        expected += """<testcase classname="" name="%s" time="%s" ><failure>%s</failure></testcase>""" % \
                        (tests_list[1]["name"], tests_list[1]["time_taken"],tests_list[1]["message"]) 
        assert result["testcase"] == expected, result["testcase"]
        assert result["time_taken"] == 2
        assert result["errors"] == 1
        assert result["failed"] == 1
        assert result["skips"] == 0
     
    def test_reporter_formats_test_case_with_one_failure(self):
        tests_list = []
        tests_list.append({"name":"failedtest",
                           "time_taken": 1,
                           "failed": True,
                           "message": "Omg I failed",
            })
        reporter = Reporter(tests_list)
        result = reporter._format_results()
        assert result["testcase"] == """<testcase classname="" name="%s" time="%s" ><failure>%s</failure></testcase>""" % \
                        (tests_list[0]["name"], tests_list[0]["time_taken"],tests_list[0]["message"])
        assert result["time_taken"] == 1
        assert result["errors"] == 0
        assert result["failed"] == 1 
        assert result["skips"] == 0 
    
    def test_reporter_formats_test_case_with_error(self):
        tests_list = []
        tests_list.append({"name":"errorstest",
                           "time_taken": 1,
                           "errors": True,
                           "message": "Omg I errored"
            })
        reporter = Reporter(tests_list)
        result = reporter._format_results()
        assert result["testcase"] == """<testcase classname="" name="%s" time="%s" ><error>%s</error></testcase>""" % \
                        (tests_list[0]["name"], tests_list[0]["time_taken"],tests_list[0]["message"])
        assert result["time_taken"] == 1
        assert result["errors"] == 1
        assert result["failed"] == 0 
        assert result["skips"] == 0 

    def test_reporter_formats_test_case_with_skip(self):
        tests_list = []
        tests_list.append({"name":"skipstest",
                           "time_taken": 1,
                           "skips": True,
                           "message": "Omg I skipped"
            })
        reporter = Reporter(tests_list)
        result = reporter._format_results()
        assert result["testcase"] == """<testcase classname="" name="%s" time="%s" ><skipped>%s</skipped></testcase>""" % \
                        (tests_list[0]["name"], tests_list[0]["time_taken"],tests_list[0]["message"])
        assert result["time_taken"] == 1
        assert result["errors"] == 0
        assert result["failed"] == 0 
        assert result["skips"] == 1 

    def test_that_reporter_writes_to_disk(self):
        tests_list = []
        tests_list.append({"name":"skipstest",
                           "time_taken": 1,
            })
        suite_xml="""<?xml version="1.0" encoding="utf-8"?>
        <testsuite name="Garmr" errors="{error}" failures="{failure}" 
            skips="{skips}" tests="{numtests}" time="{timetaken}">
            {testresults}
        </testsuite>"""
        testcase = """<testcase classname="" name="%s" time="%s" />""" % \
                        (tests_list[0]["name"], tests_list[0]["time_taken"])

        expected = suite_xml.format(error=0, failure=0, skips=0, numtests=len(tests_list), 
                timetaken=1, testresults=testcase)

        reporter = Reporter(tests_list)
        reporter.write_results()

        f = open("garmr-results.xml", "r")
        contents = f.read()
        f.close()
        assert expected == contents
