
#include "FourDD.hh"
#include "gtest/gtest.h"

namespace {

  // TODO: consider making a constructor with most of
  // these parameters set to default values
  /*
  FourDD fourDD(bool debug,
		char *sounding_url,
		float sounding_look_back,
		float wind_alt_min,
		float wind_alt_max,
		float avg_wind_u,
		float avg_wind_v,
		bool prep,
		bool filt,
		bool output_soundVol,
		float max_shear,
		int sign,
		int del_num_bins,
		bool no_dbz_rm_rv,
		float low_dbz,
		float high_dbz,
		float angle_variance,
		float comp_thresh,
		float comp_thresh2,
		bool strict_first_pass,
		int max_count,
		float ck_val,
		int proximity,
		int min_good,
		float std_thresh,
		float epsilon);
  */

  int maxSweeps_simple = 1;
  Volume *velocity = Rsl::new_volume(maxSweeps_simple);
  Volume *lastVolume = Rsl::new_volume(maxSweeps_simple);
  Volume *soundVolume = Rsl::new_volume(maxSweeps_simple);

  /*
  TEST(FourDD, InitialDealiasing_EverythingWorks) {
    FourDD fourDD;
    int maxSweeps = 1;
    Volume *velocity = Rsl::new_volume(maxSweeps);
    velocity->h.missing = -9.0;
    fourDD.InitialDealiasing();
    //    EXPECT_EQ(-9.0, fourDD.getMissingValue(velocity));
  }

  TEST(FourDD, InitialDealiasing_FirstPassSpatialContinuity_AllMissing) {
    FourDD fourDD;
    int maxSweeps = 1;
    Volume *velocity = Rsl::new_volume(maxSweeps);
    velocity->h.missing = -9.0;
    // TODO: make copy of velocity to original
    fourDD.FirstPassSpatialContinuity(STATE, original, velocity,  sweepIndex, del_num_bins, pfraction);
    //    EXPECT_EQ(-9.0, fourDD.getMissingValue(velocity));
  }

  TEST(FourDD, InitialDealiasing_FirstPassSpatialContinuity_NoMissing) {
    FourDD fourDD;
    int maxSweeps = 1;
    Volume *velocity = Rsl::new_volume(maxSweeps);
    velocity->h.missing = -9.0;
    // TODO: make copy of velocity to original
    fourDD.FirstPassSpatialContinuity(STATE, original, velocity,  sweepIndex, del_num_bins, pfraction);
    //    EXPECT_EQ(-9.0, fourDD.getMissingValue(velocity));
  }

  TEST(FourDD, InitialDealiasing_UnfoldUsingWindow) {
    FourDD fourDD;
    int maxSweeps = 1;
    Volume *velocity = Rsl::new_volume(maxSweeps);
    velocity->h.missing = -9.0;
    // TODO: make copy of velocity to original
    fourDD.UnfoldRemoteBinsOrUnsuccessfulBinsUsingWindow(
	       STATE, original, velocity,  sweepIndex, del_num_bins, pfraction);
    //    EXPECT_EQ(-9.0, fourDD.getMissingValue(velocity));
  }


  TEST(FourDD, InitialDealiasing_SecondPassSoundVolumeOnly) {
    FourDD fourDD;
    int maxSweeps = 1;
    Volume *velocity = Rsl::new_volume(maxSweeps);
    velocity->h.missing = -9.0;
    // TODO: make copy of velocity to original
    fourDD.SecondPassSoundVolumeOnly(STATE, original, velocity,  sweepIndex, del_num_bins, fraction2, pfraction);
    //    EXPECT_EQ(-9.0, fourDD.getMissingValue(velocity));
  }

  */
  TEST(FourDD, Unfold_negative) {
    FourDD fourDD;
    float foldedValue = 8;
    float referenceValue = -19;
    int max_count = 3;
    float NyqVelocity = 8;
    EXPECT_EQ(-24.0, fourDD.Unfold(foldedValue, referenceValue, max_count, NyqVelocity));
  }

  TEST(FourDD, Unfold_positive) {
    FourDD fourDD;
    float foldedValue = -3;
    float referenceValue = 23;
    int max_count = 3;
    float NyqVelocity = 8;
    EXPECT_EQ(29.0, fourDD.Unfold(foldedValue, referenceValue, max_count, NyqVelocity));
  }

  TEST(FourDD, Unfold_max_count_exceeded) {
    FourDD fourDD;
    float foldedValue = 8;
    float referenceValue = -19;
    int max_count = 1;
    float NyqVelocity = 8;
    EXPECT_EQ(-8.0, fourDD.Unfold(foldedValue, referenceValue, max_count, NyqVelocity));
  }

  TEST(FourDD, Unfold_max_count_0) {
    FourDD fourDD;
    float foldedValue = 2;
    float referenceValue = -19;
    int max_count = 0;
    float NyqVelocity = 8;
    EXPECT_EQ(2.0, fourDD.Unfold(foldedValue, referenceValue, max_count, NyqVelocity));
  }

  /*
  TEST(FourDD, AssessNeighborhood) {
    FourDD fourDD;
    int maxSweeps = 1;
    int nbins = 3;
    int nrays = 3;

    float nbins1[] = {-10.0, -8.0, -7.0};
    float nbins2[] = {  4.0, 2.0,  -3.0};
    float nbins3[] = {  1.0,-2.0, -19.0};


    Volume *velocity = Rsl::new_volume(maxSweeps);
    velocity->sweeps[0] = Rsl::new_sweep(nrays);
    for (int r=0; r<nrays; r++) {
      velocity->sweeps[0]->rays[r] = Rsl::new_ray(nbins);
      velocity->sweeps[0]->rays[r]->h.binDataAllocated = true;
    }
    velocity->sweeps[0]->rays[0] = nbins1;
    velocity->sweeps[0]->rays[1] = nbins2;
    velocity->sweeps[0]->rays[2] = nbins3;

    float foldedValue = 2;
    float referenceValue = -19;
    int max_count = 0;
    float NyqVelocity = 8;
    short **STATE = fourDD.CreateSTATE(velocity);
    Volume *rvVolume;
    int sweepIndex;
    int currIndex;
    int i;
    float foldedValue;
    float pfraction;
    float NyqVelocity = 10.0;
    int *nWithinNyquist; 
    int *nOutsideNyquist;
    int *nPositiveFolds;
    int *nNegativeFolds;
    bool *noHope;

      
    fourDD.AssessNeighborhood2(STATE, rvVolume, sweepIndex, currIndex, i,
			       val,
			       pfraction, NyqVelocity,
			       &in, &out, &numpos, &numneg, &noHope);
			       // foldedValue, referenceValue, max_count, NyqVelocity);

    fourDD.DestroySTATE(STATE, nbins);
    // Rsl::free_volume(velocity);

    EXPECT_EQ(2.0, nWithinNyquist);
    EXPECT_EQ(2.0, nOutsideNyquist);
    EXPECT_EQ(2.0, nPositiveFolds);
    EXPECT_EQ(2.0, nNegativeFolds);
    EXPECT_EQ(false, noHope);

  }
  */

  TEST(FourDD, AssessNeighborhood_All_TBD) {
    FourDD fourDD;
    int maxSweeps = 1;
    int nbins = 3;
    int nrays = 3;
    
    float nbins1[] = {-10.0, -8.0, -7.0};
    float nbins2[] = {  4.0, 2.0,  -3.0};
    float nbins3[] = {  1.0,-2.0, -19.0};

    Volume *velocity = Rsl::new_volume(maxSweeps);
    
    velocity->sweep[0] = Rsl::new_sweep(nrays);
    for (int r=0; r<nrays; r++) {
      velocity->sweep[0]->ray[r] = Rsl::new_ray(nbins);
      velocity->sweep[0]->ray[r]->h.binDataAllocated = true;
    }
    
    velocity->sweep[0]->ray[0]->range = nbins1;
    velocity->sweep[0]->ray[1]->range = nbins2;
    velocity->sweep[0]->ray[2]->range = nbins3;

    float foldedValue = 2;
    float NyqVelocity = 10;
    int sweepIndex = 0;
    int rayIndex = 1;
    int binIdx = 1;
    float pfraction = 1.0;
    int nWithinNyquist; 
    int nOutsideNyquist;
    int nPositiveFolds;
    int nNegativeFolds;
    bool noHope;
    int del_num_bins = 0;

    short **STATE = fourDD.CreateSTATE(velocity, FourDD::TBD);
    fourDD.AssessNeighborhood2(STATE, velocity, sweepIndex, rayIndex, binIdx,
			       del_num_bins, foldedValue,
			       pfraction, NyqVelocity,
			       &nWithinNyquist, &nOutsideNyquist, &nPositiveFolds, &nNegativeFolds, &noHope);

    fourDD.DestroySTATE(STATE, nbins);

    EXPECT_EQ(0, nWithinNyquist);
    EXPECT_EQ(0, nOutsideNyquist);
    EXPECT_EQ(0, nPositiveFolds);
    EXPECT_EQ(0, nNegativeFolds);
    EXPECT_EQ(false, noHope);
  }

  TEST(FourDD, AssessNeighborhood_Mixed_States) {
    FourDD fourDD;
    int maxSweeps = 1;
    int nbins = 3;
    int nrays = 3;
    
    float binsRay1[] = {-10.0, -8.0, -7.0};  // out/neg, out/== , in/
    float binsRay2[] = {  4.0, 2.0,  -3.0};  //  in/   ,  X     , in/
    float binsRay3[] = {  1.0,20.0, -19.0};  //  in/   , out/pos, out/neg

    Volume *velocity = Rsl::new_volume(maxSweeps);
    
    velocity->sweep[0] = Rsl::new_sweep(nrays);
    for (int r=0; r<nrays; r++) {
      velocity->sweep[0]->ray[r] = Rsl::new_ray(nbins);
      velocity->sweep[0]->ray[r]->h.binDataAllocated = true;
    }
    
    velocity->sweep[0]->ray[0]->range = binsRay1;
    velocity->sweep[0]->ray[1]->range = binsRay2;
    velocity->sweep[0]->ray[2]->range = binsRay3;

    float foldedValue = 2;
    float NyqVelocity = 10;
    int sweepIndex = 0;
    int rayIndex = 1;
    int binIdx = 1;
    float pfraction = 1.0;
    int nWithinNyquist; 
    int nOutsideNyquist;
    int nPositiveFolds;
    int nNegativeFolds;
    bool noHope;
    int del_num_bins = 0;

    short **STATE = fourDD.CreateSTATE(velocity, FourDD::DEALIASED);
    // STATE [bin][ray]
    STATE[1][0] = FourDD::TBD;
    STATE[2][1] = FourDD::MISSING;

    fourDD.AssessNeighborhood2(STATE, velocity, sweepIndex, rayIndex, binIdx,
			       del_num_bins, foldedValue,
			       pfraction, NyqVelocity,
			       &nWithinNyquist, &nOutsideNyquist, &nPositiveFolds, &nNegativeFolds, &noHope);

    fourDD.DestroySTATE(STATE, nbins);

    EXPECT_EQ(3, nWithinNyquist);
    EXPECT_EQ(3, nOutsideNyquist);
    EXPECT_EQ(1, nPositiveFolds);
    EXPECT_EQ(2, nNegativeFolds);
    EXPECT_EQ(false, noHope);
  }



  TEST(FourDD, AssessNeighborhood_Mixed_States_bin_last) {
    FourDD fourDD;
    int maxSweeps = 1;
    int nbins = 3;
    int nrays = 3;
    
    float binsRay1[] = {-10.0, -8.0, -7.0};  // out/neg, TBD    , in/
    float binsRay2[] = {  4.0, 2.0,  -3.0};  //  in/   , in/    ,  X
    float binsRay3[] = {  1.0,20.0, -19.0};  //  in/   , out/pos, MISSING

    Volume *velocity = Rsl::new_volume(maxSweeps);
    
    velocity->sweep[0] = Rsl::new_sweep(nrays);
    for (int r=0; r<nrays; r++) {
      velocity->sweep[0]->ray[r] = Rsl::new_ray(nbins);
      velocity->sweep[0]->ray[r]->h.binDataAllocated = true;
    }
    
    velocity->sweep[0]->ray[0]->range = binsRay1;
    velocity->sweep[0]->ray[1]->range = binsRay2;
    velocity->sweep[0]->ray[2]->range = binsRay3;

    float foldedValue = -3;
    float NyqVelocity = 10;
    int sweepIndex = 0;
    int rayIndex = 1;
    int binIdx = 2;
    float pfraction = 1.0;
    int nWithinNyquist; 
    int nOutsideNyquist;
    int nPositiveFolds;
    int nNegativeFolds;
    bool noHope;
    int del_num_bins = 0;

    short **STATE = fourDD.CreateSTATE(velocity, FourDD::DEALIASED);
    // STATE [bin][ray]
    STATE[1][0] = FourDD::TBD;
    STATE[2][2] = FourDD::MISSING;

    fourDD.AssessNeighborhood2(STATE, velocity, sweepIndex, rayIndex, binIdx,
			       del_num_bins, foldedValue,
			       pfraction, NyqVelocity,
			       &nWithinNyquist, &nOutsideNyquist, &nPositiveFolds, &nNegativeFolds, &noHope);

    fourDD.DestroySTATE(STATE, nbins);

    EXPECT_EQ(2, nWithinNyquist);
    EXPECT_EQ(1, nOutsideNyquist);
    EXPECT_EQ(1, nPositiveFolds);
    EXPECT_EQ(0, nNegativeFolds);
    EXPECT_EQ(false, noHope);
  }




  TEST(FourDD, AssessNeighborhood_All_DEALIASED) {
    FourDD fourDD;
    int maxSweeps = 1;
    int nbins = 3;
    int nrays = 3;
    
    float nbins1[] = {-10.0, -8.0, -7.0};  // out/neg, out/== , in/
    float nbins2[] = {  4.0, 2.0,  -3.0};  //  in/   ,  X     , in/
    float nbins3[] = {  1.0,-2.0, -19.0};  //  in/   ,  in/   , out/neg

    Volume *velocity = Rsl::new_volume(maxSweeps);
    
    velocity->sweep[0] = Rsl::new_sweep(nrays);
    for (int r=0; r<nrays; r++) {
      velocity->sweep[0]->ray[r] = Rsl::new_ray(nbins);
      velocity->sweep[0]->ray[r]->h.binDataAllocated = true;
    }
    
    velocity->sweep[0]->ray[0]->range = nbins1;
    velocity->sweep[0]->ray[1]->range = nbins2;
    velocity->sweep[0]->ray[2]->range = nbins3;

    float foldedValue = 2;
    float NyqVelocity = 10;
    int sweepIndex = 0;
    int rayIndex = 1;
    int binIdx = 1;
    float pfraction = 1.0;
    int nWithinNyquist; 
    int nOutsideNyquist;
    int nPositiveFolds;
    int nNegativeFolds;
    bool noHope;
    int del_num_bins = 0;

    short **STATE = fourDD.CreateSTATE(velocity, FourDD::DEALIASED);
    fourDD.AssessNeighborhood2(STATE, velocity, sweepIndex, rayIndex, binIdx,
			       del_num_bins, foldedValue,
			       pfraction, NyqVelocity,
			       &nWithinNyquist, &nOutsideNyquist, &nPositiveFolds, &nNegativeFolds, &noHope);

    fourDD.DestroySTATE(STATE, nbins);

    EXPECT_EQ(5, nWithinNyquist);
    EXPECT_EQ(3, nOutsideNyquist);
    EXPECT_EQ(0, nPositiveFolds);
    EXPECT_EQ(2, nNegativeFolds);
    EXPECT_EQ(false, noHope);
  }


  TEST(FourDD, AssessNeighborhood_noHope) {
    FourDD fourDD;
    int maxSweeps = 1;
    int nbins = 3;
    int nrays = 3;

    Volume *velocity = Rsl::new_volume(maxSweeps);
    
    velocity->sweep[0] = Rsl::new_sweep(nrays);
    for (int r=0; r<nrays; r++) {
      velocity->sweep[0]->ray[r] = Rsl::new_ray(nbins);
    }

    float foldedValue = 2;
    float NyqVelocity = 10;
    int sweepIndex = 0;
    int rayIndex = 1;
    int binIdx = 1;
    float pfraction = .9;
    int nWithinNyquist; 
    int nOutsideNyquist;
    int nPositiveFolds;
    int nNegativeFolds;
    bool noHope;
    int del_num_bins = 0;

    // create STATE with only 1 TBD or DEALIASED; all the rest are MISSING, or UNSUCCESSFUL
    short **STATE = fourDD.CreateSTATE(velocity, FourDD::MISSING);
    fourDD.AssessNeighborhood2(STATE, velocity, sweepIndex, rayIndex, binIdx,
			       del_num_bins, foldedValue,
			       pfraction, NyqVelocity,
			       &nWithinNyquist, &nOutsideNyquist, &nPositiveFolds, &nNegativeFolds, &noHope);

    fourDD.DestroySTATE(STATE, nbins);

    EXPECT_EQ(0, nWithinNyquist);
    EXPECT_EQ(0, nOutsideNyquist);
    EXPECT_EQ(0, nPositiveFolds);
    EXPECT_EQ(0, nNegativeFolds);
    EXPECT_EQ(true, noHope);
  }



  TEST(FourDD, getMissingValue) {
    FourDD fourDD;
    int maxSweeps = 1;
    Volume *velocity = Rsl::new_volume(maxSweeps);
    velocity->h.missing = -9.0;
    EXPECT_EQ(-9.0, fourDD.getMissingValue(velocity));
  }

  /*
  // expect an exception here ...
  TEST(FourDD, getMissingValue_NULL) {
    FourDD fourDD;
    Volume *vel = NULL;
    EXPECT_EQ(-9.0, fourDD.getMissingValue(vel));
  }


  TEST(FourDD, findRay_NULL) {
    FourDD fourDD;
    Volume *velocity = NULL;
    velocity->h.missing = -9.0;
    EXPECT_EQ(-9.0, fourDD.findRay(velocity, velocity, 0, 0, 0));
  }

  TEST(FourDD, Filter3x3_NULL) {
    FourDD fourDD;
    float missingVal = -999e+33;
    Volume *velocity = NULL;
    velocity->h.missing = -9.0;
    EXPECT_EQ(-9.0, fourDD.Filter3x3(velocity, 0, missingVal));
  }
  */
  /*
  TEST(FourDD, Filter3x3_binTooBig) {
    FourDD fourDD;
    float missingVal = -999e+33;
    Volume *velocity = simpleVolume;
    velocity->h.missing = missingVal;
    int bin_i = simpleVolume->nbins+1;
    EXPECT_EQ(-9.0, fourDD.Filter3x3(velocity, bin_i, missingVal));
  }

  TEST(FourDD, Filter3x3_binGood) {
    FourDD fourDD;
    float missingVal = -999e+33;
    Volume *velocity = simpleVolume;
    velocity->h.missing = missingVal;
    int bin_i = simpleVolume->nbins-11;
    EXPECT_EQ(-9.0, fourDD.Filter3x3(velocity, bin_i, missingVal));
  }

  TEST(FourDD, AssessNeighborhood_HappyDay) {
    FourDD fourDD;
    float missingVal = -999e+33;
    Volume *velocity = simpleVolume;
    velocity->h.missing = missingVal;
    int bin_i = 1;
    short **STATE;
    int currIndex; 
    int numRays;
    int numberOfDealiasedNeighbors;
    int numberOfTbdNeighbors;
    int binindex[3]; 
    int rayindex[3];

    // TODO: initialize STATE; maybe make this a global variable?

    fourDD.AssessNeighborhood(
              STATE, currIndex, bin_i, numRays,
	      &numberOfDealiasedNeighbors, &numberOfTbdNeighbors,
	      binindex, rayindex);

    EXPECT_EQ(9, numberOfDealiasedNeighbors);
    EXPECT_EQ(9, numberOfTbdNeighbors);
    EXPECT_EQ(9, binindex[0]); // TODO: ...
    EXPECT_EQ(9, rayindex[0]);

  }


  TEST(FourDD, window_HappyDay) {
    FourDD fourDD;
    float missingVal = -999e+33;
    Volume *rvVolume = simpleVolume;
    velocity->h.missing = missingVal;
    int bin_i = simpleVolume->maxBins-11;
    
    int sweepIndex;
    int startray;
    int endray;
    int firstbin;
    int lastbin;
    float std;
    float missingVal; 
    unsigned short success;

    EXPECT_EQ(-9.0, fourDD.window(rvVolume, sweepIndex, startray,
	  endray, firstbin, lastbin, std,
	  missingVal, &success));

  }
  */


} // namespace
