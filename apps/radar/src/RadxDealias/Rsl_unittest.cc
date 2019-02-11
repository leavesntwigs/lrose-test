#include <limits.h>
#include <Rsl.hh>
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


TEST(RSL, copy_volume) {

  int nsweeps = 3;
  int nrays = 2;
  int nbins = 5;

  int totalDataPoints = nbins * nrays * nsweeps;
  Range *data = (Range *) malloc(sizeof(Range) * totalDataPoints);
  for (int d=0; d<totalDataPoints; d++)
    data[d] = (Range) d;   

  Volume *volume = Rsl::new_volume(nsweeps);

  Sweep **sweeps = volume->sweep;
  for (int i=0; i<nsweeps; i++) {
    sweeps[i] = Rsl::new_sweep(nrays);
    Ray **rays = sweeps[i]->ray;
    for (int r=0; r<nrays; r++) {;
      rays[r] = Rsl::new_ray(nbins);
	// remember, we are not allocating space for the data;
	// instead we are using pointers to the data
      int index = (i*nrays*nbins) + r*nbins;
      printf("index = %d for %d sweeps, %d rays \n", index, i, r);
      rays[r]->range = &data[index];
    }
  }

  Rsl::print_volume(volume);

  // copy the volume
  Volume *copy = Rsl::copy_volume(volume);

  Rsl::print_volume(copy);


  // compare the copy and the original
  EXPECT_EQ(copy->h.nsweeps, volume->h.nsweeps);
  EXPECT_EQ(copy->h.nsweeps, nsweeps);
  EXPECT_NE(volume->sweep, nullptr);
  EXPECT_NE(copy->sweep, nullptr);

  Sweep **sweep = volume->sweep;
  Sweep **sweepCopy = copy->sweep;
  for (int i = 0; i < volume->h.nsweeps; i++) {
    EXPECT_EQ(volume->sweep[i]->h.nrays, copy->sweep[i]->h.nrays);
    EXPECT_EQ(copy->sweep[i]->h.nrays, nrays);
    EXPECT_NE(volume->sweep[i]->ray, nullptr);
    EXPECT_NE(copy->sweep[i]->ray, nullptr);
    Ray **ray = sweep[i]->ray;
    Ray **rayCopy = sweepCopy[i]->ray;
    //cerr << " THERE ARE " << volume->sweep[i]->h.nrays << " RAYS" << endl;
    int nRays = volume->sweep[i]->h.nrays;
    //cerr << " THERE ARE " << nRays << " RAYS" << endl;

    for (int r = 0; r < nRays; r++) {
      //cerr << "==> i = " << i << "; r = " << r << endl;
      EXPECT_EQ(volume->sweep[i]->ray[r]->h.nbins, copy->sweep[i]->ray[r]->h.nbins);
      EXPECT_EQ(copy->sweep[i]->ray[r]->h.nbins, nbins);
      EXPECT_NE(volume->sweep[i]->ray[r]->range, nullptr);
      EXPECT_NE(copy->sweep[i]->ray[r]->range, nullptr);
      for (int b=0; b < volume->sweep[i]->ray[r]->h.nbins; b++) {
	//cerr << "I'm in the danger zone";
        //cerr << "==> i = " << i << "; r = " << r << "; b = " << b << endl;
        EXPECT_EQ(volume->sweep[i]->ray[r]->range[b], copy->sweep[i]->ray[r]->range[b]);
      }
    
    }
    
  }

  Rsl::free_volume(volume);
  Rsl::free_volume(copy);
  free(data);
}




TEST(RSL, DZ_INVF_just_right) {
  Range x = Rsl::DZ_INVF(32.15);  
  //cout << "Range is " << x << endl;
  EXPECT_EQ(32, x);
}

  // need to catch an exception here 
TEST(RSL, DZ_INVF_negative) {
  try {
    Range x = Rsl::DZ_INVF(-32.15);
    FAIL() << "Expected std::out_of_range" << " on value " << x;  
  } catch(std::out_of_range const & err) {
    EXPECT_EQ(err.what(),std::string("value too small for conversion to 2-byte unsigned int"));
  }
  catch(...) {
    FAIL() << "Expected std::out_of_range";
  }
}

TEST(RSL, DZ_INVF_too_small) {
  float too_small = 1E-37;
  Range x = Rsl::DZ_INVF(too_small);  
  //cout << "Range is " << x << endl;
  EXPECT_EQ(0, x);
}

  // need to catch an exception here 
TEST(RSL, DZ_INVF_too_big) {
  try {
    float too_big = 1E+37;
    Range x = Rsl::DZ_INVF(too_big);
    FAIL() << "Expected std::out_of_range" << " on value " << x;  
  } catch(std::out_of_range const & err) {
    EXPECT_EQ(err.what(),std::string("value too large for conversion to 2-byte unsigned int"));
  }
  catch(...) {
    FAIL() << "Expected std::out_of_range";
  }
}

 
  // Test the memory allocation and free  
  /*
Dsr2Radar.cc:  radar = Rsl::new_radar(numFields + 1);
Dsr2Radar.cc:      Volume *volume =  Rsl::new_volume(nSweepsVol); 
Dsr2Radar.cc:  volume->h.type_str = new char[13];
Dsr2Radar.cc:  volume->h.type_str = new char[9];
Dsr2Radar.cc:  volume->h.type_str = new char[9];
Dsr2Radar.cc:      Sweep *sweep = Rsl::new_sweep(nbeamsTilt);
Dsr2Radar.cc:      Ray *ray = Rsl::new_ray(numGates);
Dsr2Radar.cc:  fieldRays = new vector<Ray*>[numFields];
Dsr2Radar.cc:  fieldSweeps = new vector<Sweep*>[numFields];
  */

TEST(RSL, alloc_free_radar) {

  int numFields = 1;
  int nSweepsVol = 3;
  // fill trmm_rsl structure for James Dealias
  Radar *radar = Rsl::new_radar(numFields + 1);
  Volume *volume = Rsl::new_volume(nSweepsVol);
  radar->v[0] = volume;
  // leave some arrays ragged
  
  Rsl::free_radar(radar);
  
  // fill RadxVol structure for RadxDealias

  // run the operation

}

  /*
TEST(FourDD, findFirstTimeInDataSet) {
  FourDD timeList;
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

