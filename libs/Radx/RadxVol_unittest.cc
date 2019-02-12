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
  // int nFields = 2;
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

  // So, is the ray the base element? (YES) i.e. create rays first,
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
      //      const Radx::si16 *data = &rawData[0];
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

  // check for some expected values ...
  // Check the new fields because their values are dependent on the original values
  //   wait, field1 and field2 are NOT defined anymore! 
  //
  RadxField *testField1 = radxVol->getField("VEL_UNF");
  Radx::si16 *testData = testField1->getDataSi16();

  EXPECT_EQ(40, testField1->getNPoints());

  for (size_t i=0; i<testField1->getNPoints(); i++) {
    int expectedValue = i * -1;
    EXPECT_EQ(expectedValue, testData[i]);
  }

  RadxField *testField2 = radxVol->getField("DBZ_UNF");
  testData = testField2->getDataSi16();

  EXPECT_EQ(40, testField2->getNPoints());

  for (size_t i=0; i<testField2->getNPoints(); i++) {
    int expectedValue = (i+50) * -1;
    EXPECT_EQ(expectedValue, testData[i]);
  }

}

}  // namespace

