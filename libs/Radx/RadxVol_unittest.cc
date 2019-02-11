#include <limits.h>
#include "Radx/RadxVol.hh"
#include "Radx/RadxRay.hh"
#include "Radx/RadxField.hh"
#include "Radx/RadxFile.hh"
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





// take an existing field in a volume, copy it,
// rename it, then insert new data values
TEST(RadxVol, createRadxVolumeDeNovo) {
  
  Radx::si16 rawData[100];

  for (int i=0; i<100; i++) {
    rawData[i] = i;
  }

  Radx::si16 newData[100];

  for (int i=0; i<100; i++) {
    newData[i] = i * -1;
  }

  int nSweeps = 2;
  int nRays = 4;
  int nFields = 2;
  int nGates = 5;

  /* layout should be like this ...
    sweep 0:  0 ... 19
    Field 0: "VEL" 
    ray 0:  0  1  2  3  4 
    ray 1:  5  6  7  8  9
    ray 2: 10 11 12 13 14
    ray 3: 15 16 17 18 19

    Field 1: "DBZ" 
    ray 0: 50 51 52 53 54 
    ray 1: 55 56 57 58 59
    ray 2: 60 61 62 63 64
    ray 3: 65 66 67 68 69

    sweep: 1: 20 ... 39
  */

  RadxVol *radxVol = new RadxVol();

  // So, is the ray the base element? i.e. create rays first,
  // then add fields (filled with data)  to the rays
  // associate the ray with a sweep number?
  // then add the ray to the volume?
  // finally move the data from the fields to a giant memory
  // space managed by the volume, with rays, sweeps, and fields
  // pointing to sections in the giant memory space?

  // for each sweep 
  for (int s=0; s<nSweeps; s++) {
    // for each ray of data
    for (int r=0; r<nRays; r++) {
      RadxRay *newRay = new RadxRay();

      newRay->setVolumeNumber(1);
      newRay->setSweepNumber(s);
      newRay->setRayNumber(r);
        
      //      const string name = "VEL";
      //const string units = "m/s"; 
      Radx::si16 missingValue = -999;
      const Radx::si16 *data = &rawData[0];
      double scale = 1.0;
      double offset = 0.0;
      bool isLocal = false;

      int idx;
      idx = s*20 + r*nGates;   
      RadxField *field1 = newRay->addField("VEL", "m/s", nGates, missingValue, &rawData[idx], scale, offset, isLocal);
      idx += 50;
      RadxField *field2 = newRay->addField("DBZ", "dB", nGates, missingValue, &rawData[idx], scale, offset, isLocal);

      // to avoid this warning ...
      // WARNING - Range geom has not been set on ray
      double startRangeKm = 3.0;
      double gateSpacingKm = 5.0;
      newRay->setRangeGeom(startRangeKm, gateSpacingKm);

      radxVol->addRay(newRay);
    }
  }

  radxVol->loadFieldsFromRays(); // moves data from ray fields to volumes  
  
  radxVol->printWithFieldData(cout); 

  // ok, now take each field, copy its metadata, insert new data, and
  // add it to the volume.

  // move the data back to the rays, so that I can add a couple
  // new fields to the rays
  radxVol->loadRaysFromFields();

  // fetch the total number of rays (#sweeps * #rays)
  // for each sweep 
  //for (int s=0; s<nSweeps; s++) {
    // for each ray of data
    vector<RadxRay *> currentRays = radxVol->getRays();
    // TODO: use vector iterator here ...
    int rayNum = 0;
    //for (int r=0; r<nRays; r++) {

    for (vector<RadxRay *>::iterator r=currentRays.begin(); r<currentRays.end(); r++) {
      RadxRay *newRay = *r;
      //RadxRay *oldRay = *r;
      //RadxRay *newRay = new RadxRay();

      //newRay->copyMetaData(*oldRay);
      //newRay->setVolumeNumber(1);
      //newRay->setSweepNumber(s);
      //newRay->setRayNumber(r); // rayNum);
        
      //      const string name = "VEL";
      //const string units = "m/s"; 
      Radx::si16 missingValue = -999;
      //      const Radx::si16 *data = &rawData[0];
      double scale = 1.0;
      double offset = 0.0;
      bool isLocal = false;

      int idx;
      int s = newRay->getSweepNumber();
      idx = s*20 + (rayNum%nRays)*nGates;   
      RadxField *field1 = newRay->addField("VEL_UNF", "m/s", nGates, missingValue, &newData[idx], scale, offset, isLocal);
      idx += 50;
      RadxField *field2 = newRay->addField("DBZ_UNF", "dB", nGates, missingValue, &newData[idx], scale, offset, isLocal);

      // to avoid this warning ...
      // WARNING - Range geom has not been set on ray
      //double startRangeKm = 3.0;
      //double gateSpacingKm = 5.0;
      //newRay->setRangeGeom(startRangeKm, gateSpacingKm);
      // radxVol->addRay(newRay);
      rayNum += 1;
    }
    //}

  radxVol->loadFieldsFromRays(); // moves data from ray fields to volumes  

  cout << " **********  unfolded ******* " << endl;
  
  radxVol->printWithFieldData(cout); 
  
  RadxFile outFile;
  outFile.writeToPath(*radxVol, "/Users/brenda/git/lrose-test/libs/Radx/createRadxVolumeDeNovo.nc");

  //EXPECT_EQ(1, timeList.getMode());
  //EXPECT_EQ(RadxTimeList::MODE_FIRST, timeList.getMode());
}

  /* tests for Timelist

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
*/
}  // namespace

