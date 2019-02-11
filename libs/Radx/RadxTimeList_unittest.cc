#include <limits.h>
#include "Radx/RadxTimeList.hh"
#include "gtest/gtest.h"


namespace {

// Step 2. Use the TEST macro to define your tests.
//
// TEST has two parameters: the test case name and the test name.
// After using the macro, you should define your test logic between a
// pair of braces.  You can use a bunch of macros to indicate the
// success or failure of a test.  EXPECT_TRUE and EXPECT_EQ are
// examples of such macros.  For a complete list, see gtest.h.
//
// <TechnicalDetails>
//
// In Google Test, tests are grouped into test cases.  This is how we
// keep test code organized.  You should put logically related tests
// into the same test case.
//
// The test case name and the test name should both be valid C++
// identifiers.  And you should not use underscore (_) in the names.
//
// Google Test guarantees that each test you define is run exactly
// once, but it makes no guarantee on the order the tests are
// executed.  Therefore, you should write your tests in such a way
// that their results don't depend on their order.
//
// </TechnicalDetails>



TEST(RadxTimeList, setModeFirst) {
  RadxTimeList timeList;
  timeList.clearMode();
  timeList.setModeFirst();
  EXPECT_EQ(1, timeList.getMode());
  EXPECT_EQ(RadxTimeList::MODE_FIRST, timeList.getMode());
}

TEST(RadxTimeList, compileListFromInterval) {
  RadxTimeList timeList;
  timeList.clearMode();
  RadxTime startTime;
  RadxTime endTime;

  endTime.set(RadxTime::NOW);
  timeList.setModeInterval(startTime, endTime);
  timeList.setDir("/Users/brenda/data/dorade/dow"); // timrex/swp.1080620053141.SPOLRVP8.0.001.8_SUR_v040");
  // timeList.setDir("/Users/brenda/Downloads");
  if (timeList.compile()) {
    cerr << timeList.getErrStr() << endl;
  }

  vector<string> pathList = timeList.getPathList();
  if (pathList.size() <= 0) {
    cerr << "pathList is empty" << endl;
    cerr << timeList.getErrStr() << endl;
  }
  else
    cerr << "pathList is NOT empty" << endl;

  for(vector<string>::const_iterator i = pathList.begin(); i != pathList.end(); ++i) {
    cerr << *i << endl;
  }
  cerr << endl;
  
  RadxTime firstTime;
  RadxTime lastTime;
  RadxTime dummyTime;
  
  string firstFilePath = pathList.at(0);
  /*
  size_t found;
  found = firstFilePath.find_last_of("/\\");
  string firstFile = firstFilePath.substr(found+1);
  //  timeList.getDoradeTime(firstFile, firstTime);
  timeList.getTimeFromFileName(firstFile, firstTime, dummyTime);
  string lastFilePath = pathList.at(pathList.size()-1);
  found = lastFilePath.find_last_of("/\\");
  string lastFile = lastFilePath.substr(found+1);

  //  timeList.getDoradeTime(lastFile, lastTime);
  timeList.getTimeFromFileName(lastFile, lastTime, dummyTime);
  */
  //  vector<RadxTime> validTimes = timeList.getValidTimes();
  //firstTime = validTimes.at(0);

  // getFirstAndLastTime(RadxTime &fileStartTime, RadxTime &fileEndTime)
  timeList.getFirstAndLastTime(firstTime, lastTime);

  cerr << "first time " << firstTime << endl;
  cerr << "last time " << lastTime << endl;

}

TEST(RadxTimeList, findFirstTimeInDataSet) {
  RadxTimeList timeList;
  timeList.clearMode();
  RadxTime startTime;
  RadxTime endTime;

  startTime.set(RadxTime::NOW);
  timeList.setModeFirst();
  
  //  timeList.getStartTime();
  timeList.setDir("/Users/brenda/data/dorade/dow"); // timrex/swp.1080620053141.SPOLRVP8.0.001.8_SUR_v040");
  // timeList.setDir("/Users/brenda/Downloads");
  if (timeList.compile()) {
    cerr << "Result of timeList.compile() " << timeList.getErrStr() << endl;
  }
  
  vector<string> pathList = timeList.getPathList();
  if (pathList.size() <= 0) {
    cerr << "pathList is empty" << endl;
    cerr << timeList.getErrStr() << endl;
  }
  else
    cerr << "pathList is NOT empty" << endl;

  for(vector<string>::const_iterator i = pathList.begin(); i != pathList.end(); ++i) {
    cerr << *i << endl;
  }
  cerr << endl;
  

  // I want to find the first time in the data set ...
  vector<RadxTime> validTimes = timeList.getValidTimes();
  if (validTimes.size() <= 0) {
    cerr << "validTimes is empty" << endl;
  } else {
    //TimePath timePath = timePathSet.begin();
    RadxTime firstTime = validTimes.at(0);
    cerr << "first time " << firstTime << endl;
  }
}

}  // namespace

