
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

  TEST(FourDD, AssessNeighborhood_Mixed_States_bin0) {
    FourDD fourDD;
    int maxSweeps = 1;
    int nbins = 3;
    int nrays = 3;
    
    float binsRay1[] = {-10.0, -8.0, -7.0};  //  in/   , TBD    , in/
    float binsRay2[] = {  4.0, 2.0,  -3.0};  //  X     , in/    ,  in/
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
    int binIdx = 0;
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

    EXPECT_EQ(3, nWithinNyquist);
    EXPECT_EQ(1, nOutsideNyquist);
    EXPECT_EQ(1, nPositiveFolds);
    EXPECT_EQ(0, nNegativeFolds);
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

  // wrap right == ray+1
  TEST(FourDD, AssessNeighborhood_Mixed_States_bin_last_wrap_right) {
    FourDD fourDD;
    int maxSweeps = 1;
    int nbins = 3;
    int nrays = 3;
    
    //                                          -------
    float binsRay1[] = {-10.0, -8.0, -7.0};  // out/neg, TBD    , in/
    float binsRay2[] = {  4.0, 2.0,  -3.0};  //  in/   , in/    , MISSING
    float binsRay3[] = {  1.0,20.0, -19.0};  //  in/   , out/pos,  X

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
    int rayIndex = 2;
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
    STATE[2][1] = FourDD::MISSING;

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

  // wrap left == ray-1
  TEST(FourDD, AssessNeighborhood_Mixed_States_bin0_wrap_left) {
    FourDD fourDD;
    int maxSweeps = 1;
    int nbins = 3;
    int nrays = 3;
    //                                                           -----
    float binsRay1[] = {-10.0, -8.0, -7.0};  //   X    , TBD    , in/
    float binsRay2[] = {  4.0, 2.0,  -3.0};  //  in/   , in/    , in/
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
    int rayIndex = 0;
    int binIdx = 0;
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

    EXPECT_EQ(3, nWithinNyquist);
    EXPECT_EQ(1, nOutsideNyquist);
    EXPECT_EQ(1, nPositiveFolds);
    EXPECT_EQ(0, nNegativeFolds);
    EXPECT_EQ(false, noHope);
  }


  // wrap left == ray-1
  TEST(FourDD, AssessNeighborhood_Mixed_States_bin0_wrap_left4) {
    FourDD fourDD;
    int maxSweeps = 1;
    int nbins = 3;
    int nrays = 4;
    //                                                           vvvv
    float binsRay1[] = {-10.0, -8.0, -7.0};   //   X    , TBD    , in/
    float binsRay2[] = {  4.0,  2.0,  -3.0};  //  in/   , in/    , in/
    float binsRay3[] = {  1.0, 20.0, -19.0};  //  in/   , out/pos, MISSING <---
    float binsRay4[] = {  7.0,-30.0,   0.0};  // out/== , out/neg, in/

    Volume *velocity = Rsl::new_volume(maxSweeps);
    
    velocity->sweep[0] = Rsl::new_sweep(nrays);
    for (int r=0; r<nrays; r++) {
      velocity->sweep[0]->ray[r] = Rsl::new_ray(nbins);
      velocity->sweep[0]->ray[r]->h.binDataAllocated = true;
    }
    
    velocity->sweep[0]->ray[0]->range = binsRay1;
    velocity->sweep[0]->ray[1]->range = binsRay2;
    velocity->sweep[0]->ray[2]->range = binsRay3;
    velocity->sweep[0]->ray[3]->range = binsRay4;

    float foldedValue = -3;
    float NyqVelocity = 10;
    int sweepIndex = 0;
    int rayIndex = 0;
    int binIdx = 0;
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
    EXPECT_EQ(2, nOutsideNyquist);
    EXPECT_EQ(0, nPositiveFolds);
    EXPECT_EQ(1, nNegativeFolds);
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
  */


  TEST(FourDD, findRay_NULL) {
    FourDD fourDD;
    Volume *velocity = NULL;
    // velocity->h.missing = -9.0;
    EXPECT_EQ(-9.0, fourDD.findRay(velocity, velocity, 0, 0, 0));
  }

  TEST(FourDD, findRay_HappyDay_intraVolume) {
    FourDD fourDD;
    float missingVal = -999e+33;
    int maxSweeps = 4;
    int nbins = 3;
    int nrays = 3;

    Volume *velocity = Rsl::new_volume(maxSweeps);
 
    for (int s=0; s<maxSweeps; s++) {   
      velocity->sweep[s] = Rsl::new_sweep(nrays);
      for (int r=0; r<nrays; r++) {
        velocity->sweep[s]->ray[r] = Rsl::new_ray(nbins);
        velocity->sweep[s]->ray[r]->h.binDataAllocated = true;
        // Note: the azimuth need to be the same for each sweep
        velocity->sweep[s]->ray[r]->h.azimuth = 10.0 + (120.0*r);
      }
    }

    velocity->h.missing = missingVal;

    // int binIdx = 1;
    int rayIdx = 1;
    int sweepIdx1 = 0;
    int sweepIdx2 = 2;

    EXPECT_EQ(rayIdx, fourDD.findRay(velocity, velocity, sweepIdx1, sweepIdx2, rayIdx));
  }

  TEST(FourDD, findRay_HappyDay_interVolume) {
    FourDD fourDD;
    float missingVal = -999e+33;
    int maxSweeps = 4;
    int nbins = 3;
    int nrays = 3;

    Volume *velocity = Rsl::new_volume(maxSweeps);
 
    for (int s=0; s<maxSweeps; s++) {   
      velocity->sweep[s] = Rsl::new_sweep(nrays);
      for (int r=0; r<nrays; r++) {
        velocity->sweep[s]->ray[r] = Rsl::new_ray(nbins);
        // Note: the azimuth need to be the same for each sweep
        velocity->sweep[s]->ray[r]->h.azimuth = 10.0 + (120.0*r);
      }
    }
    // 10, 130, 250  -->  370

    Volume *sounding = Rsl::new_volume(maxSweeps);

    int nRaysSounding = nrays + 2;
    float raySpacing = 360.0/ (float) nRaysSounding;
    for (int s=0; s<maxSweeps; s++) {   
      sounding->sweep[s] = Rsl::new_sweep(nRaysSounding);
      for (int r=0; r<nRaysSounding; r++) {
        sounding->sweep[s]->ray[r] = Rsl::new_ray(nbins);
        // Note: the azimuth need to be the same for each sweep
        sounding->sweep[s]->ray[r]->h.azimuth = 0.0 + (raySpacing*r);
      }
    }
    // 0, 72, 144,  216, 288 -->  360

    velocity->h.missing = missingVal;

    //int binIdx = 1;
    int rayIdx = 1;
    int sweepIdx1 = 0;
    int sweepIdx2 = 2;

    // find ray in sounding, closest to 130.0 degrees
    int closestRayIdx = fourDD.findRay(velocity, sounding, sweepIdx1, sweepIdx2, rayIdx);
    EXPECT_EQ(2, closestRayIdx);
    EXPECT_EQ(130.0, velocity->sweep[sweepIdx1]->ray[rayIdx]->h.azimuth);
    EXPECT_EQ(144.0, sounding->sweep[sweepIdx2]->ray[closestRayIdx]->h.azimuth);
  }


  TEST(FourDD, findRay_HappyDay_interVolume_boundary_min) {
    FourDD fourDD;
    float missingVal = -999e+33;
    int maxSweeps = 4;
    int nbins = 3;
    int nrays = 3;

    Volume *velocity = Rsl::new_volume(maxSweeps);
 
    for (int s=0; s<maxSweeps; s++) {   
      velocity->sweep[s] = Rsl::new_sweep(nrays);
      for (int r=0; r<nrays; r++) {
        velocity->sweep[s]->ray[r] = Rsl::new_ray(nbins);
        // Note: the azimuth need to be the same for each sweep
        velocity->sweep[s]->ray[r]->h.azimuth = 10.0 + (120.0*r);
      }
    }
    // 10, 130, 250  -->  370

    Volume *sounding = Rsl::new_volume(maxSweeps);

    int nRaysSounding = nrays + 2;
    float raySpacing = 360.0/ (float) nRaysSounding;
    for (int s=0; s<maxSweeps; s++) {   
      sounding->sweep[s] = Rsl::new_sweep(nRaysSounding);
      for (int r=0; r<nRaysSounding; r++) {
        sounding->sweep[s]->ray[r] = Rsl::new_ray(nbins);
        // Note: the azimuth need to be the same for each sweep
        sounding->sweep[s]->ray[r]->h.azimuth = 0.0 + (raySpacing*r);
      }
    }
    // 0, 72, 144,  216, 288 -->  360

    velocity->h.missing = missingVal;

    int rayIdx = 0;
    int sweepIdx1 = 0;
    int sweepIdx2 = 2;

    // find ray in sounding, closest to 130.0 degrees
    int closestRayIdx = fourDD.findRay(velocity, sounding, sweepIdx1, sweepIdx2, rayIdx);
    EXPECT_EQ(0, closestRayIdx);
    EXPECT_EQ(10.0, velocity->sweep[sweepIdx1]->ray[rayIdx]->h.azimuth);
    EXPECT_EQ(0.0, sounding->sweep[sweepIdx2]->ray[closestRayIdx]->h.azimuth);
  }


  TEST(FourDD, findRay_HappyDay_interVolume_boundary_max) {
    FourDD fourDD;
    float missingVal = -999e+33;
    int maxSweeps = 4;
    int nbins = 3;
    int nrays = 3;

    Volume *velocity = Rsl::new_volume(maxSweeps);
 
    for (int s=0; s<maxSweeps; s++) {   
      velocity->sweep[s] = Rsl::new_sweep(nrays);
      for (int r=0; r<nrays; r++) {
        velocity->sweep[s]->ray[r] = Rsl::new_ray(nbins);
        // Note: the azimuth need to be the same for each sweep
        velocity->sweep[s]->ray[r]->h.azimuth = 10.0 + (120.0*r);
      }
    }
    // 10, 130, 250  -->  370

    Volume *sounding = Rsl::new_volume(maxSweeps);

    int nRaysSounding = nrays + 2;
    float raySpacing = 360.0/ (float) nRaysSounding;
    for (int s=0; s<maxSweeps; s++) {   
      sounding->sweep[s] = Rsl::new_sweep(nRaysSounding);
      for (int r=0; r<nRaysSounding; r++) {
        sounding->sweep[s]->ray[r] = Rsl::new_ray(nbins);
        // Note: the azimuth need to be the same for each sweep
        sounding->sweep[s]->ray[r]->h.azimuth = 0.0 + (raySpacing*r);
      }
    }
    // 0, 72, 144,  216, 288 -->  360

    velocity->h.missing = missingVal;

    //int binIdx = 1;
    int rayIdx = nrays - 1;
    int sweepIdx1 = 0;
    int sweepIdx2 = 2;

    // find ray in sounding, closest to 130.0 degrees
    int closestRayIdx = fourDD.findRay(velocity, sounding, sweepIdx1, sweepIdx2, rayIdx);
    EXPECT_EQ(3, closestRayIdx);
    EXPECT_EQ(250.0, velocity->sweep[sweepIdx1]->ray[rayIdx]->h.azimuth);
    EXPECT_EQ(216.0, sounding->sweep[sweepIdx2]->ray[closestRayIdx]->h.azimuth);
  }

  TEST(FourDD, InitialDealiasing_HappyDay) {

    // TODO: need two sweeps in velocity for aboveValue, startingValue,
    // TODO: need prevValue, soundValue

    //    float data[] = {9, 2, -7, -12, -13, 10, 13, 9, -5, -5, 20, -13, 14, -11, -7, 17, 18, 1, 0, 2, -13, 10, 7, -18, 9, -2, 17, -13, -4, -4, -3, -8, 18, -5, -2, -12, 20, 8, -17, 6, 3, -17, 8, -16, 17, 18, 2, -18, -2, -6, 18, -4, -2, 14, 3, 19, 13, 2, 8, 18, 4, -8, -4, -13, 4, 20, -14, 17, 8, 3, -12, 5, 20, 19, 2, -4, -4, 14, -2, -9, -14, 17, -20, 8, 5, -18, 16, -20, 2, -9, -14, 16, 8, 11, 15, -16, 10, 5, 7, 3, -20, -10, 10, -10, -8, 4, -10, 6, 4, 6, -15, 4, 20, 13, -1, -1, 10, 14, -14, 10};
   
    float missingVal = -999e+33;

    int maxSweeps = 3;
    int nbins = 3;
    int nrays = 1;  // we'll need more rays for the spatial dealiasing
    int del_num_bins = 0;
    
    // data for original velocity volume; contains folded velocities
    float obins1[] = {-5, 20, -13};
    //float obins2[] = {14, -11, -7};
    //float obins3[] = {17, 18, 1};

    float obins4[] = {-13,   2, -7};
    //float obins5[] = {-12,   9, 10};
    //float obins6[] = { 13,   9, -5};

    float obins7[] = {0, 2, -13};
    //float obins8[] = {10, 7, -1};
    //float obins9[] = {8, 9, -2};

    // velocity data for previous volume; contains unfolded velocities
    // this is the direction we want to go
    // vary the Nyquist value to get closer and closer to desired velocity
    float pbins1[] = {-13, -13, -13};
    float missingValBins[] = {-999e+33, -999e+33, -999e+33};
    //float pbins3[] = {-13, -13, -13};

    // make original velocity volume
    Volume *velocity = Rsl::new_volume(maxSweeps);
    velocity->sweep[0] = Rsl::new_sweep(nrays);
    for (int r=0; r<nrays; r++) {
      velocity->sweep[0]->ray[r] = Rsl::new_ray(nbins);
      velocity->sweep[0]->ray[r]->h.binDataAllocated = true;
    }
    velocity->sweep[0]->ray[0]->range = obins1;
    //    velocity->sweep[0]->ray[1]->range = nbins2;
    //velocity->sweep[0]->ray[2]->range = nbins3;

    velocity->sweep[1]->ray[0]->range = obins4;
    //    velocity->sweep[1]->ray[1]->range = nbins5;
    //velocity->sweep[1]->ray[2]->range = nbins6;

    velocity->sweep[2]->ray[0]->range = obins7;
    //velocity->sweep[2]->ray[1]->range = nbins8;
    //velocity->sweep[2]->ray[2]->range = nbins9;
    velocity->h.missing = missingVal;

    // make previous velocity volume
    Volume *prevVelocity = Rsl::new_volume(maxSweeps);
    prevVelocity->sweep[0] = Rsl::new_sweep(nrays);
    for (int r=0; r<nrays; r++) {
      prevVelocity->sweep[0]->ray[r] = Rsl::new_ray(nbins);
      prevVelocity->sweep[0]->ray[r]->h.binDataAllocated = true;
    }
    prevVelocity->sweep[1]->ray[0]->range = pbins1;
    //prevVelocity->sweep[1]->ray[1]->range = pbins1;
    //prevVelocity->sweep[1]->ray[2]->range = pbins1;
    prevVelocity->h.missing = missingVal;

    // we do need azimuth info for findRay 
    for (int s=0; s<maxSweeps; s++) {   
      velocity->sweep[s] = Rsl::new_sweep(nrays);
      for (int r=0; r<nrays; r++) {
        velocity->sweep[s]->ray[r] = Rsl::new_ray(nbins);
        // Note: the azimuth need to be the same for each sweep
            velocity->sweep[s]->ray[r]->h.azimuth = 10.0 + (120.0*r);
        prevVelocity->sweep[s]->ray[r]->h.azimuth = 10.0 + (120.0*r);
      }
    }
    /*
    // 10, 130, 250  -->  370

    Volume *sounding = Rsl::new_volume(maxSweeps);

    int nRaysSounding = nrays + 2;
    float raySpacing = 360.0/ (float) nRaysSounding;
    for (int s=0; s<maxSweeps; s++) {   
      sounding->sweep[s] = Rsl::new_sweep(nRaysSounding);
      for (int r=0; r<nRaysSounding; r++) {
        sounding->sweep[s]->ray[r] = Rsl::new_ray(nbins);
        // Note: the azimuth need to be the same for each sweep
        sounding->sweep[s]->ray[r]->h.azimuth = 0.0 + (raySpacing*r);
      }
    }
    // 0, 72, 144,  216, 288 -->  360

    //    velocity->h.missing = missingVal;
    */

    FourDD fourDD;

    //  fill STATE info
    short **STATE = fourDD.CreateSTATE(velocity, FourDD::TBD);

    //  construct rvVolume; out param
    Volume *rvVolume = Rsl::new_volume(maxSweeps);
    rvVolume->sweep[0] = Rsl::new_sweep(nrays);
    for (int r=0; r<nrays; r++) {
      rvVolume->sweep[0]->ray[r] = Rsl::new_ray(nbins);
      rvVolume->sweep[0]->ray[r]->h.binDataAllocated = true;
    }
    rvVolume->sweep[0]->ray[0]->range = missingValBins;
    rvVolume->sweep[1]->ray[0]->range = missingValBins;
    rvVolume->sweep[2]->ray[0]->range = missingValBins;

    // need lastVolume or soundVolume, or both
    Volume *lastVolume = prevVelocity;  
    Volume *soundVolume = NULL;
    Volume *original = velocity;
    int sweepIndex = 1;  // start in the middle
    bool filt = false; // this is the 3x3 filtering
    float fraction = 0.25;  // how close do unfolded velocities need to be?

    // calls findRay, Unfold, DealiasVerticalAndTemporal ==> need sweep above
    //                                                   ==> need previous volume in time
    fourDD.InitialDealiasing(rvVolume, lastVolume, soundVolume,
                      original, sweepIndex, del_num_bins, STATE,
                      filt, fraction); 

    //    EXPECT_EQ(false);
    EXPECT_EQ(-13.0, rvVolume->sweep[1]->ray[0]->range[0]);
  }


  //   TEST(FourDD, prepVolume_NULL) {
  //   TEST(FourDD, prepVolume_high_low_dbz) {
  //   TEST(FourDD, prepVolume_yes_dbz_rm_rv) {
  //   TEST(FourDD, prepVolume_del_num_bins) {
  //   TEST(FourDD, prepVolume_manyDBZ_to_oneRV) {
  //
  TEST(FourDD, prepVolume_HappyDay) {
    FourDD fourDD;
    Volume* DBZVolume; 
    Volume* rvVolume; 
    int del_num_bins = 0;
    float missingVal = -999e+33;
    float low_dbz;
    float high_dbz;
    bool no_dbz_rm_rv = false;

    fourDD.prepVolume(DBZVolume, rvVolume, del_num_bins, missingVal,
               low_dbz, high_dbz, no_dbz_rm_rv);

    // test values of rvVolume for missingVal
    EXPECT_EQ(missingVal, rvVolume);
  }

  TEST(FourDD, DealiasVerticalAndTemporal_MissingValue) {
    FourDD fourDD;

    // in args
    float missingValue = -999e+33;
    float aboveValue = 0.0;
    float soundValue = 0.0;
    float startingValue = missingValue;
    float prevValue = 0.0;
    bool lastVolumeIsNull = true;
    float fraction = 0.25;
    float NyqVelocity = 10.0;
    int max_count = 3;
    bool strict_first_pass = false;

    // out args
    float unfoldedValue;
    bool successful = false;

    // find ray in sounding, closest to 130.0 degrees
    fourDD.TryToDealiasUsingVerticalAndTemporalContinuity(
            missingValue, aboveValue, soundValue, startingValue, prevValue,
            lastVolumeIsNull,
            fraction, NyqVelocity,
            strict_first_pass,
            max_count,
            &unfoldedValue, &successful);
    EXPECT_FALSE(successful);
    EXPECT_EQ(missingValue, unfoldedValue);
  }

  TEST(FourDD, DealiasVerticalAndTemporal_strict_first_pass) {
    FourDD fourDD;
    // unfold startingValue until within prevValue +/- 2 
    // aboveValue-unfolded_prevValue < .25 * 8 = 2
    // soundValue-unfolded_prevValue < .25 * 8 = 2
    // need aboveValue, soundValue, and prevValue within threshold
    // will be unfolding to match prevValue

    // in args
    float missingValue = -999e+33;

    // all must be within -28 +/- 2
    float aboveValue = -29.0;
    float soundValue = -29.99;
    float prevValue = -27.0;

    float startingValue = 4.0;  // -28 -12  x 20 36
    bool lastVolumeIsNull = false;
    float fraction = 0.25;  //  8 +/- 2 => 
    float NyqVelocity = 8.0;
    bool first_pass_only = true;
    
    float ck_val = 1.0;
    int max_count = 3;

    // out args
    float unfoldedValue = missingValue;
    bool successful = false;

    // find ray in sounding, closest to 130.0 degrees
    fourDD.TryToDealiasUsingVerticalAndTemporalContinuity(
            missingValue, aboveValue, soundValue, startingValue, prevValue,
            lastVolumeIsNull,
            fraction, NyqVelocity,
            first_pass_only,
            max_count,
            &unfoldedValue, &successful);
    EXPECT_TRUE(successful);
    EXPECT_EQ(-28.0, unfoldedValue);
  }



  TEST(FourDD, Filter3x3_all_missing) {
    FourDD fourDD;
    float missingVal = -999e+33;

    int maxSweeps = 1;
    int nbins = 3;
    int nrays = 3;
    int del_num_bins = 0;
    
    float nbins1[] = {-999e+33, -999e+33, -999e+33};
    float nbins2[] = {-999e+33, -999e+33, -999e+33};
    float nbins3[] = {-999e+33, -999e+33, -999e+33};

    Volume *velocity = Rsl::new_volume(maxSweeps);
    
    velocity->sweep[0] = Rsl::new_sweep(nrays);
    for (int r=0; r<nrays; r++) {
      velocity->sweep[0]->ray[r] = Rsl::new_ray(nbins);
      velocity->sweep[0]->ray[r]->h.binDataAllocated = true;
    }

    velocity->sweep[0]->ray[0]->range = nbins1;
    velocity->sweep[0]->ray[1]->range = nbins2;
    velocity->sweep[0]->ray[2]->range = nbins3;

    velocity->h.missing = missingVal;

    int binIdx = 1;
    int rayIdx = 1;
    int sweepIdx = 0;

    short expected = FourDD::MISSING; 
    short classification = fourDD.Filter3x3(velocity, binIdx, rayIdx, sweepIdx,
                                            del_num_bins);
    EXPECT_EQ(expected, classification);
  }

  TEST(FourDD, Filter3x3_5_nonMissing) {
    FourDD fourDD;
    float missingVal = -999e+33;

    int maxSweeps = 1;
    int nbins = 3;
    int nrays = 3;
    int del_num_bins = 0;
    
    float nbins1[] = {      -9,        3, -900e+33};
    float nbins2[] = {-999e+33, -999e+33, -999e+33};
    float nbins3[] = {      33, -999e+33,  999e+20};

    Volume *velocity = Rsl::new_volume(maxSweeps);
    
    velocity->sweep[0] = Rsl::new_sweep(nrays);
    for (int r=0; r<nrays; r++) {
      velocity->sweep[0]->ray[r] = Rsl::new_ray(nbins);
      velocity->sweep[0]->ray[r]->h.binDataAllocated = true;
    }

    velocity->sweep[0]->ray[0]->range = nbins1;
    velocity->sweep[0]->ray[1]->range = nbins2;
    velocity->sweep[0]->ray[2]->range = nbins3;

    velocity->h.missing = missingVal;

    int binIdx = 1;
    int rayIdx = 1;
    int sweepIdx = 0;

    short expected = FourDD::TBD; 
    short classification = fourDD.Filter3x3(velocity, binIdx, rayIdx, sweepIdx,
                                            del_num_bins);
    EXPECT_EQ(expected, classification);
  }

  TEST(FourDD, Filter3x3_border_3_nonMissing) {
    FourDD fourDD;
    float missingVal = -999e+33;

    int maxSweeps = 1;
    int nbins = 3;
    int nrays = 3;
    int del_num_bins = 0;
    
    float nbins1[] = {      -9,        3, -900e+33};
    float nbins2[] = {-999e+33, -999e+33, -999e+33};  // last element X
    float nbins3[] = {      33, -999e+33,  999e+20};

    Volume *velocity = Rsl::new_volume(maxSweeps);
    
    velocity->sweep[0] = Rsl::new_sweep(nrays);
    for (int r=0; r<nrays; r++) {
      velocity->sweep[0]->ray[r] = Rsl::new_ray(nbins);
      velocity->sweep[0]->ray[r]->h.binDataAllocated = true;
    }

    velocity->sweep[0]->ray[0]->range = nbins1;
    velocity->sweep[0]->ray[1]->range = nbins2;
    velocity->sweep[0]->ray[2]->range = nbins3;

    velocity->h.missing = missingVal;

    int binIdx = 2;
    int rayIdx = 1;
    int sweepIdx = 0;

    short expected = FourDD::TBD; 
    short classification = fourDD.Filter3x3(velocity, binIdx, rayIdx, sweepIdx,
                                            del_num_bins);
    EXPECT_EQ(expected, classification);
  }


  TEST(FourDD, Filter3x3_corner_2_nonMissing) {
    FourDD fourDD;
    float missingVal = -999e+33;

    int maxSweeps = 1;
    int nbins = 3;
    int nrays = 3;
    int del_num_bins = 0;

    //                 vvvv
    float nbins1[] = {      -9,        3, -999e+33};
    float nbins2[] = {-999e+33, -999e+33, -999e+33};
    float nbins3[] = {      33, -999e+33,  999e+20};  // last element X

    Volume *velocity = Rsl::new_volume(maxSweeps);
    
    velocity->sweep[0] = Rsl::new_sweep(nrays);
    for (int r=0; r<nrays; r++) {
      velocity->sweep[0]->ray[r] = Rsl::new_ray(nbins);
      velocity->sweep[0]->ray[r]->h.binDataAllocated = true;
    }

    velocity->sweep[0]->ray[0]->range = nbins1;
    velocity->sweep[0]->ray[1]->range = nbins2;
    velocity->sweep[0]->ray[2]->range = nbins3;

    velocity->h.missing = missingVal;

    int binIdx = 2;
    int rayIdx = 2;
    int sweepIdx = 0;

    short expected = FourDD::MISSING; 
    short classification = fourDD.Filter3x3(velocity, binIdx, rayIdx, sweepIdx,
                                            del_num_bins);
    EXPECT_EQ(expected, classification);
  }
    


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
